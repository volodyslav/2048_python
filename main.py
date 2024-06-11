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
        self.game_values = [[0 for _ in range(TILE_ROWS)] for _ in range(TILE_COLS)]
        # FPS
        self.clock = pygame.time.Clock()
        #  Generate start number
        self.generate_random_tile_number()

    def run_game(self):
        """Main while loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_RIGHT:
                        self.move_number_tile("right")
                        self.generate_random_tile_number()
                    elif event.key == pygame.K_LEFT:
                        self.move_number_tile("left")
                        self.generate_random_tile_number()
                    elif event.key == pygame.K_UP:
                        self.move_number_tile("up")
                    elif event.key == pygame.K_DOWN:
                        self.move_number_tile("down")

            self.show_screen()

    def generate_random_tile_number(self):
        """Generate two random tiles with numbers"""
        for i in range(2):
            self.generate_random()

    def move_right(self, value_index, max_index, row, col, i):
        """Check movement to the right"""
        while value_index < max_index:
            if value_index == max_index:
                # Check if 0 0 0 2
                self.game_values[i][value_index] = col
            elif row[value_index] == row[value_index + 1]:
                # Check if 2 == 2
                self.game_values[i][value_index] = 0
                self.game_values[i][value_index + 1] = col + col
            elif row[value_index + 1] == 0:
                # Check if 2 0 0 2 only == 0 0 0 4
                self.game_values[i][value_index + 1] = row[value_index]
                self.game_values[i][value_index] = 0
            elif row[value_index] != row[value_index + 1]:
                # Check if 0 0 4 2
                self.game_values[i][value_index + 1] = row[value_index + 1]
                self.game_values[i][value_index] = row[value_index]
            else:
                self.game_values[i][value_index] = 0
                self.game_values[i][max_index] = col
            value_index += 1

    def move_left(self, value_index, row, col, i):
        """Check movement to the left"""
        while value_index > 0:
            if value_index == 0:
                # Check if 2 0 0 0
                self.game_values[i][value_index] = col
            elif row[value_index] == row[value_index - 1]:
                # Check if 2 == 2
                self.game_values[i][value_index] = 0
                self.game_values[i][value_index - 1] = col + col
            elif row[value_index - 1] == 0:
                # Check if 2 0 0 2 only == 4 0 0 0
                self.game_values[i][value_index - 1] = row[value_index]
                self.game_values[i][value_index] = 0
            elif row[value_index] != row[value_index - 1]:
                # Check if 4 2 0 0
                self.game_values[i][value_index] = row[value_index]
                self.game_values[i][value_index - 1] = row[value_index - 1]
            else:
                self.game_values[i][value_index] = 0
                self.game_values[i][0] = col
            value_index -= 1

    def move_up(self, row_index, col, j):
        """Check movement to the top"""
        while row_index > 0:
            if row_index == 0:
                # Check if [2] 0 0 0
                self.game_values[row_index][j] = col
            elif self.game_values[row_index][j] == self.game_values[row_index - 1][j]:
                # Check if 2 == 2
                self.game_values[row_index][j] = 0
                self.game_values[row_index - 1][j] = col + col
            elif self.game_values[row_index - 1][j] == 0:
                # Check if 2 000
                self.game_values[row_index - 1][j] = self.game_values[row_index][j]
                self.game_values[row_index][j] = 0
            row_index -= 1

    def move_down(self, row_index, col, j, max_index):
        while row_index < max_index:
            if row_index == max_index:
                # Check if 0  0 0 2
                self.game_values[row_index][j] = col
            elif self.game_values[row_index + 1][j] == 0:
                #  0 0 0 2
                self.game_values[row_index + 1][j] = self.game_values[row_index][j]
                self.game_values[row_index][j] = 0
            elif self.game_values[row_index][j] == self.game_values[row_index + 1][j]:
                # Check if 2 == 2
                self.game_values[row_index][j] = 0
                self.game_values[row_index + 1][j] = col + col
            elif self.game_values[row_index][j] == 0:
                # Check if 2 000
                self.game_values[row_index + 1][j] = self.game_values[row_index][j]
                self.game_values[row_index][j] = 0
            row_index += 1

    def move_number_tile(self, action):
        """Moves tiles with numbers"""
        # Max index
        max_index = TILE_COLS - 1
        for i, row in enumerate(self.game_values):
            for j, col in enumerate(row):
                if col != 0:
                    value_index = j
                    row_index = i
                    if action == "right":
                        self.move_right(value_index, max_index, row, col, i)
                    elif action == "left":
                        self.move_left(value_index, row, col, i)
                    elif action == "up":
                        self.move_up(row_index, col, j)
                    elif action == "down":
                        self.move_down(row_index, col, j, max_index)

    def draw_rect_tiles(self, col, row, color):
        """Draws tiles' rects"""
        tile_rect = pygame.Rect((((TILE_SIZE[0] * col) - 40),
                                 (TILE_SIZE[1] * row) - 40),
                                (TILE_SIZE[0] - 20, TILE_SIZE[1] - 20))
        pygame.draw.rect(self.screen, color, tile_rect)

    def draw_tile_number(self, col, row):
        """Draws tile with number -> movable"""
        self.draw_rect_tiles(col, row, (191, 189, 147))
        number = self.font.render(f"{self.game_values[row-1][col-1]}", False, (61, 61, 56))
        self.screen.blit(number, ((TILE_SIZE[0] * col) + 10, (TILE_SIZE[1] * row) - 10))

    def generate_random(self):
        """Generates random numbers for tiles with start 2 value"""
        ran_col = random.randint(1, TILE_COLS)
        ran_row = random.randint(1, TILE_ROWS)
        # Check if we have some value except 0
        if self.game_values[ran_row - 1][ran_col - 1] != 0:
            self.generate_random()
        else:
            self.game_values[ran_row - 1][ran_col - 1] = 2

    def draw_tiles(self):
        """Draw tiles"""
        for row in range(1, TILE_ROWS+1):
            for col in range(1, TILE_COLS+1):
                self.draw_rect_tiles(col, row, TILE_COLOR)

    def show_screen(self):
        """Show screen's objects"""
        self.clock.tick(60)
        # Show screen, color
        self.screen.fill(SCREEN_COLOR)

        # Draw a board
        pygame.draw.rect(self.screen, GAME_BOARD_COLOR, self.board_rect,
                         border_radius=5)
        # Tiles
        self.draw_tiles()

        # Draw tiles with numbers
        for i, row in enumerate(self.game_values):
            for j, col in enumerate(row):
                if col != 0:
                    self.draw_tile_number(j+1, i+1)

        #print(f"all values {self.game_values}")

        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run_game()
