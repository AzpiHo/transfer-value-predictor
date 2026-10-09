from ftv_ml import TrainingPipeline


def test_plan_is_position_specific_and_untrained() -> None:
    plan = TrainingPipeline().plan()
    assert plan.horizon_months == 6
    assert plan.label_source == "unconfigured"
    assert [model.position for model in plan.models] == ["GK", "DF", "MF", "FW"]
    for model in plan.models:
        assert model.target == "delta_market_value_eur"
        assert model.outputs == ("direction", "magnitude")
        assert model.horizon_months == 6
    assert "does not train" in plan.notes
