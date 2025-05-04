from enum import Enum
from typing import Any, Callable, List, Protocol, Tuple
import pygame

from utils.observable import Observable


class Widget(Protocol):

    def __init__(self, screen: pygame.Surface, label: str, area: pygame.Rect, color: pygame.Color, background: pygame.Color, hover_color: pygame.Color, font: pygame.font.Font = None):
        self.screen = screen
        self.label = label
        self.area = area
        self.color = color
        self.background = background
        self.hover_color = hover_color
        self.font = font or pygame.font.SysFont('Arial', 16)
        self.label_surface = self.render_text(self.label, self.color)
        self.enabled = True
        self.focused = False
        self.is_hovered = False
    
    @staticmethod
    def bind_state(object: object, field: str) -> Tuple[Callable, Callable]:
        return (
            lambda value: setattr(object, field, value),
            lambda: getattr(object, field)
        )
    
    @staticmethod
    def bind_observable_state(observable: Observable) -> Tuple[Callable, Callable]:
        return (
            lambda value: observable.set(value),
            lambda: observable.get()
        )
    
    @staticmethod
    def bind_dict_state(container: dict, key: Any) -> Tuple[Callable, Callable]:
        return (
            lambda value: container.__setitem__(key, value),
            lambda: container.get(key)
        )

    def render_text(self, text: str, color: pygame.Color) -> pygame.Surface:
        return self.font.render(text, True, color)

    def set_focus(self, value: bool) -> None:
        self.focused = value

    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    def draw(self) -> None:
        ...

    def center_middle_position(self, text_area: pygame.Surface) -> pygame.Vector2:
        x = self.area.left + (self.area.width - text_area.get_width()) / 2
        y = self.area.top + (self.area.height - text_area.get_height()) / 2
        return pygame.Vector2(x, y)

    def left_middle_position(self, text_area: pygame.Surface) -> pygame.Vector2:
        x = self.area.left + 5
        y = self.area.top + (self.area.height - text_area.get_height()) / 2
        return pygame.Vector2(x, y)


class Button(Widget):

    def __init__(self, screen: pygame.Surface, label: str, area: pygame.Rect, command: Callable, color: pygame.Color = pygame.Color('beige'), background: pygame.Color = pygame.Color('black'), hover_color: pygame.Color = pygame.Color('red'), press_color: pygame.Color = pygame.Color('darkgray'), font: pygame.font.Font = None):
        super().__init__(screen, label, area, color, background, hover_color, font)
        self.command = command
        self.hover_color = hover_color
        self.press_color = press_color
        self.pressed = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.enabled:
            return
        
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.area.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.is_hovered:
                self.pressed = False
                return self.command()

    def draw(self) -> None:
        if not self.enabled:
            return
        
        background_color = self.background
        if self.pressed and self.is_hovered:
            background_color = self.press_color

        pygame.draw.rect(self.screen, background_color, self.area)
        if self.is_hovered:
            pygame.draw.rect(self.screen, self.hover_color, self.area, 2)

        label_position = self.center_middle_position(self.label_surface)
        self.screen.blit(self.label_surface, label_position)


