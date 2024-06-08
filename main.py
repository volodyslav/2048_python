import pygame
import sys
import random

# Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_COLOR = (179, 179, 179)

# GAME board settings
GAME_BOARD_SIZE = (600, 600)
GAME_BOARD_COLOR = (117, 112, 106)

# Tiles' settings
TILE_COLS = 4
TILE_ROWS = 4
TILE_COLOR = (163, 157, 149)
TILE_SIZE = (GAME_BOARD_SIZE[0] // TILE_COLS, GAME_BOARD_SIZE[1] // TILE_ROWS)


class Game:
    def __init__(self):
        pygame.init()
        # Screen settings
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2048")

        # Board
        self.board_rect = pygame.FRect((SCREEN_WIDTH//2 - GAME_BOARD_SIZE[0] // 2,
                                        SCREEN_HEIGHT // 2 - GAME_BOARD_SIZE[1] // 2),
                                       GAME_BOARD_SIZE)

        # Text
        self.font = pygame.font.SysFont('Arial', 60)

        # Rows and cols
        self.game_values = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        # Random col and row
        self.ran_col = random.randint(1, TILE_COLS)
        self.ran_row = random.randint(1, TILE_ROWS)

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

    def draw_tile_number(self, col, row):
        """Draws tile with number -> movable"""
        tile_rect = pygame.Rect((((TILE_SIZE[0] * col) - 40),
                                 (TILE_SIZE[1] * row) - 40),
                                (TILE_SIZE[0] - 20, TILE_SIZE[1] - 20))
        number = self.font.render(f"{2}", False, (61, 61, 56))
        pygame.draw.rect(self.screen, (191, 189, 147), tile_rect)
        self.screen.blit(number, ((TILE_SIZE[0] * col) + 10, (TILE_SIZE[1] * row) - 10))

    def show_screen(self):
        """Show screen's objects"""
        self.clock.tick(60)
        # Show screen, color
        self.screen.fill(SCREEN_COLOR)

        # Draw a board
        pygame.draw.rect(self.screen, GAME_BOARD_COLOR, self.board_rect,
                         border_radius=5)
        # Tiles
        for row in range(1, TILE_ROWS+1):
            for col in range(1, TILE_COLS+1):
                tile_rect = pygame.Rect((((TILE_SIZE[0] * col) - 40),
                                         (TILE_SIZE[1] * row) - 40),
                                        (TILE_SIZE[0] - 20, TILE_SIZE[1] - 20))

                pygame.draw.rect(self.screen, TILE_COLOR, tile_rect)

        # Draw tiles with numbers
        print(f"Random: {self.ran_row, self.ran_col}")
        print(f"all values {self.game_values}")
        self.draw_tile_number(self.ran_col, self.ran_row)
        self.game_values[self.ran_row - 1][self.ran_col -1] = 2

        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run_game()
