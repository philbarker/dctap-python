"""Classes for Python objects derived from CSV files."""

from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import List
from .config import get_config_dict
from .utils import is_uri_or_prefixed_uri


@dataclass
class TAPStatementConstraint:
    """Instances hold TAP/CSV elements related to statement constraints."""

    # pylint: disable=too-many-instance-attributes
    # - It's a dataclass, right?
    # pylint: disable=invalid-name
    # - propertyID, etc, do not conform to snake-case naming style.

    propertyID: str = ""
    propertyLabel: str = ""
    mandatory: str = False
    repeatable: str = False
    valueNodeType: str = ""
    valueDataType: str = ""
    valueConstraint: str = ""
    valueConstraintType: str = ""
    valueShape: str = ""
    note: str = ""

    statement_warnings = defaultdict(list)

    config_dict = get_config_dict()

    def reset_config_dict(self, external_config_dict=None):
        self.config_dict = external_config_dict

    def normalize(self):
        """Normalizes values of certain fields."""
        # self._normalize_value_node_type(config_dict)
        # self._warn_about_literal_datatype_used_with_uri()
        return True

    def validate(self):
        """Validates values of certain fields."""
        self._value_uri_should_not_have_nodetype_literal()
        self._value_node_type_is_from_enumerated_list()
        return self

    def _value_uri_should_not_have_nodetype_literal(self):
        """URI values should usually not have a valueNodeType of Literal."""
        if is_uri_or_prefixed_uri(self.valueConstraint):
            if "Literal" in self.valueNodeType:
                self.statement_warnings['valueNodeType'] = (
                    f"{repr(self.valueConstraint)} looks like URI, but "
                    f"valueNodeType is {repr(self.valueNodeType)}."
                )
        return self

    def _value_node_type_is_from_enumerated_list(self):
        """Take valueNodeType from configurable enumerated list, case-insensitive."""
        valid_types = [nt.lower() for nt in self.config_dict['value_node_types']]
        if self.valueNodeType:
            self.valueNodeType = self.valueNodeType.lower() # normalize to lowercase
            if self.valueNodeType not in valid_types:
                self.statement_warnings['valueNodeType'] = (
                    f"{repr(self.valueNodeType)} is not a valid node type."
                )
        return self

    def get_warnings(self):
        """Emit warnings dictionary for this instance of TAPStatementConstraint.
        -- Dictionary is populated by invoking validate() mathod."""
        return dict(self.statement_warnings)


@dataclass
class TAPShape:
    """Instances hold TAP/CSV row elements related to shapes."""

    # pylint: disable=invalid-name
    # True that propertyID, etc, do not conform to snake-case naming style.

    shapeID: str = ""
    shapeLabel: str = ""
    start: bool = False
    sc_list: List[TAPStatementConstraint] = field(default_factory=list)

    # Initialize shape_warnings: TAPStatementConstraint as keys, blank list as values.
    shape_warnings = defaultdict(list)
    for field in list(shape_warnings):
        shape_warnings[field] = list()

#    def validate(self, config_dict=None):
#        """Normalize values where required."""
#        self._normalize_default_shapeID(config_dict)
#        return True

    def _normalize_default_shapeID(self, config_dict=None):
        """If shapeID not specified, sets default value from config."""
        if not self.shapeID:
            self.shapeID = config_dict['default_shape_name']
        return self

#    def get_shape_warnings(self):
#        """Emit shape_warnings for this instance of TAPStatementConstraint."""
#        return dict(shape_warnings)
#

# #         if not is_uri_or_prefixed_uri(sh_id):       # If shape key resembles not URI,
# #             warn_ddict["shapeID"] = (           # Warn that shape identifiers
# #                 f"{repr(sh_id)} should ideally "    # should ideally be URIs.
# #                 "be a URI."
# #             )