from collections import defaultdict

from omniecs.system import System
from omniecs.types import EntityId

from ui.components.behavior import Selectable, Selected, SelectionGroup
from ui.events.events import DeselectGroupEvent

class SelectionGroupConsistencyCheckerSystem(System):

    def execute(self, _: float) -> None:
        radio_groups: dict[str, set[EntityId]] = defaultdict(set)
        for (entity_id, (selection_group,)) in self.world.query(SelectionGroup, all_of=(Selected,)):
            radio_groups[selection_group.group].add(entity_id)

        for group_id, entity_ids in radio_groups.items():
            if len(entity_ids) > 1:
                selected_item = sorted(entity_ids, key=lambda x: x.value)[0]
                self.world.push_event(DeselectGroupEvent(group=group_id, selected=selected_item))
                selectable: Selectable = self.world.get_component(selected_item, Selectable)
                for command in selectable.enter:
                    self.world.add_component(selected_item, command)                   
