import random, pygame
import sys
# pygame setup
pygame.init()


















pygame.mixer.init()
screen = pygame.display.set_mode((1100,800))
pygame.display.set_caption('NebulaNymph')
fps = pygame.time.Clock() 

# Membuat class
class Button(pygame.sprite.Sprite):
    def __init__(self,posX,posY,OnIMGpath,OffIMGpath,soundPath):
        super().__init__()
        self.OnIMG = pygame.image.load(OnIMGpath)
        self.OffIMG = pygame.image.load(OffIMGpath)
        self.rect = self.OffIMG.get_rect(topleft = (posX,posY))
        self.image = self.OnIMG
        self.sound = pygame.mixer.Sound(soundPath)
        self.soundPlayed = False
    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(self.mousePos):
            self.image = self.OnIMG
            if not self.soundPlayed:
                self.sound.play()
                self.soundPlayed = True
        else:
            self.image = self.OffIMG
            self.soundPlayed = False

buttonGO = Button(375,380,'images/menu/button START! on.png','images/menu/button START! off.png','audio/button select.mp3')
buttonEXIT = Button(375,545,'images/menu/button EXIT! on.png','images/menu/button EXIT! off.png','audio/button select.mp3')

class Player_Hitbox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Alive = True
        self.taking_damage = False
        self.HP = 255
        self.image = pygame.image.load('images/game/player_hitbox.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (210,0))
        self.berryBushCollided = False
        self.dead = False
    def update(self,posY):
        self.rect.bottom = posY-15
    
    def PlayerCollisionCheck(self,stoneSmallRect,stoneMedRect,stoneBigRect,berryBushRect):
        if self.rect.colliderect(stoneMedRect) or self.rect.colliderect(stoneSmallRect) or self.rect.colliderect(stoneBigRect) or self.rect.colliderect(berryBushRect):
            self.HP -= 3
            self.taking_damage = True
        else: self.taking_damage = False

        if self.HP <= 0:
            self.Alive = False
            self.dead = True

        if self.rect.colliderect(berryBushRect):
            self.berryBushCollided = True
        else: self.berryBushCollided = False

PlayerHitbox = Player_Hitbox()

class PlayerAnimation(pygame.sprite.Sprite):
    def __init__(self,posX,posY):
        super().__init__()
    # RUNNING ANIMATION
        self.RunAnimFrameList = []
        self.RunAnimFrameList.append(pygame.image.load('images/game/animated/player run/1.1.png').convert_alpha())
        self.RunAnimFrameList.append(pygame.image.load('images/game/animated/player run/1.2.png').convert_alpha())
        self.RunAnimFrameList.append(pygame.image.load('images/game/animated/player run/1.3.png').convert_alpha())
        self.RunAnimFrameList.append(pygame.image.load('images/game/animated/player run/1.4.png').convert_alpha())
        self.RunAnimFrameList.append(pygame.image.load('images/game/animated/player run/1.5.png').convert_alpha())
        self.RunAnimFrameList.append(pygame.image.load('images/game/animated/player run/1.6.png').convert_alpha())
        self.RunAnimFrameList.append(pygame.image.load('images/game/animated/player run/1.7.png').convert_alpha())
    # FALLING ANIMATION
        self.JumpAnimFrameList = []
        self.JumpAnimFrameList.append(pygame.image.load('images/game/animated/player fall/1.png').convert_alpha())
        self.JumpAnimFrameList.append(pygame.image.load('images/game/animated/player fall/2.png').convert_alpha())
        self.JumpAnimFrameList.append(pygame.image.load('images/game/animated/player fall/3.png').convert_alpha())
        self.JumpAnimFrameList.append(pygame.image.load('images/game/animated/player fall/4.png').convert_alpha())
        self.JumpAnimFrameList.append(pygame.image.load('images/game/animated/player fall/2.png').convert_alpha())
        self.JumpAnimFrameList.append(pygame.image.load('images/game/animated/player fall/3.png').convert_alpha())
        self.JumpAnimFrameList.append(pygame.image.load('images/game/animated/player fall/4.png').convert_alpha())
        self.JumpAnimFrameList.append(pygame.image.load('images/game/animated/player fall/2.png').convert_alpha())
        self.JumpAnimFrameList.append(pygame.image.load('images/game/animated/player fall/3.png').convert_alpha())
    # CRASH DOWN ANIMATION
        self.CrashAnimFrameList = []
        self.CrashAnimFrameList.append(pygame.image.load('images/game/animated/player crash/2.1.png').convert_alpha())
        self.CrashAnimFrameList.append(pygame.image.load('images/game/animated/player crash/2.2.png').convert_alpha())
        self.CrashAnimFrameList.append(pygame.image.load('images/game/animated/player crash/2.3.png').convert_alpha())
        self.CrashAnimFrameList.append(pygame.image.load('images/game/animated/player crash/2.4.png').convert_alpha())
        self.CrashAnimFrameList.append(pygame.image.load('images/game/animated/player crash/2.5.png').convert_alpha())
        self.CrashAnimFrameList.append(pygame.image.load('images/game/animated/player crash/2.6.png').convert_alpha())
        self.CrashAnimFrameList.append(pygame.image.load('images/game/animated/player crash/2.7.png').convert_alpha())

        self.AnimState = 'run'
        self.jumpPower = 10
        self.gravity = 0.25
        self.currentFrame = 0
        self.image = self.RunAnimFrameList[0]
        self.rect = self.image.get_rect(midbottom = (posX,posY))
       
    def jumpLanded(self):
        self.jumpPower = 10
        self.rect.bottom = 540
        self.AnimState = 'run'

    def update(self,AnimSpeed): 
        if self.AnimState == 'run':
            self.currentFrame += AnimSpeed
            if self.currentFrame >= len(self.RunAnimFrameList): self.currentFrame = 0
            self.image = self.RunAnimFrameList[int(self.currentFrame)]

        elif self.AnimState == 'jump':
            self.currentFrame += AnimSpeed
            self.jumpPower -= self.gravity
            self.rect.bottom -= self.jumpPower
            if self.rect.bottom >= 540:
                self.jumpLanded()
            if self.currentFrame >= len(self.JumpAnimFrameList): self.currentFrame = 0
            self.image = self.JumpAnimFrameList[int(self.currentFrame)]
        
        elif  self.AnimState == 'crash':
            self.currentFrame += AnimSpeed
            self.jumpPower = -12
            self.jumpPower -= self.gravity
            self.rect.bottom -= self.jumpPower
            if self.rect.bottom >= 530:
                self.jumpLanded()
            if self.currentFrame >= len(self.CrashAnimFrameList): self.currentFrame = 0
            self.image = self.CrashAnimFrameList[int(self.currentFrame)]

class ObsticleGround(pygame.sprite.Sprite):

    def __init__(self,startingX,imagePath):
        super().__init__()
        self.image = pygame.image.load(imagePath)
        self.rect = self.image.get_rect(midbottom = (startingX,540))
    
    def update(self,mapSpeed,maxRespawnX,minRespawnX,respawnBorder):
        self.rect.left -= mapSpeed
        if self.rect.left <= respawnBorder:
            self.rect.left = random.randint(minRespawnX,maxRespawnX)

class ObsticleGroundAnimated(pygame.sprite.Sprite):

    def __init__(self,startingX,framePath1,framePath2,framePath3):
        super().__init__()
        self.frameList = []
        self.frameList.append(pygame.image.load(framePath1).convert_alpha())
        self.frameList.append(pygame.image.load(framePath2).convert_alpha())
        self.frameList.append(pygame.image.load(framePath3).convert_alpha())
        self.image = self.frameList[0]
        self.currentFrame = 0
        self.animPlay = False
        self.rect = self.image.get_rect(midbottom = (startingX,540))
    
    def update(self,mapSpeed,maxRespawnX,minRespawnX,respawnBorder,animSpeed):
        self.rect.left -= mapSpeed
        if self.rect.left <= respawnBorder:
            self.rect.left = random.randint(minRespawnX,maxRespawnX)
        self.image = self.frameList[int(self.currentFrame)]
        if self.animPlay:
            if self.currentFrame < 2.6:
                self.currentFrame += animSpeed
            else:
                self.animPlay = False
        if self.rect.left > 1200:
            self.currentFrame = 0

class PlanetBoost(pygame.sprite.Sprite):
    def __init__(self, image_0_path, image_1_path):
        super().__init__()
        self.image_0 = pygame.image.load(image_0_path)
        self.image_1 = pygame.image.load(image_1_path)
        self.pos_X = random.randint(600,1000)
        self.pos_Y = random.randint(50,300)
        self.image = self.image_0
        self.rect = self.image.get_rect()
        self.image_alpha = 0
        self.Fade_In = False
        self.Fade_Out = False
        self.ready_for_click = False
        self.respawn_timer_active = True
        self.spawn_timer = 0
        self.image.set_alpha(self.image_alpha)

    def generate_new_cords(self):
        self.pos_Y = random.randint(50,300)
        self.pos_X = random.randint(500,1000)

    def update(self, respawn_time):
        self.rect.midtop = (self.pos_X,self.pos_Y)
        self.mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(self.mousePos):
            self.image = self.image_1
        else: self.image = self.image_0
    # fade in
        if self.Fade_In:
            self.image_alpha += 3
            self.ready_to_respawn = False
            if self.image_alpha >= 255:
                self.ready_for_click = True
                self.Fade_In = False
                self.image_alpha = 255
    # fade out        
        if self.Fade_Out:
            self.image_alpha -= 5
            self.ready_for_click = False
            if self.image_alpha <= 0:
                self.Fade_Out = False
                self.Fade_In = False
                self.pos_Y = -100
                self.respawn_timer_active = True
    # respawn timer    
        if self.respawn_timer_active:
            self.spawn_timer += 1
            if self.spawn_timer > respawn_time:
                self.spawn_timer = 0
                self.respawn_timer_active = False
                self.Fade_In = True
                self.pos_Y = random.randint(50,300)
                self.pos_X = random.randint(500,1000)

        self.image.set_alpha(self.image_alpha)


PlayerAnimHandle = PlayerAnimation(200,540)
StoneSmall = ObsticleGround(2500,'images/game/batu api.png')
StoneMed = ObsticleGround(6000,'images/game/meteor sedang.png') # 8000 org
StoneBig = ObsticleGround(17000,'images/game/meteor besar.png') # 17000 original
BerryBush = ObsticleGroundAnimated(18000,'images/game/animated/berry bush/bush 1.png','images/game/animated/berry bush/bush 2.png','images/game/animated/berry bush/bush 3.png',) #25000 org
PlanetScore = PlanetBoost('images/game/planet score 0.png','images/game/planet score 1.png')
PlanetTime = PlanetBoost('images/game/planet time 0.png','images/game/planet time 1.png')

# sprite adding
menuSprites = pygame.sprite.Group()
gameSprites = pygame.sprite.Group()
    

# core vars
Game, Pause, Menu = False, False, True


    #game start
game_start_AUD = pygame.mixer.Sound('audio/game start.mp3')
game_start_AUD.set_volume(0.17)
    # AUDIO
game_music_list = []
game_music_list.append(pygame.mixer.Sound('audio/game music 1.mp3'))
game_music_list.append(pygame.mixer.Sound('audio/game music 2.mp3'))
game_music_list.append(pygame.mixer.Sound('audio/game music 3.mp3'))
game_music_list.append(pygame.mixer.Sound('audio/game music 4.mp3'))
game_music = random.choice(game_music_list)
game_music.set_volume(0.15)
    #game variables
high_score_label_cord = (10, 10)
high_score = 0
movementSpeedTimer = 0
movementSpeed = 5
groundX = -1100
grass_X_1 = 3000
score = 0
scoreTimer = 0

    #game background
ground_stoneAge = pygame.image.load('images/game/jalananbatuu.png').convert_alpha()
grass_IMG_1 = pygame.image.load('images/game/surface1.png').convert_alpha()
mushroomsIMG = pygame.image.load('images/game/mushrooms 1.png').convert_alpha()
mushrooms_X = 5000
sky_stoneAge = pygame.image.load('images/game/back.png').convert_alpha()
nightOverlayIMG = pygame.image.load('images/game/night overlay.png').convert_alpha()

skyPosX = -2800
skyXspeed = 0.9
nightOverlayAlpha = 0

    # GUI
high_score_value_cord = (190, 10)
fontGameUI = pygame.font.Font('fonts/minecraft.otf', 30)
high_score_label = fontGameUI.render("High Score:", False, (255, 255, 255))
HPlabel = fontGameUI.render('HP',False,(130,100,230))
score_text = fontGameUI.render(str(score),False,(255,255,255))
score_label = pygame.image.load('images/game/score label.png').convert_alpha()
score_boost_PopUp = pygame.image.load('images/game/score boost +20.png').convert_alpha()
score_boost_PopUp_FadeIn, score_boost_PopUp_FadeOut,score_boost_PopUp_alpha = False, False, 0
HP_damage_take_highlight = pygame.image.load('images/game/HP damage highlight.png').convert_alpha()

 
    #images
menuScreenMapIMG = pygame.image.load('images/menu/screenMap.png').convert_alpha()
    #transition: menu -> game
transition_game_img = pygame.image.load('images/game/transition.png').convert_alpha()
transition_game_X = -1400
transition_game_X_speed = 85
transition_game = False

    # audio
menu_music_list = []
menu_music_list.append(pygame.mixer.Sound('audio/menu music 1.mp3'))
menu_music_list.append(pygame.mixer.Sound('audio/menu music 2.mp3'))
menu_music_list.append(pygame.mixer.Sound('audio/menu music 3.mp3'))
menu_music_list.append(pygame.mixer.Sound('audio/menu music 4.mp3'))
menu_music = menu_music_list[0]
menu_music_volume = 0.2
menu_music_last = -1
menu_music.play()
menu_music.set_volume(menu_music_volume)

    #vars
prevMenuImg = 1
menuImgAlreadyChosen = False
menuImgCordMap = [0,-800,-1600,-2400] #y cords of menu screen image mapping
menuScreenImg = menuImgCordMap[3]

#----------------PAUSE----------------PAUSE----------------PAUSE---------------
pauseScreenIMG = pygame.image.load('images/pause/screen.png').convert_alpha()
FirstEscapeInput = True

while True:


    while Game:
        print("GAME RUNNING")
        menuSprites.remove(buttonGO)
        menuSprites.remove(buttonEXIT)
        gameSprites.add(PlayerAnimHandle)
        gameSprites.add(PlayerHitbox)
        gameSprites.add(StoneSmall)
        gameSprites.add(StoneMed)
        gameSprites.add(StoneBig)
        gameSprites.add(BerryBush)
        gameSprites.add(PlanetScore)
        gameSprites.add(PlanetTime)

        # update high score
        if score > high_score:
            high_score = score

        for event in pygame.event.get(): 

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit()
            
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                Pause = True
                PauseDrawn = False #ensures the pause screen is drawn once, to keep transparency
                Game = False
                Menu = False
                menuImgAlreadyChosen = False
                FirstEscapeInput = True
                print('  mode -> PAUSE')

            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                PlayerAnimHandle.AnimState = 'jump'

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = pygame.mouse.get_pos()

                    # score boost planet
                    if PlanetScore.rect.collidepoint(mousePos) and PlanetScore.ready_for_click:
                        score += 10
                        print('planet ScoreBoost clicked')
                        PlanetScore.Fade_Out = True
                        score_boost_PopUp_FadeIn = True
                    # slow down time planet
                    if PlanetTime.rect.collidepoint(mousePos) and PlanetTime.ready_for_click:
                        movementSpeed = (movementSpeed // 2.5) + 4
                        print('planet SlowMotion clicked')
                        PlanetTime.Fade_Out = True

                if PlayerAnimHandle.rect.bottom <= 530:
                    PlayerAnimHandle.AnimState = 'crash'
        
        groundX -= movementSpeed
        grass_X_1 -= movementSpeed
        mushrooms_X -= movementSpeed
        movementSpeedTimer += 1

        if movementSpeedTimer > 240:
            movementSpeed += 1
            movementSpeedTimer = 0

#background update
        if groundX <= -5500: groundX = 0
        if grass_X_1 <= -1200: grass_X_1 = mushrooms_X + random.randint(50,2500)
        if mushrooms_X <= -1200: mushrooms_X = random.randint(4000,8000)
        
        if BerryBush.rect.colliderect(StoneBig.rect):
            BerryBush.rect.left += 160
    #sky
        if skyPosX < -780 and skyPosX > -2700:
            skyXspeed += 0.2
            if nightOverlayAlpha > 0:
                nightOverlayAlpha -= 2
        elif skyPosX < -4100 and skyPosX > -6030:
            skyXspeed += 0.2
            if nightOverlayAlpha <= 210:
                nightOverlayAlpha += 2
        else: skyXspeed = 0.9 #0.7 original
        skyPosX -= skyXspeed
        if skyPosX < -6800: skyPosX = 0
    # planet boost


# player collision
        PlayerHitbox.PlayerCollisionCheck(StoneSmall.rect,StoneMed.rect,StoneBig.rect,BerryBush.rect)
        if PlayerHitbox.berryBushCollided: BerryBush.animPlay = True
# HP bar
        HPbar_RGB = (abs(255-PlayerHitbox.HP),0,PlayerHitbox.HP)
        HPbar_height = PlayerHitbox.HP / 2

#score update
        scoreTimer += 1
        if scoreTimer > 60:
            score += 1 
            scoreTimer = 0

        screen.blit(sky_stoneAge, (skyPosX,0))
        screen.blit(ground_stoneAge, (groundX,540))
        gameSprites.draw(screen)
        PlayerAnimHandle.update(0.18)
        PlayerHitbox.update(PlayerAnimHandle.rect.bottom)
        
    #obsticles update
        StoneSmall.update(movementSpeed,2200,1200,-42)
        StoneMed.update(movementSpeed,3500,1300,-63)
        StoneBig.update(movementSpeed,5800,1500,-77)
        BerryBush.update(movementSpeed,6500,2200,-105,0.4)
        screen.blit(grass_IMG_1, (grass_X_1,180))
        screen.blit(mushroomsIMG, (mushrooms_X, 505))

    # Player Health
        pygame.draw.rect(screen, HPbar_RGB, (30, 400, 15, HPbar_height))
    # Player Death
        if not PlayerHitbox.Alive:
            Game, Menu = False, True
            PlayerHitbox.Alive, PlayerHitbox.HP = True, 255
            score = 0
            movementSpeed = 5
            skyPosX = -2800


    #sky objects
        screen.blit(nightOverlayIMG, (0,0))
        nightOverlayIMG.set_alpha(nightOverlayAlpha)
        PlanetScore.update(600)
        PlanetTime.update(1500)

#gui
    # taking damage HP highlight
        if PlayerHitbox.taking_damage:
            screen.blit(HP_damage_take_highlight, (3,358))
    # text render
        screen.blit(HPlabel, (25,370))
        score_text = fontGameUI.render(str(score),False,(255,255,255))
        screen.blit(score_text, (242,572))
        screen.blit(score_label, (105,560))
    # score boost pop up
        if score_boost_PopUp_FadeIn:
            score_boost_PopUp_alpha += 3
            score_boost_PopUp.set_alpha()
            if score_boost_PopUp_alpha >= 255:
                score_boost_PopUp_FadeOut = True
                score_boost_PopUp_FadeIn = False
        if score_boost_PopUp_FadeOut:
            score_boost_PopUp_alpha -= 3
            if score_boost_PopUp_alpha <= 0:
                score_boost_PopUp_FadeOut = False
        score_boost_PopUp.set_alpha(score_boost_PopUp_alpha)
        screen.blit(score_boost_PopUp, (222,597))

    # transition continue from menu
        if transition_game:
            transition_game_X += transition_game_X_speed
            transition_game_X_speed += 2
            screen.blit(transition_game_img, (transition_game_X, -10))
            if transition_game_X > 1100:
                transition_game = False

        pygame.display.update()
        fps.tick(60)


    #adding menu sprites
    menuSprites.add(buttonGO)
    menuSprites.add(buttonEXIT)
    gameSprites.remove(PlayerAnimHandle)
    gameSprites.remove(PlayerHitbox)
    gameSprites.remove(StoneSmall)
    gameSprites.remove(StoneMed)
    gameSprites.remove(StoneBig)
    gameSprites.remove(BerryBush)
    gameSprites.remove(PlanetScore)
    gameSprites.remove(PlanetTime)

    # switching menu background every re-enter
    if menuImgAlreadyChosen == False:
            while menuScreenImg == prevMenuImg:
                menuScreenImg = menuImgCordMap[1]
                menuImgAlreadyChosen = True
                prevMenuImg = menuScreenImg
            pygame.mixer.unpause()

    while Menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #closing window
                pygame.quit()
                raise SystemExit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if buttonEXIT.rect.collidepoint(mousePos):
                    sys.exit()

                if buttonGO.rect.collidepoint(mousePos):
                    transition_game = True
                    game_start_AUD.play()
                    
        screen.blit(menuScreenMapIMG, (0,menuScreenImg))
        screen.blit(high_score_label, high_score_label_cord)
        high_score_value = fontGameUI.render(str(high_score), False, (255, 255, 255))
        screen.blit(high_score_value, high_score_value_cord)
        menuSprites.draw(screen)

        if transition_game:
            transition_game_X += transition_game_X_speed
            transition_game_X_speed -= 3
            screen.blit(transition_game_img, (transition_game_X, -10))
            if transition_game_X > -180:
                Game = True
                Menu = False
                Pause = False
                game_music = random.choice(game_music_list).play()
                menu_music.set_volume(0)

        menuSprites.update()
        pygame.display.update() #updating display
        fps.tick(60)


    while Pause:
        print("PAUSE STARTED")
        pygame.mixer.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit()

            if event.type == pygame.MOUSEBUTTONDOWN: #when click
                mousePos = pygame.mouse.get_pos()
                if mousePos[0] > 414 and mousePos[0] < 683 and mousePos[1] > 448 and mousePos[1] < 503: # to menu button click range
                    pygame.mixer.unpause()
                    print('  mode -> MENU')
                    Game = False
                    Pause = False
                    Menu = True
                    PauseDrawn = False

                    menu_music = menu_music_list[3]
                    menu_music.set_volume(0.2)
                    game_music.set_volume(0)
                    menu_music.play()
            
            if pygame.key.get_pressed()[pygame.K_ESCAPE] and not FirstEscapeInput:
                pygame.mixer.unpause()
                print('  mode -> GAME')
                Pause = False
                Menu = False
                Game = True
                PauseDrawn = False
                menuImgAlreadyChosen = False
                FirstEscapeInput = True

            if PauseDrawn == False:
                screen.blit(pauseScreenIMG, (122,4))
                PauseDrawn = True
                FirstEscapeInput = False
    
        pygame.display.update()
        fps.tick(60)
