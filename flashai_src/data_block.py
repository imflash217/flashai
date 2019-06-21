"""
The data block API lets you customize the creation of a `DataBunch` by isolating the underlying parts of that process in separate blocks, mainly:
    1. Where are the inputs and how to create them?
    2. How to split the data into a training and validation sets?
    3. How to label the inputs?
    4. What transforms to apply?
    5. How to add atest set?
    6. How to wrap in dataloaders and create the `DataBunch`?
"""

__author__ = "@imflash217"
__copyright__ = "flashAI @2019"


