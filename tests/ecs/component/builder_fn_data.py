import pytest
from ecs_architecture.component import COMPONENTS


@pytest.fixture(params=COMPONENTS, ids=lambda cls: '.'.join(cls.__name__.split('.')[-2:]))
def component_case(request):
    component_cls = request.param
    return component_cls.test_config
