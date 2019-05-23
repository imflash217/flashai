"""`flashai.data` loads and manages datasets with `DataBunch`"""

from torch.utils.data.dataloader import default_collate

class DataBunch():
    """Bind `train_dl`, `valid_dl`, and `test_dl` in a data object."""

    def __init__(self, train_dl: DataLoader, valid_dl: DataLoader,
                    fix_dl: DataLoader=None, test_dl: Optional[DataLoader]=None,
                    device: torch.device=None, dl_tfms: Optional[Collection[Callable]]=None,
                    path: PathOrStr=".", collate_fn: Callable=data_collate, no_check: bool=False):

        self.dl_tfms = listify(dl_tfms)
        self.device = defaults.device if device is None else device
        assert not isinstance(train_dl, DeviceDataLoader)

        def _create_dl(dl, **kwargs):
            if dl is None:
                return None
            return DeviceDataLoader(dl, self.device, self.dl_tfms, collate_fn, **kwargs)

        self.train_dl, self.valid_dl, self.fix_dl, self.test_dl = map(_create_dl, [train_dl, valid_dl, fix_dl, test_dl])
        if fix_dl is None:
            self.fix_dl = slef.train_dl.new(shuffle=False, drop_last=False)
        self.single_dl = _create_dl(DataLoader(valid_dl.dataset, batch_size=1, num_workers=0))
        self.path = Path(path)
        if not no_check:
            self.sanity_check()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__};\n\nTrain: {self.train_ds};\n\nValid: {self.valid_ds};\n\nTest: {self.test_ds}"

    @staticmethod
    def _init_ds(train_ds: Dataset, valid_ds: Dataset, test_ds: Optional[Dataset]=None):
        """train_ds, but without training tfms"""
        fix_ds = valid_ds.new(train_ds.x, train_ds.y) if hasattr(valid_ds, "new") else train_ds
        return [o for o in (train_ds, valid_ds, fix_ds, test_ds) if o is not None]

    @classmethod
    def create(cls, trains_ds: Dataset, valid_ds: Dataset, test_ds: Optionla[Dataset]=None, path: PathOrStr=".",
                bs: int=64, val_bs: int=None, num_workers: int=defaults.cpus, dl_tfms: Optional[Colletion[Callable]]=None,
                device: torch.device=None, collate_fn: Callable=data_collate, no_check: bool=False, **dl_kwargs) -> "DataBunch":
        """
        Create a `DataBunch` from `train_ds`, `valid_ds` and maybe `test_ds` with a batchsize of `bs`.
        Passes `**dl_kwargs` to `DataLoader()`.
        """

        datasets = cls._init_ds(train_ds=train_ds, valid_ds=valid_ds, test_ds=test_ds)
        valid_bs = ifnone(valid_bs, bs)
        dls = [DataLoader(d, b, shuffle=s, drop_last=s, num_workers=num_workers, **dl_kwargs) for d, b, s in
               zip(datasets, (bs, val_bs, val_bs, val_bs), (True, False, False, False)) if d in not None]
        return cls(*dls, path=path, device=device, dl_tfms=dl_tfms, collate_fn=collate_fn, no_check=no_check)

    def __getattr__(self, k: int) -> Any:
        return getattr(self.train_dl, k)

    def __setattr__(self, data: Any):
        self.__dict__.update(data)

    def dl(self, ds_type: DatasetType=DatasetType.Valid) -> DeviceDataLoader:
        """
        Returns appropriate `Dataset` for validation, training, or test (`ds_type`)
        """
        #TODO: refactor
        return (self.train_dl if ds_type == DatasetType.Train else
                self.valid_dl if ds_type == DatasetType.Valid else
                self.test_dl if ds_type == DatasetType.Test else
                self.single_dl if ds_type == DataseType.Single else
                self.fix_dl)

    @property
    def dls(self) -> List[DeviceDataLoader]:
        """
        Returns a list of all `DeviceDataLoaders`.
        If you need a specific `DeviceDataLoader`, access via the relevant property (`train_dl`, `valid_dl`, etc)
        as the index if DLs in this list is not guranteed to remain constant.
        """

        result = [self.train_dl, self.fix_dl, self.single_dl]

        # Preserve the original ordering of Train, Valid, Fix, Single, Test data loaders
        if self.valid_dl:
            result.insert(1, self.valid_dl)
        return result if not self.test_dl else result + [self.test_dl]

    def add_tfm(self, tfm: Callable) -> None:
        for dl in self.dls:
            dl.add_tfm(tfm)

    def remove_tfm(self, tfm: Callable) -> None:
        for dl in self.dls:
            dl.remove_tfm(tfm)

    def save(self, file: PathLikeOrBinaryStream="data_save.pkl") -> None:
        """
        Save the `DataBunch` in `self.path/file`.
        `file` can be file-like (file or binary)
        """

        if not getattr(self, 'label_list', False):
            warn("Serializing the `DataBunch` only works when you created it using the DataBlock API")
            return
        try_save(self.lable_list, self.path, file)

    def add_test(self, items: Iterator, label: Any=None) -> None:
        """
        Add the `items` as a test set.
        Pass along `label` otherwise lable them with `EmptyLabel`
        """
        self.label_list.add_test(items, label=label)
        vdl = self.valid_dl
        dl = DataLoader(self.label_list.test, vdl.batch_size, shuffle=False, drop_last=False, num_workers=vdl.num_workers)
        self.test_dl = DeviceDataLoader(dl, vdl.device, vdl.tfms, vdl.collate_fn)

    def one_batch(self, ds_type: DatasetType=DatasetType.Train,
                  detach: bool=True, denorm: bool=True, cpu: bool=True) -> Collection[Tensor]:
        """
        Get one batch from the dataloader of `ds_type`.
        Optionally `detach` and `denorm`
        """
        dl = self.dl(ds_type)
        w = self.num_workers
        self.num_workers = 0
        try:
            x, y = next(iter(dl))
        finally:
            self.num_workers = w
        if detach:
            x, y = to_detach(x, cpu=cpu), to_detach(y, cpu=cpu)
        norm = getattr(self, "norm", False)
        if denorm and norm:
            x = self.denorm(x)
            if norm.keywords.get("do_y", False):
                y = self.denorm(y, do_x=True)
        return x, y

    def one_item(self, item, detach: bool=False, denorm: bool=False, cpu: bool=False):
        """
        Get one `item` into a batch.
        Optionally `detach` and `denorm`
        """
        ds = self.single_ds
        with ds.set_item(item):
            return self.one_batch(ds_type=DatasetType.Single, detach=detach, denorm=denorm, cpu=cpu)

    def show_batch(self, rows: int=5, ds_type: DatasetType=DatasetType.Train, reverse: bool=False, **kwargs) -> None:
        """
        Show a batch of data in `ds_type` on a few `rows`
        """

        # Grabbing one batch of data from th dataset
        x, y = self.one_batch(ds_type, True, True)
        if reverse:
            x, y = x.flip(0), y.flip(0)
        n_items = rows**2 if self.train_ds.x._square_show else rows

        # checking if the requested number of items exist in the batch
        if self.dl(ds_type).batch_size < n_items:
            n_items = self.dl(ds_type).batch_size

        # grabbing items from x
        xs = [self.train_ds.x.reconstruct(grab_idx(x, i)) for i in range(n_items)]

        # TODO: get rid of has_arg if possible
        # grabbing the corresponding ys
        if has_arg(self.train_ds.y.reconstruct, "x"):
            ys = [self.train_ds.y.reconstruct(grab_idx(y, i), x=x) for i, x in enumerate(xs)]
        else:
            ys = [self.train_ds.y.reconstruct(grab_idx(y, i)) for i in range(n_items)]

        self.train_ds.x.show_xys(xs, ys, **kwargs)


    def sanity_check(self):
        """
        Check the underlying data in the training set, whether it can be properly loaded or not
        """
        final_message = "You can deactivate this message by passing `no_check=True`"

        # Checking whether the train_ds or train_dl has items in it or whether it is empty or corrupted
        if not hasattr(self.train_ds, 'items') or len(self.train_ds.items) == 0 or not hasattr(self.train_dl, 'batch_sampler'):
            return
        if len(self.train_dl) == 0:
            warn(f"Your training dataloader is EMPTY, you have only {len(self.train_dl.dataset)} items in the training set."
                 f"Your batchsize is {self.train_dl.batch_size}, you should lower it.")
            print(final_message)
            return
        idx = next(iter(self.train_dl.batch_sampler))
        samples, fails = [], []

        # Collecting the samples from the training dataset. Indexing sucessful/failed attempts
        for i in idx:
            try:
                samples.append(self.train_dl.dataset[i])
            except:
                fails.append(i)

        # Handling the cases when one or more fails while retrieving samples from the dataset
        if len(fails) > 0:
            warn_msg = f"There seems to be something wrong with your dataset. For example, in the first batch we can't access "
            if len(fails) == len(idx):
                warn_msg += f"any element of self.train_ds\nTried: {show_some(idx)}"
            else:
                warn_msg += f"these elements in self.train_ds:\n{show_some(fails)}"
            warn(warn_msg)
            print(final_message)
            return

        try:
            batch = self.collate_fn(samples)
        except:
            message = f"Failed to collate samples of your dataset together in a batch"
            try:
                shapes = [[o[i].data.shape for o in samples] for i in range(2)]
                message += f"\nShapes of the inputs/targets: \n{shapes}"
            except:
                pass
            warn(message)
            print(final_message)

    def load_data(path: PathOrStr, file: PathLikeOrBinaryStream="data_save.pkl",
                  bs: int=64, val_bs: int=None, num_workers: int=defaults.cpus,
                  dl_tfms: Optional[Collections[Callable]]=None, device: torch.device=None,
                  collate_fn: Callable=data_collate, no_check: bool=False, **kwargs) -> DataBunch:
        """
        Loads a saved `DataBunch` from `path/file`.
        `file` can be file-like (file or buffer)
        """
        source = Path(path)/file if is_pathlike(file) else file
        ll = torch.load(source, map_location="cpu") if defaults.device == torch.device("cpu") else torch.load(source)
        return ll.databunch(path=path, bs=bs, val_bs=val_bs, num_workers=num_workers, dl_tfms=dl_tfms,
                            device=device, collate_fn=collate_fn, no_check=no_check, **kwargs)

















