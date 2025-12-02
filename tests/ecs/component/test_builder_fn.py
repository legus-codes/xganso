import pytest
from pydantic import ValidationError

from tests.ecs.component.builder_fn_data import component_case

def test_build_valid_component(component_case: dict):
    builder = component_case['builder']
    cls = component_case['cls']
    parameters = component_case['parameters']
    fields = component_case['fields']

    component = builder(**parameters)

    assert isinstance(component, cls)
    for field, value in fields.items():
        assert getattr(component, field) == value

def test_build_invalid_component(component_case: dict):
    builder = component_case['builder']

    for invalid_paramters in component_case['invalid_cases']:
        with pytest.raises(ValidationError):
            builder(**invalid_paramters)
