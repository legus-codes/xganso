import pygame

from editor.hex_editor_controller import HexEditorController


if __name__ == '__main__':
    screen_size = pygame.Vector2(1440, 775)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    editor_ui = HexEditorController(screen)

    running = True

    while running:
        for event in pygame.event.get():

            editor_ui.handle_event(event)

            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        editor_ui.handle_key_pressed(keys)

        delta_time = clock.get_time()

        screen.fill((30, 30, 30))

        editor_ui.draw()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
