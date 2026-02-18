from dataclasses import dataclass
from typing import Iterable

from ecs_framework.types import Bundle, Component
from ui.bundles import ActivatableBundle, InputBundle, PanelLayoutBundle, PointerBundle, RectTransformBundle, SelectableBundle, SurfaceBundle, TextVisualBundle, ToggleableBundle, WidgetCoreBundle


@dataclass
class PanelBundle(Bundle):
    core: WidgetCoreBundle
    transform: RectTransformBundle
    layout: PanelLayoutBundle
    surface: SurfaceBundle
    
    
    def components(self) -> Iterable[Component]:
        yield from self.core.components()
        yield from self.transform.components()
        yield from self.layout.components()
        yield from self.surface.components()


@dataclass
class TextBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    surface: SurfaceBundle
    
    def components(self) -> Iterable[Component]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.surface.components()


@dataclass
class ButtonBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    surface: SurfaceBundle
    pointer: PointerBundle
    activatable: ActivatableBundle
    
    def components(self) -> Iterable[Component]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.surface.components()
        yield from self.pointer.components()
        yield from self.activatable.components()


@dataclass
class ToggleBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    surface: SurfaceBundle
    pointer: PointerBundle
    activatable: ActivatableBundle
    toggleable: ToggleableBundle
    
    def components(self) -> Iterable[Component]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.surface.components()
        yield from self.pointer.components()
        yield from self.activatable.components()
        yield from self.toggleable.components()


@dataclass
class TextInputBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    surface: SurfaceBundle
    pointer: PointerBundle
    inputable: InputBundle
    
    def components(self) -> Iterable[Component]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.surface.components()
        yield from self.pointer.components()
        yield from self.inputable.components()
    

@dataclass
class RadioButtonBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    surface: SurfaceBundle
    pointer: PointerBundle
    selectable: SelectableBundle
    
    def components(self) -> Iterable[Component]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.surface.components()
        yield from self.pointer.components()
        yield from self.selectable.components()



# def create_radio_button(world: ECS, label: str, radio_group: str, rect: pygame.Rect, parent: Optional[int] = None, trigger: Optional[Component] = None) -> int:
#     entity = create_button(world, label, rect, trigger, parent)
#     world.add_component(entity, Selectable())
#     world.add_component(entity, RadioItem(radio_group))
#     return entity



# # def create_list


