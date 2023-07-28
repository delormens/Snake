import os, sys
import pygame
import random
import pygame_gui
os.system('cls')

################################################################################
#                           НАСТРОЙКИ                                          #
################################################################################
SCREEN = WIDTH, HEIGHT = 720, 460
FPS = 30
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (165, 42, 42)
PURPLE = (75, 0, 130)

class Game():
    def __init__(self):
        self.screen_width = 720
        self.screen_height = 460
        self.fps = pygame.time.Clock()
        self.score = 0
        self.game_over_sound = pygame.mixer.Sound('sound/game_over.mp3')
        self.background_img = None
        pygame.mixer.music.load('sound/background_music.mp3')
        pygame.mixer.music.play(-1)

    def load_images(self):
        apple_img_original = pygame.image.load('img/apple.png').convert_alpha()
        apple_img_scaled = pygame.transform.scale(apple_img_original, (20, 20))
        self.apple_img = apple_img_scaled
        self.background_img = pygame.image.load('background/background1.png').convert()

    def init_and_check_errors(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print("[X] Error initializing pygame")
            sys.exit()
        else:
            print("[+] Initialized successfully")
        
    def surface(self):
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake')
        self.load_images()

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

    def change_fps(self):
        pygame.display.flip()
        self.fps.tick(20)

    def show_score(self, choice=1):
        s_font = pygame.font.Font('font/Montserrat.ttf', 20)
        s_surf = s_font.render('Score: {0}'.format(self.score), True, WHITE)
        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (80, 10)
        else:
            s_rect.midtop = (360, 120)
        self.play_surface.blit(s_surf, s_rect)

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
            pygame.time.delay(50)
            alpha_value += 5
        pygame.time.delay(1000)
        pygame.mixer.music.stop()
        self.game_over_sound.play()
        pygame.time.delay(3000)
        sys.exit()

    def change_background(self, image_path):
        self.background_img = pygame.image.load(image_path).convert()
        
    def draw_objects(self, snake, apple_pos):
        self.play_surface.blit(self.background_img, (0, 0))
        for pos in snake.snake_body:
            pygame.draw.rect(self.play_surface, snake.snake_color, pygame.Rect(pos[0], pos[1], 10, 10))
        self.play_surface.blit(self.apple_img, (apple_pos[0], apple_pos[1]))
        self.show_score()
        pygame.display.flip()

class Snake():
    def __init__(self, snake_color):
        self.snake_head = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        self.dir = "RIGHT"
        self.change_to = self.dir

    def validate_change(self, new_direction):
        if new_direction == "RIGHT" and not self.dir == "LEFT":
            self.dir = "RIGHT"
        if new_direction == "LEFT" and not self.dir == "RIGHT":
            self.dir = "LEFT"
        if new_direction == "UP" and not self.dir == "DOWN":
            self.dir = "UP"
        if new_direction == "DOWN" and not self.dir == "UP":
            self.dir = "DOWN"

    def move(self):
        if self.dir == "RIGHT":
            self.snake_head[0] += 10
        if self.dir == "LEFT":
            self.snake_head[0] -= 10
        if self.dir == "UP":
            self.snake_head[1] -= 10
        if self.dir == "DOWN":
            self.snake_head[1] += 10

    def check_for_collision(self):
        if self.snake_head[0] >= game.screen_width or self.snake_head[0] < 0 or \
           self.snake_head[1] >= game.screen_height or self.snake_head[1] < 0:
            return True
        for segment in self.snake_body[1:]:
            if segment[0] == self.snake_head[0] and segment[1] == self.snake_head[1]:
                return True
        return False

def main_menu():
    pygame.init()
    screen_width = 720
    screen_height = 460
    pygame.mixer.music.load('sound/background_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.image.load('background/background1.png').convert()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Snake')
    manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()))
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 150), (220, 50)),text='Start game',manager=manager)
    settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 225), (220, 50)),text='Settings',manager=manager)
    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        pygame.quit()
                        return
                    elif event.ui_element == settings_button:
                        settings_menu(screen)
            manager.process_events(event)
        manager.update(time_delta)
        screen.fill((0, 0, 0))
        manager.draw_ui(screen)
        pygame.display.flip()

def settings_menu(screen):
    manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()))
    change_background_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 150), (220, 50)),text='Change the background',manager=manager)
    disable_music_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 225), (220, 50)),text='Turn off music',manager=manager)
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 310), (220, 50)),text='Go back',manager=manager)
    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == change_background_button:
                        pass
                        #pygame.image.load('other/background.png').convert() # РЕАЛИЗОВАТЬ ИЗМЕНЕНИЕ ФОНА
                    elif event.ui_element == disable_music_button:
                        pygame.mixer.music.stop()
                    elif event.ui_element == back_button:
                        return
            manager.process_events(event)
        manager.update(time_delta)
        screen.fill((0, 0, 0))
        manager.draw_ui(screen)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen_width = 720
    screen_height = 460
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Snake')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        main_menu()
        pygame.init()
        game = Game()
        game.init_and_check_errors()
        game.surface()
        game.load_images()
        snake = Snake(GREEN)
        apple_pos = [100, 100]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        settings_menu(screen)
            game.change_fps()
            snake.change_to = game.event_loop(snake.change_to)
            snake.validate_change(snake.change_to)
            snake.move()
            if snake.snake_head == apple_pos:
                game.score += 1
                apple_pos = [random.randrange(1, int(screen_width/10)) * 10, random.randrange(1, int(screen_height/10)) * 10]
            snake.snake_body.insert(0, list(snake.snake_head))
            if snake.snake_head[0] == apple_pos[0] and snake.snake_head[1] == apple_pos[1]:
                apple_pos = [random.randrange(1, game.screen_width // 10) * 10,
                             random.randrange(1, game.screen_height // 10) * 10]
            else:
                snake.snake_body.pop()
            if snake.check_for_collision():
                game.game_over()
            game.draw_objects(snake, apple_pos)