class TextInput(Widget):

    def __init__(self, screen: pygame.Surface, label: str, variable: Observable, area: pygame.Rect, focused_color: pygame.Color, color: pygame.Color = pygame.Color('beige'), background: pygame.Color = pygame.Color('black'), hover_color: pygame.Color = pygame.Color('red'), font: pygame.font.Font = None):
        super().__init__(screen, label, area, color, background, hover_color, font)
        self.variable = variable
        self.focused_color = focused_color
        self.variable.bind(self.update_text)
        self.text_surface = None
        self.update_text(self.get_value())

    def get_value(self) -> str:
        return self.variable.get()

    def set_value(self, value: str) -> None:
        self.variable.set(value)

    def handle_character(self, character: str) -> None:
        self.set_value(self.get_value() + character)

    def update_text(self, value: str) -> None:
        if not self.enabled:
            return
        self.text_surface = self.render_text(str(value), self.color)

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.area.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.focused = self.is_hovered
        elif event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:
                self.set_value(self.get_value()[:-1])
            elif event.key == pygame.K_RETURN:
                self.focused = False
            else:
                self.handle_character(event.unicode)

    def draw(self) -> None:
        if not self.enabled:
            return
        
        pygame.draw.rect(self.screen, self.background, self.area)
        if self.focused:
            pygame.draw.rect(self.screen, self.focused_color, self.area, 2)
        elif self.is_hovered:
            pygame.draw.rect(self.screen, self.hover_color, self.area, 2)

        label_position = self.left_middle_position(self.label_surface)
        self.screen.blit(self.label_surface, label_position)

        text_position = self.left_middle_position(self.text_surface) + pygame.Vector2(self.label_surface.get_width(), 0)
        self.screen.blit(self.text_surface, text_position)

        if self.focused:
            cursor_position = text_position.xy + pygame.Vector2(self.text_surface.get_width() + 2, 0)
            cursor_height = self.text_surface.get_height()
            pygame.draw.line(self.screen, self.color, cursor_position, cursor_position + pygame.Vector2(0, cursor_height))


class IntTextInput(TextInput):

    def __init__(self, screen: pygame.Surface, label: str, variable: Observable[int], area: pygame.Rect, focused_color: pygame.Color, color: pygame.Color = pygame.Color('beige'), background: pygame.Color = pygame.Color('black'), hover_color: pygame.Color = pygame.Color('red'), font: pygame.font.Font = None):
        super().__init__(screen, label, variable, area, focused_color, color, background, hover_color, font)

    def get_value(self) -> str:
        return str(self.variable.get())

    def set_value(self, value: str) -> None:
        if value:
            self.variable.set(int(value))
        else:
            self.variable.set(value)

    def handle_character(self, character: str) -> None:
        if character.isnumeric():
            self.set_value(int(self.get_value() + character))


class RadioStyle(Enum):
    CLASSIC = 1
    TOGGLE = 2


class RadioButton(Widget):

    def __init__(self, screen: pygame.Surface, label: str, value: Any, variable: Observable, area: pygame.Rect, color: pygame.Color = pygame.Color('beige'), background: pygame.Color = pygame.Color('black'), radius: int = 10, hover_color: pygame.Color = pygame.Color('red'), select_color: pygame.Color = pygame.Color('blue'), style: RadioStyle = RadioStyle.TOGGLE, font: pygame.font.Font = None):
        super().__init__(screen, label, area, color, background, hover_color, font)
        self.value = value
        self.variable = variable
        self.radius = radius
        self.inner_radius = radius * 0.6
        self.hover_color = hover_color
        self.select_color = select_color
        self.style = style
        self.variable.bind(self.update_widget)
        self.is_selected = False
        self.update_widget(self.variable.get())

    def update_widget(self, value: Any) -> None:
        if not self.enabled:
            return
        self.is_selected = value == self.value

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.area.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.variable.set(self.value)

    def draw(self) -> None:
        if not self.enabled:
            return
        
        if self.style == RadioStyle.CLASSIC:
            self.draw_classic()
        else:
            self.draw_toggle()

    def draw_classic(self) -> None:
        pygame.draw.rect(self.screen, self.background, self.area)
        if self.is_hovered:
            pygame.draw.rect(self.screen, self.hover_color, self.area, 2)
        if self.is_selected:
            pygame.draw.circle(self.screen, self.select_color, self.area.midleft + pygame.Vector2(self.radius, 0), self.inner_radius)
        label_position = self.left_middle_position(self.label_surface) + pygame.Vector2(self.radius * 2, 0)
        self.screen.blit(self.label_surface, label_position)

    def draw_toggle(self) -> None:
        background_color = self.select_color if self.is_selected else self.background
        pygame.draw.rect(self.screen, background_color, self.area)
        if self.is_hovered:
            pygame.draw.rect(self.screen, self.hover_color, self.area, 2)

        label_position = self.center_middle_position(self.label_surface)
        self.screen.blit(self.label_surface, label_position)


