"""Functional programming pygame chess game"""

import pygame
import cytoolz

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])


def run_game():
    """Main game loop"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        # Flip the display
        pygame.display.flip()


def check_events():
    """Check for events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True


if __name__ == "__main__":
    run_game()
