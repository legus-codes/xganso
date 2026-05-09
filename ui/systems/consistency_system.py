from collections import defaultdict

from omniecs.system import System
from omniecs.types import EntityId

from ui.components.behavior import Selected, SelectionGroup
from ui.events.events import DeselectItemEvent

class RadioGroupConsistencyCheckerSystem(System):

    def execute(self, _: float) -> None:
        radio_groups: dict[str, set[EntityId]] = defaultdict(set)
        for (entity_id, (selection_group,)) in self.world.query(SelectionGroup,):
            radio_groups[selection_group.group].add(entity_id)

        for group_id, entity_ids in radio_groups.items():
            selected_items: list[EntityId] = []
            for entity_id in entity_ids:
                selected = self.world.get_component(entity_id, Selected)
                
                if selected is None:
                    continue

                selected_items.append(entity_id)

            if len(selected_items) > 1:
                selected_item = sorted(selected_items, key=lambda x: x.value)[0]
                self.world.push_event(DeselectItemEvent(radio_group=group_id, selected_item=selected_item))
