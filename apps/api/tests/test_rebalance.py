from app.utils.rebalance import rebalance_day


def test_rebalance_with_overage():
    result = rebalance_day(2000, 2300, 2, True, ["knee"])
    assert result.new_targets["remaining_calories"] == 0
    assert result.workout_suggestion is not None


def test_rebalance_normal():
    result = rebalance_day(2000, 1200, 2, False, [])
    assert result.new_targets["remaining_calories"] == 800
    assert result.new_targets["per_meal_target"] == 400
    assert result.workout_suggestion is None
