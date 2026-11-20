import pytest
from src.parcel_acceptance import is_parcel_accepted


@pytest.mark.parametrize(
    "weight_grams, length_cm, expected",
    [
        (1, 1, True),          # TC_PA_01: Both at lower valid boundaries
        (5000, 100, True),     # TC_PA_02: Typical valid inputs
        (20000, 200, True),    # TC_PA_03: Both at upper valid boundaries (catches < 200 bug)
        (20000, 50, True),     # TC_PA_04: Weight at upper boundary, typical length
        (500, 200, True),      # TC_PA_05: Typical weight, length at upper boundary (catches < 200 bug)
        (0, 100, False),       # TC_PA_06: Zero weight
        (500, 0, False),       # TC_PA_07: Zero length
        (20001, 100, False),   # TC_PA_08: Weight above limit
        (500, 201, False),     # TC_PA_09: Length above limit
        (25000, 250, False),   # TC_PA_10: Both above limits
    ],
)
def test_is_parcel_accepted_valid_and_rejected(weight_grams, length_cm, expected):
    result = is_parcel_accepted(weight_grams, length_cm)
    assert result is expected
    assert type(result) is bool


@pytest.mark.parametrize(
    "weight_grams, length_cm",
    [
        (-1, 100),    # TC_PA_11: Negative weight
        (500, -1),    # TC_PA_12: Negative length
        (-10, -5),    # TC_PA_13: Both negative
    ],
)
def test_is_parcel_accepted_negative_values(weight_grams, length_cm):
    with pytest.raises(ValueError):
        is_parcel_accepted(weight_grams, length_cm)


@pytest.mark.parametrize(
    "weight_grams, length_cm",
    [
        (True, 100),     # TC_PA_14: Boolean weight
        (500, False),    # TC_PA_15: Boolean length
        (500.0, 100),    # TC_PA_16: Float weight
        (500, "100"),    # TC_PA_17: String length
        (None, 100),     # TC_PA_18: None weight
    ],
)
def test_is_parcel_accepted_invalid_type(weight_grams, length_cm):
    with pytest.raises(TypeError):
        is_parcel_accepted(weight_grams, length_cm)