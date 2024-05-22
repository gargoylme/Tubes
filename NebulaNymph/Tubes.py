import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Display dimensions
display_width = 480
display_height = 600

class Colors:
    purple = (153, 51, 255)
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)

class Images:
    def __init__(self):
        try:
            self.icon = pygame.image.load('icon.png')
            self.player = pygame.image.load("buzz.png")
            self.meteor = pygame.image.load("meteor.png")
            self.rock = pygame.image.load("bebatuan.png")
            self.ufo = pygame.image.load("ufo.png")
            self.bg = pygame.image.load("bg.png")
            self.crash = pygame.image.load("crash.png")
            self.bgs = pygame.image.load("pinggir.png")
        except pygame.error as e:
            print(f"Error loading resources: {e}")
            pygame.quit()
            quit()

        self.bg = self.scale_background(self.bg)
        self.bgs = self.scale_background(self.bgs)

    @staticmethod
    def scale_background(img):
        return pygame.transform.scale(img, (display_width, display_height))

class Text:
    @staticmethod
    def render(text, size, color):
        font = pygame.font.Font("freesansbold.ttf", size)
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    @staticmethod
    def message_display(game_display, text, size, x, y):
        text_surface, text_rectangle = Text.render(text, size, Colors.purple)
        text_rectangle.center = (x, y)
        game_display.blit(text_surface, text_rectangle)

class Player:
    def __init__(self, image):
        self.image = image
        self.width = 50
        self.height = 100
        self.x = (display_width / 2) - (self.width / 2)
        self.y = display_height - self.height
        self.x_change = 0

    def draw(self, game_display):
        game_display.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.x_change

class Obstacle:
    def __init__(self, image, x, y, width, height, speed):
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self, game_display):
        game_display.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.speed

def game_loop():
    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(-1)

    images = Images()
    player = Player(images.player)
    road_width = 350
    road_start_x = (display_width // 2) - (road_width // 2)
    road_end_x = (display_width // 2) + (road_width // 2)
    
    def create_random_obstacle():
        thing_startx = random.randrange(road_start_x, road_end_x - player.width)
        return Obstacle(random.choice([images.meteor, images.rock, images.ufo]), thing_startx, -600, 50, 100, 10)

    current_obstacle = create_random_obstacle()

    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Nebula Nymph")
    pygame.display.set_icon(images.icon)
    clock = pygame.time.Clock()

    score = 0
    bg_y1 = 0
    bg_y2 = -display_height
    bg_speed = 10
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_change = -10
                elif event.key == pygame.K_RIGHT:
                    player.x_change = 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0

        player.move()

        if player.x < road_start_x or player.x > road_end_x - player.width:
            crash_x = player.x
            crash_y = player.y
            game_display.blit(images.crash, (crash_x, crash_y))
            Text.message_display(game_display, "GAME OVER", 40, display_width / 2, display_height / 2)
            pygame.display.update()
            time.sleep(2)
            game_loop()

        if player.y <= display_height - player.height:
            player.y += 5

        if player.y > display_height - player.height:
            player.y = display_height - player.height

        if player.y < current_obstacle.y + current_obstacle.height:
            if (current_obstacle.x < player.x < current_obstacle.x + current_obstacle.width) or (
                    current_obstacle.x < player.x + player.width < current_obstacle.x + current_obstacle.width):
                crash_x = player.x
                crash_y = player.y
                game_display.blit(images.crash, (crash_x, crash_y))
                Text.message_display(game_display, "GAME OVER", 40, display_width / 2, display_height / 2)
                pygame.display.update()
                time.sleep(2)
                game_loop()

        game_display.fill(Colors.green)
        game_display.blit(images.bgs, (0, 0))
        game_display.blit(images.bgs, (display_width - images.bgs.get_width(), 0))

        game_display.blit(images.bg, (0, bg_y1))
        game_display.blit(images.bg, (0, bg_y2))

        player.draw(game_display)
        current_obstacle.draw(game_display)

        Text.message_display(game_display, f"Score: {score}", 45, 90, 40)
        score += 1
        current_obstacle.move()

        if current_obstacle.y > display_height:
            current_obstacle = create_random_obstacle()

        bg_y1 += bg_speed
        bg_y2 += bg_speed

        if bg_y1 >= display_height:
            bg_y1 = -display_height

        if bg_y2 >= display_height:
            bg_y2 = -display_height

        game_display.blit(images.bgs, (0, 0))
        game_display.blit(images.bgs, (display_width - images.bgs.get_width(), 0))

        pygame.display.update()
        clock.tick(60)

game_loop()
