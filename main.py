import pygame
import random

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
player_starting_lives = 5
player_lives = player_starting_lives
player_score = 0


pygame.init()

class GAME:
    def __init__(self,WINDOW_WIDTH,WINDOW_HEIGHT,player_score,player_lives):
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.surface = pygame.display.set_mode((self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        self.caption = pygame.display.set_caption("Lucky dragon")
        # the header
        self.header = Header()
        # for the score text
        self.player_score = player_score
        self.score = Score(self.player_score)
        # for lives text
        self.player_lives = player_lives
        self.lives = Lives(player_lives)
        # self.lives = Lives(self.player_lives)
        # self.dragon = Dragon(self.sound)
        self.Fps = 60
        self.clock = pygame.time.Clock()
        self.sound = Sound()
        self.dragon = Dragon(self.sound)
        self.coin = Coin(self.sound)
        self.block = Block(self.sound)
        self.apple = Apple(self.dragon.dragon_right_rect,self.coin.coin_rect,self.player_lives)

    def run(self):
        self.surface.fill((0,0,0))
        self.surface.blit(self.header.starter_text,self.header.starter_text_rect)
        pygame.display.update()
        waiting = True
        running = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    waiting = False
                if event.type == pygame.QUIT:  # Check for QUIT event to exit waiting loop
                    waiting = False
                    running = False

        self.sound.back_ground_sound_play()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.dragon.dragon_right_rect.top > 70:
                self.dragon.dragon_move_up()
            if keys[pygame.K_DOWN] and self.dragon.dragon_right_rect.bottom < self.WINDOW_HEIGHT:
                self.dragon.dragon_move_down()
            # coin movement
            self.player_lives = self.coin.coin_movement(self.player_lives)
            self.surface.fill((0,0,0))
            #block movement
            self.block.block_movement()

            #dragon and coin collidetection
            if self.dragon.dragon_colli_detection(self.coin.coin_rect,self.coin.coin_speed,self.coin.buffer_distance):
                self.player_score+=1
                self.coin.coin_speed+=self.coin.coin_acceleration
            #block and dragon collidetection
            if self.block.block_collidetection(self.block.block_rect,self.dragon.dragon_right_rect,self.block.block_speed,self.block.block_acceleration,self.block.buffer_distance):
                self.player_lives-=1

            # apple movement to add lives
            if self.apple.apple_movement(self.player_lives):
                self.player_lives+=1

            # self.apple
            Logic(self.coin.coin_rect,self.block.block_rect,self.coin.coin_speed).to_evade_the_block()
            Logic(self.coin.coin_rect, self.block.block_rect, self.coin.coin_speed).to_evade_the_apple_from_objects(self.apple.apple_image_rect)
            #update the lives
            self.score.score_text = self.score.score_font_system.render("SCORE:" + str(self.player_score), True, (0, 255, 0))
            self.lives.lives_text = self.lives.lives_font_system.render("LIVES:" + str(self.player_lives), True, (0, 255, 0))
            if self.player_lives == 0:
                self.surface.blit(self.header.game_over,self.header.game_over_rect)
                self.surface.blit(self.header.continue_text,self.header.continue_text_rect)
                pygame.display.update()
                self.sound.back_ground_sound_stop()
                pause = True
                while pause:
                    for event in pygame.event.get():
                        #if player wants to play again
                        if event.type == pygame.KEYDOWN:
                            self.player_score = 0
                            self.player_lives = 5
                            self.dragon.dragon_right_rect.y = self.WINDOW_HEIGHT//2
                            self.coin.coin_speed = self.coin.coin_starting_speed
                            self.apple.apple_image_rect.y = WINDOW_WIDTH + 200
                            self.sound.back_ground_sound_play()
                            pause = False
                        if event.type == pygame.QUIT:
                            pause = False
                            running = False

            self.surface.fill((0,0,0))
            pygame.draw.line(self.surface, (255, 255, 255), (0, 70), (self.WINDOW_WIDTH, 70), 2)
            self.surface.blit(self.header.title_text, self.header.title_text_rect)
            self.surface.blit(self.score.score_text,self.score.system_text_rect)
            self.surface.blit(self.lives.lives_text,self.lives.lives_text_rect)
            # the dragon
            # dragon = Dragon()
            self.surface.blit(self.dragon.dragon_right,self.dragon.dragon_right_rect)
            #coin
            self.surface.blit(self.coin.coin_image,self.coin.coin_rect)
            self.surface.blit(self.block.block_image,self.block.block_rect)
            self.surface.blit(self.apple.apple_image,self.apple.apple_image_rect)
            pygame.display.update()
            self.clock.tick(self.Fps)

class Header:
    def __init__(self):
        self.title_font_system = pygame.font.Font('AttackGraffiti.ttf', 32)
        self.title_text = self.title_font_system.render("LUCKY DRAGON", True, (0, 255, 0))
        self.title_text_rect = self.title_text.get_rect()
        self.title_text_rect.center = (WINDOW_WIDTH // 2, 50)

        self.font = pygame.font.Font('AttackGraffiti.ttf', 32)

        self.game_over = self.font.render('GAMEOVER',True,(0,255,0))
        self.game_over_rect = self.game_over.get_rect()
        self.game_over_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

        self.continue_text = self.font.render("Press any key to play again",True,(0,255,0))
        self.continue_text_rect = self.continue_text.get_rect()
        self.continue_text_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2 + 32)

        self.starter_text = self.font.render("Press s to start",True,(0,255,0))
        self.starter_text_rect = self.starter_text.get_rect()
        self.starter_text_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2 + 32)


class Score:
    def __init__(self,player_score):
        self.player_score = player_score
        self.score_font_system = pygame.font.SysFont('calibri', 40)
        self.score_text = self.score_font_system.render("SCORE:" + str(self.player_score), True, (0, 255, 0))
        self.system_text_rect = self.score_text.get_rect()
        self.system_text_rect.topleft = (10, 30)

class Lives:
    def __init__(self,player_lives):
        self.player_lives = player_lives
        self.lives_font_system = pygame.font.SysFont('calibri', 40)
        self.lives_text = self.lives_font_system.render("LIVES:" + str(self.player_lives), True, (0, 255, 0))
        self.lives_text_rect = self.lives_text.get_rect()
        self.lives_text_rect.topright = (950, 30)

# dragon_speed = 10
class Dragon:
    def __init__(self,sound):
        self.dragon_right = pygame.image.load("dragon_right.png")
        self.dragon_right_rect = self.dragon_right.get_rect()
        self.dragon_right_rect.center = (100,WINDOW_HEIGHT//2)
        self.dragon_speed = 10
        self.sound = sound
    def dragon_move_up(self):
        self.dragon_right_rect.y -= self.dragon_speed
    def dragon_move_down(self):
        self.dragon_right_rect.y += self.dragon_speed
    def dragon_colli_detection(self,coin_rect,coin_speed,buffer_distance):
        if self.dragon_right_rect.colliderect(coin_rect):
            self.sound.play_coin_sound()
            coin_rect.x = WINDOW_WIDTH + buffer_distance
            coin_rect.y = random.randint(70, WINDOW_HEIGHT - 32)
            return True


class Sound:
    def __init__(self):
        self.background_sound = pygame.mixer.music.load("music.wav")
        self.coin_sound = pygame.mixer.Sound("sound_1.wav")
        self.miss_sound = pygame.mixer.Sound("sound_2.wav")

    def back_ground_sound_play(self):
        pygame.mixer.music.set_volume(1.0)  # Set the volume to 100% first
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() * 2)
        pygame.mixer.music.play(-1, 0.0)

    def play_miss_sound(self):
        self.miss_sound.set_volume(0.3)
        self.miss_sound.play()

    def play_coin_sound(self):
        self.coin_sound.play()
    def back_ground_sound_stop(self):
        pygame.mixer.music.stop()
class Coin:
    def __init__(self,sound):
        self.buffer_distance = 50
        self.coin_image = pygame.image.load("coin.png")
        self.coin_rect = self.coin_image.get_rect()
        self.coin_rect.x = WINDOW_WIDTH + self.buffer_distance
        self.coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
        self.coin_starting_speed = 6
        self.coin_acceleration = .2
        self.coin_speed = self.coin_starting_speed
        self.sound = sound

    def coin_movement(self,lives):
        updated_lives = lives
        if self.coin_rect.x < 0:
            updated_lives-=1
            self.sound.play_miss_sound()
            self.coin_rect.x = WINDOW_WIDTH + self.buffer_distance
            self.coin_rect.y = random.randint(70, WINDOW_HEIGHT - 32)

        else:
            self.coin_rect.x -= self.coin_speed
        return updated_lives
class Block:
    def __init__(self,sound):
        self.buffer_distance = 50
        self.block_image = pygame.image.load("block.jpg")
        self.block_rect = self.block_image.get_rect()
        self.block_rect.x = WINDOW_WIDTH + self.buffer_distance
        self.block_rect.y = random.randint(64,WINDOW_HEIGHT-40)
        self.block_starting_speed = 2
        self.block_acceleration = .1
        self.block_speed = self.block_starting_speed
        self.sound = sound

    def block_collidetection(self,block_rect,dragon_rect,block_speed,block_acceleration,buffer_distance):
        if block_rect.colliderect(dragon_rect):
            self.sound.play_miss_sound()
            block_speed += block_acceleration
            block_rect.x = WINDOW_WIDTH + buffer_distance
            block_rect.y = random.randint(70,WINDOW_HEIGHT - 40)
            return True

    def block_movement(self):
        if self.block_rect.x < 0:

            self.block_rect.x += WINDOW_WIDTH + self.buffer_distance
            self.block_rect.y = random.randint(70, WINDOW_HEIGHT - 40)

        else:
            self.block_rect.x -= self.block_speed

class Logic:
    def __init__(self,coin,block,speed):
        self.coin = coin
        self.block = block
        self.speed = speed
    def to_evade_the_block(self):
        if self.coin.colliderect(self.block):
            middle = WINDOW_HEIGHT//2
            if self.coin.y >= middle:
                self.coin.y -= self.speed + 15

            else:
                self.coin.y += self.speed + 15
    def to_evade_the_apple_from_objects(self,apple):
        if apple.colliderect(self.coin):
            middle = WINDOW_HEIGHT // 2
            if apple.y >= middle:
                apple.y -= self.speed + 15
            else:
                apple.y += self.speed + 15

        elif apple.colliderect(self.block):
            middle = WINDOW_HEIGHT // 2
            if apple.y >= middle:
                self.block.y -= self.speed + 15
            else:
                self.block.y += self.speed + 15

class Apple:
    def __init__(self, dragon_rect, coin_rect,player_lives):
        self.apple_image = pygame.image.load("apple.jpg")
        self.apple_image_rect = self.apple_image.get_rect()
        self.apple_image_rect.x = WINDOW_WIDTH + 50
        self.apple_image_rect.y = random.randint(64,WINDOW_HEIGHT-64)
        self.apple_speed = 5
        self.dragon = dragon_rect
        self.coin = coin_rect
        self.apple_lives = player_lives
        self.flag = True


    def apple_movement(self,updated_lives):
        lives = updated_lives
        if lives == 1:
            if self.apple_image_rect.x < 0:
                self.apple_image_rect.x = WINDOW_WIDTH + 50
                self.apple_image_rect.y = random.randint(70, WINDOW_HEIGHT - 40)
            else:
                self.apple_image_rect.x -= self.apple_speed

            if self.apple_image_rect.colliderect(self.dragon):
                self.apple_lives+=1
                self.apple_image_rect.x = WINDOW_WIDTH + 50
                self.apple_image_rect.y = random.randint(70, WINDOW_HEIGHT - 40)
                return True
        elif lives >1 and lives <3:
            if self.apple_image_rect.x < 0:
                self.apple_image_rect.x = WINDOW_WIDTH + 50
                self.apple_image_rect.y = random.randint(70, WINDOW_HEIGHT - 40)
            else:
                self.apple_image_rect.x -= self.apple_speed

            if self.apple_image_rect.colliderect(self.dragon):
                self.apple_lives += 1
                self.apple_image_rect.x = WINDOW_WIDTH + 50
                self.apple_image_rect.y = random.randint(70, WINDOW_HEIGHT - 40)
                return True

game = GAME(WINDOW_WIDTH,WINDOW_HEIGHT,player_score,player_lives)
game.run()
