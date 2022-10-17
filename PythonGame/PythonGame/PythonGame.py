from cmath import e
from tkinter import W
import pygame
import os

pygame.init()

screen_width = 1000
screen_height = 600
running = True

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Joe Game')
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')


background = pygame.image.load(os.path.join(image_path, "background.png"))
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_rect = stage.get_rect().size
# character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
x_pos = (screen_width-character_width)/2
y_pos = screen_height-character_height- stage_rect[1]

# ENEMY
#enemy = pygame.image.load(os.path.join(image_path, "enemy.png"))
#enemy_size = enemy.get_rect().size
#enemy_width = enemy_size[0]
#enemy_height = enemy_size[1]
#ex_pos = (screen_width-enemy_width)/2    
#ey_pos = (screen_height-enemy_height)/2


# WEAPON
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_length = weapon_size[1]

weapons = []

weapon_speed = 10

# BALL

ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

ball_speeds = [-20, -18, -16, -14]

balls = []

balls.append({ "pos_x": 50, "pos_y": 50, "img_idx": 0, "to_x": 3, "to_y": -6, "init_spd_y": ball_speeds[0]})

speed = 0.8

to_x = 0
#to_y = 0

ball_to_remove = -1
weapon_to_remove = -1

clock = pygame.time.Clock()

game_font = pygame.font.Font(None, 40)

total_time = 60

start_ticks = pygame.time.get_ticks()

game_result = "Game Over"

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= speed
            elif event.key == pygame.K_RIGHT:
                to_x += speed
            #elif event.key == pygame.K_UP:
            #    to_y -= speed
            #elif event.key == pygame.K_DOWN:
            #    to_y += speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = x_pos + character_width/2 - weapon_width/2
                weapon_y_pos = y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
                
    x_pos += to_x*dt
    #y_pos += to_y*dt
    
    if x_pos < 0:
        x_pos = 0
    elif x_pos > screen_width - character_width:
        x_pos = screen_width - character_width

    
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > -(weapon_length/2)]
       
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        if ball_pos_y >= screen_height - stage_rect[1] - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    #if y_pos < 0:
    #    y_pos = 0
    #elif y_pos > screen_height - character_height - stage_rect[1]:
    #    y_pos = screen_height - character_height - stage_rect[1]

    char_rect = character.get_rect()
    char_rect.left = x_pos
    char_rect.top = y_pos

    #enemy_rect = enemy.get_rect()
    #enemy_rect.left = ex_pos
    #enemy_rect.top = ey_pos

    #if char_rect.colliderect(enemy_rect):
    #    running = False
    
    for ball_idx, ball_val in enumerate(balls):
        ball_rect = ball_images[ball_val["img_idx"]].get_rect()
        ball_rect.left = ball_val["pos_x"]
        ball_rect.top = ball_val["pos_y"]

        ball_size = ball_images[ball_val["img_idx"]].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if char_rect.colliderect(ball_rect):
            running = False
            break
        
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_val[0]
            weapon_rect.top = weapon_val[1]

            if weapon_rect.colliderect(ball_rect):
                ball_to_remove = ball_idx
                weapon_to_remove = weapon_idx

                if ball_val["img_idx"] < 3:
                    new_ball_rect = ball_images[ball_val["img_idx"]+1].get_rect().size
                    new_ball_width = new_ball_rect[0]
                    new_ball_height = new_ball_rect[1]
                
                    balls.append({ "pos_x": ball_val["pos_x"] + ball_width/2 - new_ball_width/2, 
                                   "pos_y": ball_val["pos_y"] + ball_height/2 - new_ball_height/2,
                                   "img_idx": ball_val["img_idx"]+1, "to_x": -3, "to_y": -6, "init_spd_y": ball_speeds[ball_val["img_idx"]+1]})
                
                    balls.append({ "pos_x": ball_val["pos_x"] + ball_width/2 - new_ball_width/2, 
                                   "pos_y": ball_val["pos_y"] + ball_height/2 - new_ball_height/2,
                                   "img_idx": ball_val["img_idx"]+1, "to_x": 3, "to_y": -6, "init_spd_y": ball_speeds[ball_val["img_idx"]+1]})

                break

        else:
            continue
        break
            
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if len(balls) == 0:
        game_result = "You Win!"
        running = False

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1


    screen.blit(background, (0, 0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]

        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(character, (x_pos, y_pos))
    #screen.blit(enemy, (ex_pos, ey_pos))
    #screen.fill((130, 200, 255))
    

    screen.blit(stage, (0, screen_height - stage_rect[1]))

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    timer = game_font.render(str(int(total_time-elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    if total_time < elapsed_time:
        game_result = "Time Over"
        running = False
        
    pygame.display.update()

msg = game_font.render(game_result, True, (255, 255, 255))
msg_rect = msg.get_rect(center = (int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()
    
pygame.time.delay(1000)
pygame.quit()