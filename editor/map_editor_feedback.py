from dataclasses import dataclass, field
from datetime import datetime
from ecs_framework.ecs import ECS, ComponentProtocol, SystemProtocol
from ui.ui_components import UILabel, UINeedRedraw


@dataclass
class Feedback(ComponentProtocol):
    message: str
    timestamp: datetime = field(init=False)

    def __post_init__(self):
        self.timestamp = datetime.now()

@dataclass
class FeedbackDisplayer(ComponentProtocol):
    pass


class FeedbackBroadcastSystem(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world

    def execute(self, delta_time):
        all_feedbacks = []
        for entity, feedback in self.world.get_entities_with_single_component(Feedback):
            all_feedbacks.append(feedback)
            self.world.remove_component(entity, Feedback)

        if not all_feedbacks:
            return

        all_feedbacks.sort(key=lambda x: x.timestamp)
        feedback = all_feedbacks[0].message

        for entity, (label, _) in self.world.get_entities_with_components(UILabel, FeedbackDisplayer):
            label.label = feedback
            self.world.add_component(entity, UINeedRedraw())
