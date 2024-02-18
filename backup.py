import pygame as pg
import math
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

FLY_SPEED = 2

background = pg.image.load('background.png')
background = pg.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

sprite_image = pg.image.load('cozy_frog.png')
sprite_image = pg.transform.scale(sprite_image, (350, 350))
sprite_rect = sprite_image.get_rect(center=(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2 + 150))

fly_image = pg.image.load('fly.png')
fly_image = pg.transform.scale(fly_image, (150, 150))
fly_image = pg.transform.rotate(fly_image, 180)
fly_rect = fly_image.get_rect(center=(200, 100))

tongue_image = pg.image.load('tongue.png')
tongue_image = pg.transform.scale(tongue_image, (100, 100))
tongue_rect = tongue_image.get_rect(center=(500, 500))

bullet_image = pg.image.load('bullet.png')
bullet_image = pg.transform.scale(bullet_image, (75, 75))
bullet_image = pg.transform.rotate(bullet_image, 45)
bullet_rect = bullet_image.get_rect()

explosion_image = pg.image.load('explosion.png')
explosion_image = pg.transform.scale(explosion_image, (200, 200))
explosion_rect = explosion_image.get_rect()

# Fly movement parameters
fly_wave_amplitude = 100  # Maximum horizontal movement distance from the center
fly_wave_frequency = 0.05  # Frequency of the wave; adjust for faster or slower oscillation

# Initialize a variable to track the horizontal oscillation phase
fly_wave_phase = 0

# Arc parameters
arc_radius = 100  # Adjust as necessary for the desired arc size
arc_angle_start = 270  # Starting angle in degrees
arc_angle_end = 360  # Ending angle in degrees
arc_angle_current = arc_angle_start  # Initialize current angle to the start angle
arc_speed = 1  # Speed of movement along the arc, adjust as necessary
moving_forward = True  # Track the direction of arc movement

tongue_shot = None
tongue_shot_alive = False
tongue_shot_alive_list = [False, False, False]
tongue_shots = [{}, {}, {}]
tongue_shot_count = 0
tongue_shot_x_motion = 2
tongue_shot_y_motion = 2
tongue_shot_rect = pg.Rect(0, 0, 75, 75)

hitbox_scale = 0.2
hitbox_width = int(150 * hitbox_scale)
hitbox_height = int(150 * hitbox_scale)

# Initialize the score and font
score = 0
font_size = 72  # Adjust as needed

pg.init()

pg.display.set_caption("game")

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.DOUBLEBUF)

clock = pg.time.Clock()

show_explosion = False
explosion_counter = 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and tongue_shot_count < 3:
            print(tongue_shot_count)
            # tongue_shot_alive = True
            tongue_shot_alive_list[tongue_shot_count] = True

            tongue_shot_x = tongue_x-20
            tongue_shot_y = tongue_y-20
            
            tongue_shot_rect = pg.Rect(0, 0, 25, 25)
            tongue_shot_rect.topleft = (tongue_shot_x, tongue_shot_y)
            
            tongue_shots[tongue_shot_count] = {
                'x': tongue_x-20,
                'y': tongue_y-20,
                'rect' : tongue_shot_rect
            }
            
            tongue_shot_count += 1

    screen.blit(background, (0, 0))
    screen.blit(sprite_image, sprite_rect)
    screen.blit(fly_image, fly_rect)
    screen.blit(tongue_image, tongue_rect)
    
    if explosion_counter > 60:
        explosion_counter = 0
        show_explosion = False
    
    if show_explosion and explosion_counter <= 60:
        screen.blit(explosion_image, explosion_rect)
        explosion_counter += 1
    
    # Calculate the new horizontal position using a sine wave for the oscillation
    fly_wave_phase += fly_wave_frequency
    fly_horizontal_movement = math.sin(fly_wave_phase) * fly_wave_amplitude
    
    # Update the fly's position
    fly_rect.centerx = (SCREEN_WIDTH / 2)-200 + fly_horizontal_movement
    fly_rect.centery += FLY_SPEED  # Continue moving down at a constant speed
    
    fly_hitbox = pg.Rect(
        fly_rect.centerx - hitbox_width // 2,
        fly_rect.centery - hitbox_height // 2,
        hitbox_width,
        hitbox_height
    )
    
    if fly_rect.top > SCREEN_HEIGHT:
        fly_rect.top = -fly_rect.height  # Reset position to the top of the screen
    else:
        fly_rect.move_ip(0, FLY_SPEED)
        
    # Update tongue's position to follow an arc
    if moving_forward:
        if arc_angle_current <= arc_angle_end:
            angle_rad = math.radians(arc_angle_current)
            tongue_x = sprite_rect.centerx - arc_radius * math.cos(angle_rad)
            tongue_y = sprite_rect.centery + arc_radius * math.sin(angle_rad)
            tongue_rect.center = (tongue_x, tongue_y)
            arc_angle_current += arc_speed
        else:
            moving_forward = False  # Change direction
            arc_angle_current -= arc_speed  # Start moving back immediately
    else:  # Moving backward
        if arc_angle_current >= arc_angle_start:
            angle_rad = math.radians(arc_angle_current)
            tongue_x = sprite_rect.centerx - arc_radius * math.cos(angle_rad)
            tongue_y = sprite_rect.centery + arc_radius * math.sin(angle_rad)
            tongue_rect.center = (tongue_x, tongue_y)
            arc_angle_current -= arc_speed
        else:
            moving_forward = True  # Change direction
            arc_angle_current += arc_speed  # Start moving forward immediately
        
    if any(tongue_shot_alive_list):
        # tongue_shot.move_ip(-tongue_shot_x_motion, -tongue_shot_y_motion)
        # pg.draw.rect(screen, (255, 182, 193), tongue_shot)
        for tongue_shotty in tongue_shots:
            if tongue_shotty:
                tongue_shot_x -= tongue_shot_x_motion
                tongue_shot_y -= tongue_shot_y_motion
                tongue_shotty['rect'].topleft = (tongue_shot_x, tongue_shot_y)
                tongue_shotty['x'] = tongue_shot_x
                tongue_shotty['y'] = tongue_shot_y
                screen.blit(bullet_image, (tongue_shot_x, tongue_shot_y))
                if tongue_shot_y < -50:
                    tongue_shot_count -= 1
                    del tongue_shotty['x']
                    del tongue_shotty['y']
                    del tongue_shotty['rect']

    if tongue_shot_rect and tongue_shot_rect.colliderect(fly_hitbox):
        fly_rect.top = -fly_rect.height  # Reset position to the top of the screen
        tongue_shot_alive = False
        tongue_shot_rect = None
        score += 1  # Increase score when the fly is hit
        show_explosion = True
        explosion_rect = explosion_image.get_rect(center=(tongue_shot_x, tongue_shot_y))

    font = pg.font.SysFont(None, font_size)

    score_text = f"Score: {score}"
    text_surface = font.render(score_text, True, (255, 255, 255))  # White color
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))  # Adjust positioning as needed
    screen.blit(text_surface, text_rect)

    pg.display.update()
    clock.tick(60)

pg.quit()
