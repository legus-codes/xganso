from omniecs.world import World, SystemProtocol
from ui.components.content import Variable
from adapters.input.events import Key, KeyDown
from ui.components.rendering import Dirty
from ui.components.behavior import Enabled, Focused, InputFilter


class EnterKeySystem(SystemProtocol):

    def __init__(self, world: World, keyboard: int):
        self.world = world
        self.keyboard = keyboard

    def execute(self, delta_time: float):
        key_down: KeyDown = self.world.get_entity_component(self.keyboard, KeyDown)
        if key_down is None or key_down.key != Key.ENTER.value:
            return

        for entity in self.world.get_entities_with(Enabled, Focused, InputFilter):
            self.world.remove_component(entity, Focused)
            self.world.add_component(entity, Dirty())


class DeleteKeySystem(SystemProtocol):

    def __init__(self, world: World, keyboard: int):
        self.world = world
        self.keyboard = keyboard

    def execute(self, delta_time: float):
        key_down: KeyDown = self.world.get_entity_component(self.keyboard, KeyDown)
        if key_down is None or key_down.key != Key.DELETE.value:
            return

        for entity, (variable, _, _, _) in self.world.get_entities_with_components(Variable, InputFilter, Enabled, Focused):
            variable.value = variable.value[:-1]
            self.world.add_component(entity, Dirty())


class TypingKeyDownSystem(SystemProtocol):

    def __init__(self, world: World, keyboard: int):
        self.world = world
        self.keyboard = keyboard

    def execute(self, delta_time: float):
        key_down: KeyDown = self.world.get_entity_component(self.keyboard, KeyDown)
        if key_down is None:
            return
        
        for entity, (variable, typeable, _, _) in self.world.get_entities_with_components(Variable, InputFilter, Enabled, Focused):
            if key_down.char in typeable.accepted_chars:
                variable.value += key_down.char
                self.world.add_component(entity, Dirty())


class CleanupKeyDownSystem(SystemProtocol):

    def __init__(self, world: World, keyboard: int):
        self.world = world
        self.keyboard = keyboard

    def execute(self, delta_time: float):
        self.world.remove_component(self.keyboard, KeyDown)
