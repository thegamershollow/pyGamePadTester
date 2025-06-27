import pygame
import sys

def init_joysticks():
    pygame.joystick.init()
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
        print(f"Initialized Joystick {i}: {joystick.get_name()}")
    return joysticks

def print_joystick_state(joystick):
    print(f"\n[{joystick.get_name()}]")

    # Axes
    for i in range(joystick.get_numaxes()):
        axis = joystick.get_axis(i)
        print(f"  Axis {i}: {axis:.3f}")

    # Buttons
    for i in range(joystick.get_numbuttons()):
        button = joystick.get_button(i)
        print(f"  Button {i}: {'Pressed' if button else 'Released'}")

    # Hats (D-pad)
    for i in range(joystick.get_numhats()):
        hat = joystick.get_hat(i)
        print(f"  Hat {i}: {hat}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Cross-Platform Gamepad Tester")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 30)
    joysticks = init_joysticks()

    if not joysticks:
        print("No joysticks detected. Please connect a controller.")
        pygame.quit()
        sys.exit()

    while True:
        screen.fill((30, 30, 30))
        y = 20

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        for joystick in joysticks:
            lines = [
                f"Gamepad: {joystick.get_name()}",
                f"Axes: {[f'{joystick.get_axis(i):.2f}' for i in range(joystick.get_numaxes())]}",
                f"Buttons: {[joystick.get_button(i) for i in range(joystick.get_numbuttons())]}",
                f"Hats: {[joystick.get_hat(i) for i in range(joystick.get_numhats())]}"
            ]

            for line in lines:
                text = font.render(line, True, (200, 200, 200))
                screen.blit(text, (20, y))
                y += 30
            y += 10  # space between controllers

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
