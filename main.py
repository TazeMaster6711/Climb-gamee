import pygame
import random

pygame.init()

font = pygame.font.SysFont('Arial', 48)

display = pygame.display.set_mode((1500, 900))

dead = False

x_pos = 0
y_pos = 0

x_vel = 0
y_vel = 0

player = pygame.Rect((x_pos, y_pos, 50, 75))

text_surface = font.render(str(round(-y_vel/50)), True, (255,255,255))
score_rect = text_surface.get_rect(center=(750, 75))

speed = 1.5

jump_last_frame = False
touching_ground = False
jump = False

wallslide_left = pygame.Rect(x_pos - 5, y_pos, 5, 75)
wallslide_right = pygame.Rect(x_pos + 50, y_pos, 5, 75)

platform_pos = []

checkpoint = 0

platforms = []
  
gravity = True

dash_cooldown = 0
dash_duration = 0

lava_pos = 1200   

for i in range(80):
    pos = (random.randint(1, 29)*50, random.randint(-17, 0) * 50 + checkpoint)
    platforms.append(pygame.Rect(pos[0], pos[1], 50, 50))
    platform_pos.append((pos[0], pos[1]))

# a


wallslide = False
used_walljump = False

while True:
    display.fill((0, 0, 0))

    if dead:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
            if event.type == pygame.K_r:    
                dead = False
                x_pos = 0
                y_pos = 0
                x_vel = 0
                y_vel = 0
                jump_last_frame = False
                touching_ground = False
                jump = False
                platform_pos = []
                checkpoint = 0
                platforms = []
                gravity = True
                dash_cooldown = 0
                dash_duration = 0
                lava_pos = 1200
                for i in range(80):
                    pos = (random.randint(1, 29)*50, random.randint(-17, 0) * 50 + checkpoint)
                    platforms.append(pygame.Rect(pos[0], pos[1], 50, 50))
                    platform_pos.append((pos[0], pos[1]))
                pygame.time.Clock().tick(60)
                pygame.display.flip()
        continue

    lava_pos -= 2   
    if lava_pos >  y_pos + 1200:
        lava_pos = y_pos + 1200   
    if lava_pos < y_pos + 450:
        dead = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    jump = False
    keys = pygame.key.get_pressed()
    if not used_walljump:        
        if keys[pygame.K_a]:
            x_vel -= speed
        if keys[pygame.K_d]:
            x_vel += speed
    if keys[pygame.K_SPACE] and not jump_last_frame:
        jump = True
        jump_last_frame = True
    elif not keys[pygame.K_SPACE]:
        jump_last_frame = False

    if keys[pygame.K_p]:
        y_vel -= 1.5

    dash_cooldown -= 1
    if keys[pygame.K_q] and dash_cooldown <= 0:       
        dash_duration = 6
        
        
        
    if dash_duration > 0:
        y_vel = 0
        y_pos -= 10 * dash_duration
        player = pygame.Rect((x_pos, y_pos, 50, 75))
        dash_cooldown = 450
        used_walljump = False
        for platform in platforms:
            if player.colliderect(platform):
                platforms.remove(platform)
        dash_duration -= 1
        if dash_duration == 0:
            y_vel = -15
    
    x_pos += x_vel
    if used_walljump:
        x_vel *= 0.99
    else:   
        x_vel *= 0.8

    player = pygame.Rect((x_pos, y_pos, 50, 75))

    wallslide = False


    for platform in platforms:
        if platform[1] > y_pos + 4500:
            platforms.remove(platform)

    for platform in platforms:
        if player.colliderect(platform):
            if not touching_ground and y_vel >= 0:
                wallslide = True            
                used_walljump = False
            while player.colliderect(platform):
                x_pos -= (x_vel / abs(x_vel))
                player = pygame.Rect((x_pos, y_pos, 50, 75))                 
    
    
    if x_pos < 0:
        x_pos = 0
        if not touching_ground and y_vel >= 0:
            wallslide = True
    if x_pos > 1450:
        x_pos = 1450
        if not touching_ground and y_vel >= 0:
            wallslide = True
    
    if wallslide:
        if jump:
            y_vel = -15 
            used_walljump = True
            for platform in platforms:
                if wallslide_left.colliderect(platform) and wallslide_right.colliderect(platform):
                    pass
                elif wallslide_left.colliderect(platform) or x_pos == 0:
                    x_vel = 10
                elif wallslide_right.colliderect(platform) or x_pos == 1450:
                    x_vel = -10
        else:
            y_vel = 5
    else:
        y_vel += 0.75
    y_pos += y_vel

    player = pygame.Rect((x_pos, y_pos, 50, 75))

    touching_ground = False
    

    for platform in platforms:
        if player.colliderect(platform):
            while player.colliderect(platform):
                y_pos -= (y_vel / abs(y_vel))
                player = pygame.Rect((x_pos, y_pos, 50, 75))                        
            y_vel = 1
            touching_ground = True
            wallslide = False

    if touching_ground and jump:
        y_vel = -17

    if checkpoint >= y_pos:
        checkpoint -= 900
        for i in range(80):
            pos = (random.randint(0, 29)*50, random.randint(-17, 0) * 50 + checkpoint)
            platforms.append(pygame.Rect(pos[0], pos[1], 50, 50))
            platform_pos.append((pos[0], pos[1]))


    if y_pos > -25:
        y_pos = -25
        y_vel = 0
        if jump:
            y_vel = -17
        else:
            touching_ground = True
    

    if touching_ground:
        used_walljump = False
        
    for platform in platforms:
        pygame.draw.rect(display, (150, 150, 150), (platform[0], platform[1] - y_pos + 450, platform[2], platform[3]))

    text_surface = font.render(str(round(-y_pos/50)), True, (255,255,255))

    player = pygame.Rect((x_pos, y_pos, 50, 75))
    wallslide_left = pygame.Rect(x_pos - 5, y_pos, 5, 75)
    wallslide_right = pygame.Rect(x_pos + 50, y_pos, 5, 75)
    pygame.draw.rect(display, (255, 255, 255), (player[0], 450, player[2], player[3]))
    pygame.draw.rect(display, (255, 0, 0), (0, lava_pos - y_pos, 1500, 900))
    display.blit(text_surface, score_rect)
    pygame.time.Clock().tick(60)
    pygame.display.flip()
    