class Option(Protocol):

    @property
    def name(self) -> str:
        ...

    @property
    def color(self) -> str:
        ...

    @property
    def text_color(self) -> str:
        ...


class OptionPicker(Widget):

    def __init__(self, screen: pygame.Surface, variable: Observable[Option], popup_value: Any, popup: Observable, area: pygame.Rect, color: pygame.Color = pygame.Color('beige'), background: pygame.Color = pygame.Color('black'), hover_color: pygame.Color = pygame.Color('red'), font: pygame.font.Font = None):
        super().__init__(screen, '', area, color, background, hover_color, font)
        self.variable = variable
        self.popup_value = popup_value
        self.popup = popup
        self.variable.bind(self.update_option)
        self.update_option(self.variable.get())

    def update_option(self, option: Option) -> None:
        if not self.enabled:
            return
        self.label = option.name
        self.background = pygame.Color(option.color)
        self.color = option.text_color
        self.label_surface = self.render_text(self.label, self.color)

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.area.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.popup.set(self.popup_value)

    def draw(self) -> None:
        if not self.enabled:
            return
        
        pygame.draw.rect(self.screen, self.background, self.area)
        if self.is_hovered:
            pygame.draw.rect(self.screen, self.hover_color, self.area, 2)
        label_position = self.center_middle_position(self.label_surface)
        self.screen.blit(self.label_surface, label_position)


class Toggle(Widget):

    def __init__(self, screen: pygame.Surface, label: str, variable: Observable[bool], area: pygame.Rect, color: pygame.Color = pygame.Color('beige'), background: pygame.Color = pygame.Color('black'), hover_color: pygame.Color = pygame.Color('red'), toggle_color: pygame.Color = pygame.Color('blue'), font: pygame.font.Font = None):
        super().__init__(screen, label, area, color, background, hover_color, font)
        self.variable = variable
        self.hover_color = hover_color
        self.toggle_color = toggle_color
        self.variable.bind(self.update_toggle)
        self.current_background = self.background
        self.update_toggle(self.variable.get())

    def update_toggle(self, toggle: bool) -> None:
        if not self.enabled:
            return
        self.current_background = self.toggle_color if toggle else self.background

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.area.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.variable.set(not self.variable.get())

    def draw(self) -> None:
        if not self.enabled:
            return
        
        pygame.draw.rect(self.screen, self.current_background, self.area)
        if self.is_hovered:
            pygame.draw.rect(self.screen, self.hover_color, self.area, 2)

        label_position = self.center_middle_position(self.label_surface)
        self.screen.blit(self.label_surface, label_position)


class Panel(Protocol):

    def __init__(self, screen: pygame.Surface, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        self.screen = screen
        self.area = area
        self.background = background
        self.frame_color = frame_color
        self.surface = pygame.Surface(self.area.size, pygame.SRCALPHA)
        self.widgets: List[Widget] = []

    def add_widget(self, widget: Widget) -> None:
        self.widgets.append(widget)

    def handle_event(self, event: pygame.event.Event) -> None:
        adjusted_event = pygame.event.Event(event.type, **event.dict)
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            relative_position = pygame.Vector2(event.pos) - pygame.Vector2(self.area.topleft)
            adjusted_event.pos = relative_position

        for widget in self.widgets:
            widget.handle_event(adjusted_event)

    def draw(self) -> None:
        self.surface.fill(self.background)
        for widget in self.widgets:
            widget.draw()
        pygame.draw.rect(self.surface, self.frame_color, self.surface.get_rect(), 2)
        self.screen.blit(self.surface, self.area.topleft)
