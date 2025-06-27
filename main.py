import pygame
import sys

def init_joysticks():
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
        print(f"Initialized Joystick {i}: {joystick.get_name()}")
    return joysticks

def print_joystick_data(joystick):
    return [
        f"Gamepad: {joystick.get_name()}",
        f"Axes: {[f'{joystick.get_axis(i):.2f}' for i in range(joystick.get_numaxes())]}",
        f"Buttons: {[joystick.get_button(i) for i in range(joystick.get_numbuttons())]}",
        f"Hats: {[joystick.get_hat(i) for i in range(joystick.get_numhats())]}"
    ]

def main():
    pygame.init()
    pygame.joystick.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Cross-Platform Gamepad Tester")
    font = pygame.font.SysFont(None, 30)
    clock = pygame.time.Clock()

    joysticks = init_joysticks()

    while True:
        screen.fill((30, 30, 30))
        y = 20

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.JOYDEVICEADDED:
                print("Joystick connected.")
                joysticks = init_joysticks()

            elif event.type == pygame.JOYDEVICEREMOVED:
                print("Joystick disconnected.")
                joysticks = init_joysticks()

        if not joysticks:
            text = font.render("No gamepad connected. Plug in a controller...", True, (180, 180, 180))
            screen.blit(text, (20, y))
        else:
            for joystick in joysticks:
                for line in print_joystick_data(joystick):
                    text = font.render(line, True, (200, 200, 200))
                    screen.blit(text, (20, y))
                    y += 30
                y += 10  # space between controllers

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
