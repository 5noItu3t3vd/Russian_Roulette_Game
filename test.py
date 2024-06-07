import pygame
import sys
import time

def fade_in(screen, color=(0, 0, 0), duration=1):
    fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_surface.fill(color)
    for alpha in range(0, 256):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(int(duration * 1000 / 255))

def fade_out(screen, color=(0, 0, 0), duration=1):
    fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_surface.fill(color)
    for alpha in range(255, -1, -1):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(int(duration * 1000 / 255))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Fade In and Fade Out Example")

    # Fill the screen with a color to see the fade effect
    screen.fill((255, 255, 255))
    pygame.display.update()
    time.sleep(1)  # Wait to see the initial color

    # Perform a fade in
    fade_in(screen, duration=2)
    time.sleep(1)  # Wait to see the fade-in effect

    # Change screen color to see the fade-out effect clearly
    screen.fill((100, 100, 100))
    pygame.display.update()
    time.sleep(1)

    # Perform a fade out
    fade_out(screen, duration=2)
    time.sleep(1)  # Wait to see the fade-out effect

    # Main event loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

main()
