from ui.resources.state import WidgetState


def test_default_widget_state():
    widget = WidgetState()
    assert widget.active_entities == set()
    assert widget.hovered_entities == set()
