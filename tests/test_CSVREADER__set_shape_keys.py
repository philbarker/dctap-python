"""
dctap.csvreader._set_shape_keys - from docstring:

    Populates shape fields of dataclass TAPShape object from dict for one row.

    Args:
        tapshape_obj: Unpopulated instance of dctap.tapclasses.TAPShape:
            TAPShape(shapeID='', shapeLabel='', st_list=[], sh_warnings={}, extras={})
        row_dict: Dictionary of all columns headers (keys) and cell values (values) 
            found in a given row, with no distinction between shape elements and 
            statement template elements.
        main_shape_elements: Default TAPClass fields related to shapes.
        xtra_shape_elements: Extra TAPClass fields as per optional config file.

    Returns:
        TAPShape object with shape fields set.
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config, get_shems
from dctap.csvreader import _get_tapshapes, _set_shape_keys
from dctap.defaults import DEFAULT_CONFIGFILE_NAME
from dctap.exceptions import ConfigError
from dctap.tapclasses import TAPShape


def test_get_tapshapes_shape_elements_on_their_own_line(tmp_path):
    """Getting rows_list from tests/test_CSVREADER_get_rows.py ."""
    os.chdir(tmp_path) # precaution to avoid interference among pytests
    config_dict = get_config()
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel"]
    config_dict["extra_shape_elements"] = ["closed", "start"]
    (main_shems, xtra_shems) = get_shems(shape_class=TAPShape, settings=config_dict)
    shape_instance = TAPShape()
    one_row = {
        "shapeID": ":a",
        "shapeLabel": "Book",
        "closed": False,
        "start": True,
        "propertyID": "ex:name",
        "valueNodeType": "literal",
    }
    assert _set_shape_keys(
        tapshape_obj=shape_instance,
        row_dict=one_row,
        main_shape_elements=main_shems,
        xtra_shape_elements=xtra_shems,
    ) == TAPShape(
        shapeID=':a', 
        shapeLabel='Book', 
        st_list=[], 
        sh_warnings={}, 
        extras={"closed": False, "start": True}
    )

#     one_row = {
#         "shapeID": ":a",
#         "shapeLabel": "Book",
#         "closed": False,
#         "start": True,
#         "propertyID": "ex:name",
#         "valueNodeType": "literal",
#     }