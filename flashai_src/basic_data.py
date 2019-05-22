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

    def __setattr__(self, data:Any):
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













