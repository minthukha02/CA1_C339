import pytest
from src.parcel_fee import delivery_fee


@pytest.mark.parametrize(
    "weight_grams, expected_fee",
    [
        (1, 500),       # TC_DF_01: Band 1 lower boundary
        (500, 500),     # TC_DF_02: Band 1 typical value
        (1000, 500),    # TC_DF_03: Band 1 upper boundary (catches < 1000 bug)
        (1001, 1000),   # TC_DF_04: Band 2 lower boundary
        (10000, 1000),  # TC_DF_05: Band 2 typical value
        (20000, 1000),  # TC_DF_06: Band 2 upper boundary
    ],
)
def test_delivery_fee_valid(weight_grams, expected_fee):
    result = delivery_fee(weight_grams)
    assert result == expected_fee
    assert type(result) is int


@pytest.mark.parametrize(
    "weight_grams",
    [
        0,       # TC_DF_07: Just below minimum weight
        -100,    # TC_DF_08: Negative weight
        20001,   # TC_DF_09: Just above maximum weight
    ],
)
def test_delivery_fee_out_of_range(weight_grams):
    with pytest.raises(ValueError):
        delivery_fee(weight_grams)


@pytest.mark.parametrize(
    "weight_grams",
    [
        True,    # TC_DF_10: Boolean (not a valid int per spec)
        500.5,   # TC_DF_11: Float
        "500",   # TC_DF_12: String
        None,    # TC_DF_13: None
    ],
)
def test_delivery_fee_invalid_type(weight_grams):
    with pytest.raises(TypeError):
        delivery_fee(weight_grams)