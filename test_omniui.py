import pygame

from adapters.render.pygame import PygameRenderer
from core.primitives import Color, ColorStack, IVec2, Vec2
from omniecs.world import WorldFactory

from ui.bundles import PanelLayoutBundle, RectTransformBundle, SurfaceBundle, TextVisualBundle, WidgetCoreBundle
from ui.components.behavior import Enabled
from ui.components.layout import RenderLayer, HorizontalAlignment, Transform, VerticalAlignment
from ui.components.rendering import Dirty
from ui.components.style import Background, Frame
from ui.systems.renderer_system import BackgroundRendererSystem, FrameRendererSystem, TextRendererSystem
from ui.types import TextStyleDescription
from ui.widgets import PanelBundle, TextBundle


if __name__ == '__main__':
    screen_size = pygame.Vector2(1440, 775)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    running = True

    pygame_renderer = PygameRenderer(screen)

    world = WorldFactory.create_world()
    world.register_system(BackgroundRendererSystem())
    world.register_system(FrameRendererSystem())
    world.register_system(TextRendererSystem())
    
    world.spawn(Enabled(), Dirty(), Background(ColorStack(Color(0, 120, 0))), Frame(ColorStack(Color(120, 120, 0)), 3), Transform(Vec2(100, 100), Vec2(100, 100)), RenderLayer(2))

    core = WidgetCoreBundle()
    transform = RectTransformBundle(Vec2(x=100, y=100), Vec2(x=50, y=50), layer=3)
    layout = PanelLayoutBundle()
    surface = SurfaceBundle(Color(0, 0, 150), Color(150, 0, 0), 2)

    panel = PanelBundle(core, transform, layout, surface)
    world.spawn(*panel.components())

    surface = SurfaceBundle(Color(0, 0, 150), Color(150, 0, 0), 2)
    text_style = TextStyleDescription('arial', 16, color=Color(0, 100, 100))

    visual = TextVisualBundle('text', text_style, horizontal_spacing=10)
    visual2 = TextVisualBundle('text', text_style, HorizontalAlignment.center)
    visual3 = TextVisualBundle('text', text_style, HorizontalAlignment.right)
    visual4 = TextVisualBundle('text', text_style, vertical_alignment=VerticalAlignment.middle, vertical_spacing=10)
    visual5 = TextVisualBundle('text', text_style, HorizontalAlignment.center, VerticalAlignment.middle)
    visual6 = TextVisualBundle('text', text_style, HorizontalAlignment.right, VerticalAlignment.middle, vertical_spacing=-10)
    visual7 = TextVisualBundle('text', text_style, vertical_alignment=VerticalAlignment.bottom, horizontal_spacing=-10)
    visual8 = TextVisualBundle('text', text_style, HorizontalAlignment.center, VerticalAlignment.bottom)
    visual9 = TextVisualBundle('text', text_style, HorizontalAlignment.right, VerticalAlignment.bottom)
    transform = RectTransformBundle(Vec2(x=300, y=300), Vec2(x=50, y=50), layer=3)
    transform2 = RectTransformBundle(Vec2(x=400, y=300), Vec2(x=50, y=50), layer=3)
    transform3 = RectTransformBundle(Vec2(x=500, y=300), Vec2(x=50, y=50), layer=3)
    transform4 = RectTransformBundle(Vec2(x=300, y=400), Vec2(x=50, y=50), layer=3)
    transform5 = RectTransformBundle(Vec2(x=400, y=400), Vec2(x=50, y=50), layer=3)
    transform6 = RectTransformBundle(Vec2(x=500, y=400), Vec2(x=50, y=50), layer=3)
    transform7 = RectTransformBundle(Vec2(x=300, y=500), Vec2(x=50, y=50), layer=3)
    transform8 = RectTransformBundle(Vec2(x=400, y=500), Vec2(x=50, y=50), layer=3)
    transform9 = RectTransformBundle(Vec2(x=500, y=500), Vec2(x=50, y=50), layer=3)
    text = TextBundle(WidgetCoreBundle(), visual, transform, surface)
    text2 = TextBundle(WidgetCoreBundle(), visual2, transform2, surface)
    text3 = TextBundle(WidgetCoreBundle(), visual3, transform3, surface)
    text4 = TextBundle(WidgetCoreBundle(), visual4, transform4, surface)
    text5 = TextBundle(WidgetCoreBundle(), visual5, transform5, surface)
    text6 = TextBundle(WidgetCoreBundle(), visual6, transform6, surface)
    text7 = TextBundle(WidgetCoreBundle(), visual7, transform7, surface)
    text8 = TextBundle(WidgetCoreBundle(), visual8, transform8, surface)
    text9 = TextBundle(WidgetCoreBundle(), visual9, transform9, surface)

    world.spawn(*text.components())
    world.spawn(*text2.components())
    world.spawn(*text3.components())
    world.spawn(*text4.components())
    world.spawn(*text5.components())
    world.spawn(*text6.components())
    world.spawn(*text7.components())
    world.spawn(*text8.components())
    world.spawn(*text9.components())

    while running:
        for event in pygame.event.get():

            # print(event)
            # print(pygame.BUTTON_LEFT, pygame.BUTTON_MIDDLE, pygame.BUTTON_RIGHT)

            if event.type == pygame.MOUSEMOTION:
                position = IVec2(*event.pos)
                #print(position)

            if event.type == pygame.QUIT:
                running = False

        delta_time = clock.get_time()

        world.execute(delta_time)

        pygame_renderer.render(world.get_draw_commands())

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
