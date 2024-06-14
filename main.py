import os
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

TILE_NUMBER_COLORS = {
    2: (191, 189, 147),
    4: (191, 173, 124),
    8: (191, 162, 84),
    16: (201, 159, 44),
    32: (252, 186, 3),
    64: (219, 127, 22),
    128: (199, 105, 62),
    256: (214, 86, 28),
    512: (252, 80, 3),
    1024: (196, 57, 29),
    2048: (250, 0, 0)
}


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
        self.font = pygame.font.Font('Roboto-Regular.ttf', 50)
        self.score_font = pygame.font.Font('Roboto-Regular.ttf', 30)

        # Rows and cols
        self.game_values = [[0 for _ in range(TILE_ROWS)] for _ in range(TILE_COLS)]
        # FPS
        self.clock = pygame.time.Clock()

        # Score
        self.score = 0
        self.best_score = 0

        # Start game logic
        self.start_game = False

        # Space text
        self.font_size = 30
        self.size_direction = 1
        self.max_font = 100
        self.min_font = 20

    def run_game(self):
        """Main while loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        self.start_game = True
                        self.game_values = [[0 for _ in range(TILE_ROWS)] for _ in range(TILE_COLS)]
                        #  Generate start number
                        self.generate_random_tile_number()
                        self.score = 0
                    elif event.key == pygame.K_RIGHT and self.start_game:
                        self.move_number_tile("right")
                        self.generate_random_tile_number(1)
                    elif event.key == pygame.K_LEFT and self.start_game:
                        self.move_number_tile("left")
                        self.generate_random_tile_number(1)
                    elif event.key == pygame.K_UP and self.start_game:
                        self.move_number_tile("up")
                        self.generate_random_tile_number(1)
                    elif event.key == pygame.K_DOWN and self.start_game:
                        self.move_number_tile("down")
                        self.generate_random_tile_number(1)

            if not self.start_game:
                self.font_size += self.size_direction

            self.save_score()
            self.show_screen()

    def generate_random_tile_number(self, number=2):
        """Generate two random tiles with numbers"""
        for i in range(number):
            self.generate_random()

    def move_right(self, max_index, row):
        """Check movement to the right"""
        self.merge_number_tiles(row, max_index)
        self.check_zero_index_value(row)
        self.merge_number_tiles(row, max_index)

    def move_left(self, row):
        """Check movement to the left"""
        row.reverse()
        self.move_right(3, row)
        row.reverse()

    def move_up(self):
        """Check movement to the top"""
        self.transpose_rows()
        for row in self.game_values:
            self.move_left(row)
        self.transpose_rows()

    def move_down(self, max_index):
        """Check movement to the bottom"""
        self.transpose_rows()
        for row in self.game_values:
            self.move_right(max_index, row)
        self.transpose_rows()

    def transpose_rows(self):
        """Transpose rows"""
        self.game_values = [list(row) for row in zip(*self.game_values)]

    def merge_number_tiles(self, row, max_index):
        """Merges two tiles if they are equal and doesn't merge if nor equals"""
        for i in range(len(row) - 1):
            if row[i] == row[i + 1] and i != max_index and row[i] != 0:
                row[i + 1] = row[i] + row[i]
                row[i] = 0
            if row[i] == row[i + 1] and i + 1 == max_index and row[i] != 0:
                row[i + 1] = row[i] + row[i]
                row[i] = 0
            if row[i + 1] == 0 and row[i] != max_index:
                row[i + 1] = row[i]
                row[i] = 0
            elif row[i + 1] != row[i] and i != max_index and row[i] != 0:
                row[i + 1] = row[i + 1]
                row[i] = row[i]

    def check_zero_index_value(self, row):
        """Check if the next number doesn't have zero value"""
        for i in range(len(row) - 1):
            if row[i + 1] == 0:
                row[i + 1] = row[i]
                row[i] = 0

    def move_number_tile(self, action):
        """Moves tiles with numbers"""
        # Max index
        max_index = TILE_COLS - 1
        for row in self.game_values:
            match action:
                case "right":
                    self.move_right(max_index, row)
                case "left":
                    self.move_left(row)
                case "up":
                    self.move_up()
                case "down":
                    self.move_down(max_index)

    def draw_rect_tiles(self, col, row, color):
        """Draws tiles' rects"""
        tile_rect = pygame.Rect((((TILE_SIZE[0] * col) - 40),
                                 (TILE_SIZE[1] * row) - 40),
                                (TILE_SIZE[0] - 20, TILE_SIZE[1] - 20))
        pygame.draw.rect(self.screen, color, tile_rect)

    def draw_tile_number(self, col, row, color):
        """Draws tile with number -> movable"""
        # Size to put number into a center of a rect
        size = -10 if color < 10 else -1 if color < 100 else 12 if color < 900 else 25
        # check text color
        number_color = "black" if color < 50 else "white" if color < 300 else (182, 191, 184) \
            if color < 500 else (247, 255, 249) if color < 1500 else (245, 247, 210)
        self.draw_rect_tiles(col, row, TILE_NUMBER_COLORS[color])
        number = self.font.render(f"{self.game_values[row-1][col-1]}", True, number_color)
        self.screen.blit(number, ((TILE_SIZE[0] * col) - size, (TILE_SIZE[1] * row) - 5))

    def draw_score(self):
        text = self.score_font.render(f"Score: {self.score}",
                                      True, "black")
        best_score_text = self.score_font.render(f"Best Score: {self.best_score}",
                                                True, "black")
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        best_score_rect = best_score_text.get_rect(center=(SCREEN_WIDTH // 2, 60))

        self.screen.blit(best_score_text, best_score_rect)
        self.screen.blit(text, text_rect)

    def generate_random(self):
        """Generates random numbers for tiles with start value"""
        # Check if we row has zero values
        row_col = [(j, i) for j, row in enumerate(self.game_values) for i, col in enumerate(row) if col == 0]
        # Random tuple
        if row_col:
            ran_number = random.choice(row_col)
            self.score += 1
            self.game_values[ran_number[0]][ran_number[1]] = 2
        else:
            self.start_game = False

    def draw_instructions(self):
        """Instructions for the game"""
        text = self.score_font.render(f"Use arrow buttons on the keyboard to move the tiles", True, "black")
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(text, text_rect)

    def check_win(self):
        """Check if the game is won"""
        winner = [True for row in self.game_values for i, col in enumerate(row) if col == 2048]
        if winner:
            text = self.font.render(f"You won!", True, "black")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            self.screen.blit(text, text_rect)
            self.start_game = False

    def write_score(self):
        """Write score into a file"""
        with open("score.txt", "w") as f:
            f.write(str(self.score))

    def save_score(self):
        """Reads scores and saves it"""
        if not os.path.exists(os.path.join("score.txt")):
            self.write_score()
        else:
            with open("score.txt", "r") as f:
                file = f.read()
                file_number = int(file)
                if file_number < self.score:
                    self.write_score()
                    self.best_score = self.score
                else:
                    self.best_score = file_number

    def check_lose(self):
        """Check if the game is over"""
        # Show lose game
        text = self.font.render(f"You lose!", True, "black")
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(text, text_rect)

    def draw_tiles(self):
        """Draw tiles"""
        for row in range(1, TILE_ROWS+1):
            for col in range(1, TILE_COLS+1):
                self.draw_rect_tiles(col, row, TILE_COLOR)

    def show_space_start_game(self):
        """Show the bouncing text how to start the game"""
        if self.font_size >= self.max_font or self.font_size <= self.min_font:
            self.size_direction = -self.size_direction
        font = pygame.font.Font('Roboto-Regular.ttf', self.font_size)
        text = font.render(f"Click 'Space' to start the game", True, "black")
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.screen.blit(text, text_rect)

    def show_screen(self):
        """Show screen's objects"""
        self.clock.tick(60)
        # Show screen, color
        self.screen.fill(SCREEN_COLOR)

        # score
        self.draw_score()

        # Draw a board
        pygame.draw.rect(self.screen, GAME_BOARD_COLOR, self.board_rect,
                         border_radius=5)
        # Tiles
        self.draw_tiles()

        # Draw tiles with numbers
        for i, row in enumerate(self.game_values):
            for j, col in enumerate(row):
                if col != 0:
                    self.draw_tile_number(j+1, i+1, col)

        # Draw space start game
        if not self.start_game:
            self.show_space_start_game()
            if self.score != 0:
                self.check_lose()

        self.check_win()

        self.draw_instructions()

        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    try:
        game.run_game()
    except Exception as e:
        print(e)
