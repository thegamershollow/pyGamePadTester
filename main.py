import pygame
import sys

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("🕹️ Python Gamepad Tester")
font = pygame.font.SysFont("consolas", 20)
clock = pygame.time.Clock()

BG_COLOR = (15, 15, 20)
TEXT_COLOR = (240, 240, 240)
PANEL_COLOR = (40, 40, 60)
ACCENT_COLOR = (100, 180, 250)

joysticks = []

def init_joysticks():
    global joysticks
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        joy.init()
        joysticks.append(joy)
        print(f"[+] Initialized {joy.get_name()}")

def draw_text(text, x, y, color=TEXT_COLOR):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))
    return y + surf.get_height() + 5

def draw_joystick_panel(joy, x, y, width=360):
    pygame.draw.rect(screen, PANEL_COLOR, (x, y, width, 260), border_radius=10)
    pygame.draw.rect(screen, ACCENT_COLOR, (x, y, width, 260), 2, border_radius=10)

    padding = 10
    text_y = y + padding
    name = joy.get_name()
    draw_text(f"🎮 {name}", x + padding, text_y)

    try:
        uid_text = f"USB ID: {joy.get_guid()[0:4]}:{joy.get_guid()[4:8]}"
        draw_text(uid_text, x + padding, text_y + 25)
    except Exception:
        draw_text("USB ID: N/A", x + padding, text_y + 25)

    # Draw axes visually
    cx = x + width // 2
    cy = y + 130
    radius = 40

    if joy.get_numaxes() >= 2:
        ax = joy.get_axis(0)
        ay = joy.get_axis(1)
        joy_x = cx + int(ax * radius)
        joy_y = cy + int(ay * radius)

        # Outer circle
        pygame.draw.circle(screen, (100, 100, 100), (cx, cy), radius, 2)
        # Inner dot
        pygame.draw.circle(screen, ACCENT_COLOR, (joy_x, joy_y), 8)

    # Triggers (LT/RT as axis 2 and 5 commonly)
    tx = x + 20
    ty = y + 200
    tw = width - 40
    th = 12

    def draw_trigger(axis_index, label):
        if joy.get_numaxes() > axis_index:
            val = (joy.get_axis(axis_index) + 1) / 2  # Normalize to [0, 1]
            fill_w = int(tw * val)
            pygame.draw.rect(screen, (60, 60, 60), (tx, ty, tw, th))
            pygame.draw.rect(screen, ACCENT_COLOR, (tx, ty, fill_w, th))
            draw_text(f"{label}: {val:.2f}", tx, ty + 15)
            return ty + 35
        return ty

    ty = draw_trigger(2, "LT")
    ty = draw_trigger(5, "RT")

def main():
    init_joysticks()

    while True:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.JOYDEVICEADDED:
                init_joysticks()
            elif event.type == pygame.JOYDEVICEREMOVED:
                init_joysticks()

        if not joysticks:
            draw_text("No gamepad connected. Plug one in...", 30, 30)
        else:
            margin = 20
            panel_w = 360
            x = margin
            y = margin
            for joy in joysticks:
                draw_joystick_panel(joy, x, y, panel_w)
                x += panel_w + margin
                if x + panel_w > screen.get_width():
                    x = margin
                    y += 280

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
