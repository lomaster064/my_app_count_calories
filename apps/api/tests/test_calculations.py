from app.utils.calculations import calculate_bmi, calculate_bmr, calculate_tdee


def test_calculate_bmr_male():
    assert round(calculate_bmr(70, 175, 30, "male"), 1) == 1648.8


def test_calculate_tdee():
    assert round(calculate_tdee(1600, "medium"), 1) == 2480.0


def test_calculate_bmi():
    assert round(calculate_bmi(70, 175), 2) == 22.86
