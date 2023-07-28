import pygame
import os, sys
import random
os.system('cls')
pygame.init()
################################################################################
#                           BASIC SETTINGS                                     #
################################################################################
SCREEN = WIDTH, HEIGHT = 720, 460
FPS = 20
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (165, 42, 42)
PURPLE = (75, 0, 130)
################################################################################
#                           SOUND                                              #
################################################################################
#background_sound = pygame.mixer.Sound('sound/background_music.mp3')
game_over_sound = pygame.mixer.Sound('sound/game_over.mp3')
################################################################################
#                           BACKGROUND                                         #
################################################################################

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 720
        self.screen_height = 460
        self.fps = pygame.time.Clock()
        self.score = 0
        self.game_over_sound = pygame.mixer.Sound('sound/game_over.mp3')
        self.apple_img = None
        self.background_img = None
        pygame.mixer.music.load('sound/background_music.mp3')
        pygame.mixer.music.play(1)

    def init_and_check_for_errors(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print("[X] Error initializing pygame: %s" % check_errors[1]) # {error} | try: expected: ДОПИСАТЬ
            sys.exit()
        else:
            print("[+] Initialized successfully")

    def load_images(self):
        background = {
            'Bg1': pygame.image.load('background/background1.png').convert(),
            'Bg2': pygame.image.load('background/background2.png').convert(),
            'Bg3': pygame.image.load('background/background3.png').convert(),
            'Bg4': pygame.image.load('background/background4.png').convert(),
            'Bg5': pygame.image.load('background/background5.png').convert()
        }
        self.background_img = background['Bg1'] # Можно изменить фон [Bg1, Bg2, Bg3, Bg4, Bg5]

    def event_loop(self, change_to):
        for event in pygame.event.get():
           if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):                   
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'): 
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'): 
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'): 
                    change_to = "DOWN"
                elif event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    sys.exit()
        return change_to
    
    def refresh_screen(self):
        pygame.display.flip()
        game.fps.tick(15)

    def set_surface_and_title(self):
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake')
        self.load_images()

    def show_score(self, choice = 1):
        s_font = pygame.font.Font('font/Montserrat.ttf', 20)
        s_surf = s_font.render('Score: {0}'.format(self.score), True, WHITE)
        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (80, 10)
        else:
            s_rect.midtop = (360, 120)
        self.play_surface.blit(s_surf, s_rect)

    def draw_objects(self):
        self.play_surface.blit(self.background_img, (0, 0))
        self.show_score()
        pygame.display.flip()

    def game_over(self):
        go_font = pygame.font.Font('font/Montserrat.ttf', 50)
        go_surf = go_font.render('GAME OVER', True, RED)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        alpha_value = 0 
        while alpha_value < 255:
            go_surf.set_alpha(alpha_value)
            self.play_surface.blit(self.background_img, (0, 0))
            self.play_surface.blit(go_surf, go_rect)
            self.show_score(0)
            pygame.display.flip()
            pygame.time.delay(30)
            alpha_value += 5
        pygame.time.delay(1000)
        pygame.mixer.music.stop()
        self.game_over_sound.play()
        pygame.time.delay(3000)
        sys.exit()

class Snake:
    def __init__(self, snake_color):
        self.snake_head_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        self.direction = "RIGHT"
        self.change_to = self.direction

    def validate_direction_and_change(self):
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and self.snake_head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, int(screen_width/10)) * 10, random.randrange(1, int(screen_height/10)) * 10]
            score += 1
        else:
            self.snake_body.pop()
        return score, food_pos
    
    def draw_snake(self, play_surface):
        play_surface.blit(game.background_img, (0, 0))
        for pos in self.snake_body:
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                pos[0], pos[1], 10, 10))
    
    def check_for_boundaries(self, game_over, screen_width, screen_height):
        if any((self.snake_head_pos[0] > screen_width-10
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height-10
                or self.snake_head_pos[1] < 0)):
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and block[1] == self.snake_head_pos[1]):
                game_over()

class Food:
    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, int(screen_width/10)) * 10, random.randrange(1, int(screen_height/10)) * 10]

    def draw_food(self, play_surface):
        pygame.draw.rect(play_surface, self.food_color, pygame.Rect(self.food_pos[0], self.food_pos[1], self.food_size_x, self.food_size_y))
        
if __name__ == "__main__":       
    pygame.init()
    screen_width = 720
    screen_height = 460 
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Snake')
    game = Game()
    game.load_images()
    snake = Snake(GREEN)
    food = Food(BROWN, game.screen_width, game.screen_height)
    game.init_and_check_for_errors()
    game.set_surface_and_title()
    while True:
        snake.change_to = game.event_loop(snake.change_to)
        snake.validate_direction_and_change()
        snake.change_head_position()
        game.score, food.food_pos = snake.snake_body_mechanism(game.score, food.food_pos, game.screen_width, game.screen_height)
        snake.draw_snake(game.play_surface)
        food.draw_food(game.play_surface)
        snake.check_for_boundaries(game.game_over, game.screen_width, game.screen_height)
        game.show_score()
        game.refresh_screen()
        game.draw_objects()