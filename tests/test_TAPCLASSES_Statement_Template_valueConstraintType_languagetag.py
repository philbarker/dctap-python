"""Tests for private functions called by TAPStatementTemplate.normalize()."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.csvreader import csvreader

config_dict = get_config()

def test_valueConstraintType_languagetag_parse():
    """If valueConstraintType list, valueConstraint parsed on whitespace."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:creator"
    sc.valueConstraintType = "languagetag"
    sc.valueConstraint = "fr it de"
    sc._valueConstraintType_languageTag_parse(config_dict)
    assert sc.valueConstraint == ["fr", "it", "de"]

def test_valueConstraintType_languagetag_item_separator_comma(tmp_path):
    """@@@"""
    config_dict = get_config()
    config_dict["list_item_separator"] = ","
    config_dict["default_shape_identifier"] = "default"
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            'PropertyID,valueConstraintType,valueConstraint\n'
            'ex:foo,languagetag,"fr, it, de"\n'
        )
    )
    value_constraint = csvreader(open(csvfile_path), config_dict)[0]["shapes"][0]["statement_templates"][0]["valueConstraint"]
    assert value_constraint == ["fr", "it", "de"]

def test_valueConstraintType_languagetag_item_separator_pipe(tmp_path):
    """@@@"""
    config_dict = get_config()
    config_dict["list_item_separator"] = "|"
    config_dict["default_shape_identifier"] = "default"
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            'PropertyID,valueConstraintType,valueConstraint\n'
            'ex:foo,languagetag,"fr|it|de"\n'
        )
    )
    value_constraint = csvreader(open(csvfile_path), config_dict)[0]["shapes"][0]["statement_templates"][0]["valueConstraint"]
    assert value_constraint == ["fr", "it", "de"]

