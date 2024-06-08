import pygame
import sys

# Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_COLOR = (179, 179, 179)

# GAME board settings
GAME_BOARD_SIZE = (600, 600)
GAME_BOARD_COLOR = (117, 108, 88)

# Tiles' settings
TILE_COLS = 4
TILE_ROWS = 4
TILE_COLOR = (176, 164, 139)
TILE_SIZE = (GAME_BOARD_SIZE[0] // TILE_COLS - 10, GAME_BOARD_SIZE[1] // TILE_ROWS - 10)


class Game:
    def __init__(self):
        pygame.init()
        # Screen settings
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2048")

        # Board
        self.board_rect = pygame.FRect((SCREEN_WIDTH//2 - GAME_BOARD_SIZE[0] // 2,
                                        SCREEN_HEIGHT // 2 - GAME_BOARD_SIZE[1] // 2),
                                       (GAME_BOARD_SIZE[0], GAME_BOARD_SIZE[1]))


        # FPS
        self.clock = pygame.time.Clock()

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.show_screen()

    def show_screen(self):
        self.clock.tick(60)
        # Show screen, color
        self.screen.fill(SCREEN_COLOR)

        # Draw a board
        pygame.draw.rect(self.screen, GAME_BOARD_COLOR, self.board_rect, border_radius=2)
        # Tiles
        for row in range(1, TILE_ROWS+1):
            for col in range(1, TILE_COLS+1):
                tile_rect = pygame.Rect((TILE_SIZE[0] * col, TILE_SIZE[1] * row),
                                        (TILE_SIZE[0] - 10, TILE_SIZE[1] - 10))
                pygame.draw.rect(self.screen, TILE_COLOR, tile_rect)


        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run_game()
