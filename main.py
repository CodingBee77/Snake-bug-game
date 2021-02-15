import pygame
import time
from pygame.locals import *
import time
import random

SIZE = 30
BACKGROUND_COLOR = (53, 55, 61)
SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 480


class Menu:
    button_width = 250
    button_height = 100
    button_easy = None
    button_medium = None
    button_hard = None

    def __init__(self, surface, start_game_method_reference):
        self.surface = surface
        self.start_game_method_reference = start_game_method_reference

    def run(self):
        self.render_background()
        self.render_buttons()
        pygame.display.flip()
        difficulty = ''
        running = True
        while running:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_easy.is_over(pos):
                        difficulty = 'easy'
                        running = False
                    elif self.button_medium.is_over(pos):
                        difficulty = 'medium'
                        running = False
                    elif self.button_hard.is_over(pos):
                        difficulty = 'hard'
                        running = False
                elif event.type == QUIT:
                    running = False
                    pygame.quit()
                    quit()
        self.start_game_method_reference(difficulty)

    def render_background(self):
        bg = pygame.image.load("resources/menu_bg.jpg")
        self.surface.blit(bg, (0, 0))

    def render_buttons(self):
        y_coordinate = (SCREEN_HEIGHT - 3 * self.button_height) / 4
        x_coordinate = (SCREEN_WIDTH - self.button_width) / 2
        self.button_easy = Button((0, 102, 0), x_coordinate, y_coordinate, self.button_width, self.button_height,
                                  'Easy', self.surface)
        self.button_medium = Button((255, 255, 0), x_coordinate, 2 * y_coordinate + self.button_height,
                                    self.button_width, self.button_height, 'Medium', self.surface)
        self.button_hard = Button((255, 0, 0), x_coordinate, 3 * y_coordinate + 2 * self.button_height,
                                  self.button_width, self.button_height, 'Hard', self.surface)
        self.button_easy.draw()
        self.button_medium.draw()
        self.button_hard.draw()


class Application:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Eats A Bug Game")
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def run(self):
        menu = Menu(self.surface, start_game_method_reference=self.start_game)
        menu.run()

    def start_game(self, difficulty):
        print(difficulty)
        Game(self.surface, difficulty).run()


class Button:
    def __init__(self, color, x, y, width, height, text='', surface=None):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            self.surface.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


class Bug:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/bug.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(
            self):  # generate a random coordinates for a bug position on a screen : at will be a number divisible by bug size
        self.x = random.randint(1, 34) * SIZE
        self.y = random.randint(1, 15) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):

        for i in range(self.length - 1, 0, -1):  # each previous block goes on position of the following
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self, surface, difficulty):
        self.play_background_music()
        self.surface = surface
        self.surface.fill((53, 55, 61))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.bug = Bug(self.surface)
        self.bug.draw()
        if difficulty == 'easy':
            self.speed = 0.2
        elif difficulty == 'medium':
            self.speed = 0.1
        elif difficulty == 'hard':
            self.speed = 0.05
        else:
            self.speed = 0.1

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music.ogg")
        pygame.mixer.music.play(-1)

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.ogg")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def inbounds(self):
        return 0 <= self.snake.x[0] <= self.surface.get_width() and 0 <= self.snake.y[0] <= self.surface.get_height()

    def outbounds_right(self):
        return self.is_right_border() and self.snake.direction == 'right'

    def is_right_border(self):
        return self.snake.x[0] == (self.surface.get_width() - SIZE)

    def outbounds_left(self):
        return self.is_left_border() and self.snake.direction == 'left'

    def is_left_border(self):
        return self.snake.x[0] == 0

    def outbounds_top(self):
        return self.is_top_border() and self.snake.direction == 'up'

    def is_top_border(self):
        return self.snake.y[0] == 0

    def outbounds_bottom(self):
        return self.is_bottom_border() and self.snake.direction == 'down'

    def is_bottom_border(self):
        return self.snake.y[0] == (self.surface.get_height() - SIZE)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.bug.draw()
        self.display_score()
        pygame.display.flip()

        # snake coliding with bug
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.bug.x, self.bug.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.bug.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise Exception()

        if self.outbounds_right():
            if self.is_bottom_border():
                self.snake.move_up()
            else:
                self.snake.move_down()
        elif self.outbounds_left():
            if self.is_bottom_border():
                self.snake.move_up()
            else:
                self.snake.move_down()
        elif self.outbounds_top():
            if self.is_left_border():
                self.snake.move_right()
            else:
                self.snake.move_left()
        elif self.outbounds_bottom():
            if self.is_left_border():
                self.snake.move_right()
            else:
                self.snake.move_left()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (900, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game over ! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.bug = Bug(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(self.speed)


if __name__ == "__main__":
    app = Application()
    app.run()
