from dataclasses import dataclass
import math
import random
from typing import List
import pygame

from battle.unit import Party


class Needle:

    def __init__(self, screen: pygame.Surface, center: pygame.Vector2, length: float):
        self.screen = screen
        self.center = center
        self.length = length
        self.angle = 0
        self.spin_speed = 0
        self.deceleration = 0
        self.spinning = False

    def spin(self) -> None:
        self.angle = random.randint(0, 359)
        self.spin_speed = 0.4 + random.random() * 0.2
        self.deceleration = 0.001 + random.random() * 0.003
        self.spinning = True

    def update(self) -> None:
        self.angle = (self.angle + self.spin_speed) % 360
        self.spin_speed = max(self.spin_speed - self.deceleration, 0)
        if self.spin_speed <= 0.001:
            self.spinning = False

    def draw(self) -> None:
        end_point = pygame.Vector2(self.length * math.cos(self.angle), self.length * math.sin(self.angle))
        pygame.draw.line(self.screen, pygame.Color('black'), self.center, self.center + end_point, 3)


class SpinningWheel:

    def __init__(self, screen: pygame.Surface, area: pygame.Rect, radius: int):
        self.screen = screen
        self.area = area
        self.radius = radius
        self.parties = []
        self.angles = {}
        self.order = []
        self.polygons = {}
        self.labels = []
        self.font = pygame.font.SysFont(None, 24)
        self.needle = Needle(self.screen, self.area.center, self.radius * 0.75)
        self.result = None

    def set_parties(self, parties: List[Party]) -> None:
        self.parties = parties
        self.setup_board()

    def setup_board(self) -> None:
        angle_per_sector = 360 / len(self.parties)
        self.angles = {}
        self.polygons = {}
        self.labels = []

        for index, party in enumerate(self.parties):
            start_angle = angle_per_sector * index
            end_angle = angle_per_sector * (index + 1)
            self.angles[party.name] = (start_angle, end_angle)
            self.polygons[party] = self.get_polygon_points(math.radians(start_angle), math.radians(end_angle), self.area.center, 10)

            # points = [center]
            # steps = 30
            # start_angle_radians = math.radians(start_angle)
            # end_angle_radians = math.radians(end_angle)
            # angle_step = (end_angle_radians - start_angle_radians) / steps
            # for step in range(steps+1):
            #     angle = start_angle_radians + angle_step * step
            #     x = center[0] + self.radius * math.cos(angle)
            #     y = center[1] + self.radius * math.sin(angle)
            #     points.append((x, y))

            # mid_angle = (start_angle_radians + end_angle_radians) / 2
            # label_x = center[0] + self.radius * 0.6 * math.cos(mid_angle)
            # label_y = center[1] + self.radius * 0.6 * math.sin(mid_angle)
            # label = self.font.render(party.name, True, 'black')
            # self.screen.blit(label, label.get_rect(center=(label_x, label_y)))

    def get_polygon_points(self, start_angle: float, end_angle: float, center: pygame.Vector2, steps: int) -> List[pygame.Vector2]:
        points = [center]
        angle_step = (end_angle - start_angle) / steps
        for step in range(steps+1):
            angle = start_angle + angle_step * step
            offset = pygame.Vector2(self.radius * math.cos(angle), self.radius * math.sin(angle))
            points.append(center + offset)
        return points

    def start(self) -> None:
        self.result = None
        self.needle.spin()

    # def stop(self) -> None:
    #     self.spinning = False
    #     selection = self.get_selected()
    #     print(selection.name)
    #     self.order.append(selection)

    # def get_selected(self) -> None:
    #     angle = self.angle % 360
    #     index = int(angle / self.angle_per_sector)
    #     print(self.angle, angle, index)
    #     return self.parties[index]

    def update(self) -> None:
        self.needle.update()

    def draw(self) -> None:
        self.draw_wheel()
        self.needle.draw()
        self.draw_button()

    def draw_wheel(self) -> None:
        for party, polygon in self.polygons.items():
            pygame.draw.polygon(self.screen, party.color, polygon)

    def draw_button(self) -> None:
        pass


if __name__ == '__main__':
    screen_size = pygame.Vector2(400, 400)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    party1 = Party('Player', 'blue', [], True)
    party2 = Party('Enemy1', 'red', [], False)
    party3 = Party('Enemy2', 'green', [], False)
    party4 = Party('Enemy3', 'yellow', [], False)
    spin_wheel = SpinningWheel(screen, screen.get_rect(), 100)
    spin_wheel.set_parties([party1, party2, party3, party4])

    running = True

    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spin_wheel.start()


            if event.type == pygame.QUIT:
                running = False

        spin_wheel.update()

        spin_wheel.draw()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
