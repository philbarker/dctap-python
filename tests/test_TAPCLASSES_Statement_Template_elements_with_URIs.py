"""Test for elements mandatory and repeatable."""

from dctap.tapclasses import TAPStatementTemplate

def test_warn_if_propertyID_not_URI():
    """In DCTAP, propertyID _should_ be an IRI."""
    sc = TAPStatementTemplate()
    sc.propertyID = "P31"
    sc._warn_if_propertyID_or_valueDataType_not_IRIlike()
    print(sc.state_warns)
    print(dict(sc.state_warns))
    print(len(dict(sc.state_warns)))
    assert len(dict(sc.state_warns)) == 1


def test_warn_if_valueDataType_not_URI():
    """In DCTAP, valueDataType _should_ be an IRI."""
    sc = TAPStatementTemplate()
    sc.propertyID = "wdt:P31"
    sc.valueDataType = "date"
    sc._warn_if_propertyID_or_valueDataType_not_IRIlike()
    print(sc.state_warns)
    print(dict(sc.state_warns))
    print(len(dict(sc.state_warns)))
    assert len(dict(sc.state_warns)) == 1
