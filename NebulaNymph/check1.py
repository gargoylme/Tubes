import pygame
import time
import random 

pygame.init()
display_width = 480
display_height = 600

purple = (153, 51, 255)
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)

buzz_width = 50
buzz_size = 100

pygame.mixer.music.load('background.wav')
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Nebula Nymph")

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

carImg = pygame.image.load("buzz.png")
meteorimg = pygame.image.load("meteor.png")
bebatuanImg = pygame.image.load("bebatuan.png")
ufoImg = pygame.image.load("ufo.png")
bgImg = pygame.image.load("bg.png")
crash_img = pygame.image.load("crash.png")
bgsImg = pygame.image.load("pinggir.png")

# Function to scale the background images
def scale_background(img):
    return pygame.transform.scale(img, (display_width, display_height))

bgImg = scale_background(bgImg)
bgsImg = scale_background(bgsImg)

def highscore(count):
    font = pygame.font.SysFont(None, 45)
    text = font.render("Score : "+str(count), True, purple )  # Mengubah warna menjadi biru
    gameDisplay.blit(text, (90 , 40))
    
def draw_things(thingx, thingy, thing):
    gameDisplay.blit(thing, (thingx, thingy))

def car(x, y):
    gameDisplay.blit(carImg, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, purple)
    return textSurface, textSurface.get_rect()

def message_display(text, size, x, y):
    font = pygame.font.Font("freesansbold.ttf", size)
    text_surface , text_rectangle = text_objects(text, font)
    text_rectangle.center = (x, y)
    gameDisplay.blit(text_surface, text_rectangle)

def crash(x, y):
    gameDisplay.blit(crash_img, (x, y))
    message_display("GAME OVER", 40, display_width/2, display_height/2)    
    pygame.display.update()
    time.sleep(2)
    gameloop() 

def gameloop():
    pygame.mixer.music.play(-1)
    bg_x1 = 0
    bg_x2 = 0
    bg_y1 = 0
    bg_y2 = -display_height
    bg_speed = 10
    bg_speed_change = 0
    car_x = ((display_width / 2) - (buzz_width / 2))
    car_y = (display_height - buzz_size)
    car_x_change = 0
    
    # Penyesuaian lebar jalan
    road_width = 350  # Lebar jalan yang diinginkan
    road_start_x =  (display_width/2) - (road_width / 2)
    road_end_x = (display_width/2) + (road_width / 2)
    
    thing_startx = random.randrange(road_start_x, road_end_x-buzz_width)
    thing_starty = -600
    thingw = 50
    thingh = 100
    thing_speed = 10
    count = 0
    
    obstacles = [(meteorimg, 0), (bebatuanImg, 0), (ufoImg, 0)]  # List semua obstakel
    current_obstacle = random.choice(obstacles)  # Pilih satu obstakel secara acak

    gameExit = False

    
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car_x_change = -10
                elif event.key == pygame.K_RIGHT:
                    car_x_change = 10
                
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_x_change = 0
            
            
        car_x += car_x_change
        
        if car_x < road_start_x or car_x > road_end_x - buzz_width:
            crash(car_x, car_y)
        
        if car_y <= 600 - buzz_size:
            car_y += 5  # Move character down
        
        if car_y > 600 - buzz_size:
            car_y = 600 - buzz_size  # Limit character's y-coordinate to 600
        
        if car_y < thing_starty + thingh:
            if car_x >= thing_startx and car_x <= thing_startx+thingw:
                crash(car_x-25, car_y-buzz_size/2)
            if car_x+buzz_width >= thing_startx and car_x+buzz_width <= thing_startx+thingw:
                crash(car_x, car_y-buzz_size/2)
            
        
        gameDisplay.fill(green) #display white background
        gameDisplay.blit(bgsImg, (0, 0))
        gameDisplay.blit(bgsImg, (display_width - bgsImg.get_width(), 0))

        gameDisplay.blit(bgImg, (bg_x1, bg_y1))
        gameDisplay.blit(bgImg, (bg_x2, bg_y2))
        
        car(car_x, car_y) #display car
        draw_things(thing_startx, thing_starty, current_obstacle[0])
        
        highscore(count)
        count += 1
        thing_starty += thing_speed
        
        if thing_starty > display_height:
            thing_startx = random.randrange(road_start_x, road_end_x-buzz_width)
            thing_starty = -200
            
            # Memilih obstakel baru secara acak setelah satu obstakel berpindah ke luar layar
            current_obstacle = random.choice(obstacles)
            
        bg_y1 += bg_speed
        bg_y2 += bg_speed
        
        if bg_y1 >= display_height:
            bg_y1 = -display_height
            
        if bg_y2 >= display_height:
            bg_y2 = -display_height
            
        # Display additional background
        gameDisplay.blit(bgsImg, (0, 0))
        gameDisplay.blit(bgsImg, (display_width - bgsImg.get_width(), 0))
        
        pygame.display.update() # update the screen
        clock.tick(60) # frame per sec
        
gameloop()
