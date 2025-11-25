import pytest


@pytest.fixture(autouse=True)
def _restore_default_conversation_threshold(monkeypatch):
    # Tests rely on conversation grouping matching the sample data (30 minutes).
    # If the runtime default changes, pin it here to keep fixtures stable.
    monkeypatch.setattr("src.utils.constants.DEFAULT_CONVERSATION_STARTER_THRESHOLD_MINUTES", 30)
