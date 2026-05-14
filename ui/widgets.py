from dataclasses import dataclass
from typing import Iterable

from omniecs.types import Bundle, Component
from ui.bundles import ActivatableBundle, InputBundle, PanelLayoutBundle, HoverableBundle, PressableBundle, RectTransformBundle, SelectableBundle, SurfaceBundle, TextVisualBundle, ToggleableBundle, WidgetCoreBundle


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
    hoverable: HoverableBundle
    pressable: PressableBundle
    activatable: ActivatableBundle
    
    def components(self) -> Iterable[Component]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.surface.components()
        yield from self.hoverable.components()
        yield from self.pressable.components()
        yield from self.activatable.components()


@dataclass
class ToggleBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    surface: SurfaceBundle
    hoverable: HoverableBundle
    activatable: ActivatableBundle
    toggleable: ToggleableBundle
    
    def components(self) -> Iterable[Component]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.surface.components()
        yield from self.hoverable.components()
        yield from self.activatable.components()
        yield from self.toggleable.components()


@dataclass
class TextInputBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    surface: SurfaceBundle
    hoverable: HoverableBundle
    inputable: InputBundle
    
    def components(self) -> Iterable[Component]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.surface.components()
        yield from self.hoverable.components()
        yield from self.inputable.components()
    

@dataclass
class RadioButtonBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    surface: SurfaceBundle
    hoverable: HoverableBundle
    selectable: SelectableBundle
    
    def components(self) -> Iterable[Component]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.surface.components()
        yield from self.hoverable.components()
        yield from self.selectable.components()


@dataclass
class MenuCategoryBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    surface: SurfaceBundle
    hoverable: HoverableBundle
    selectable: SelectableBundle      


@dataclass
class MenuItemBundle(Bundle):
    core: WidgetCoreBundle


# # def create_list


