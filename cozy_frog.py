import pygame as pg
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

FLY_SPEED = 2

background = pg.image.load('images/background.png')
background = pg.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

sprite_image = pg.image.load('images/cozy_frog.png')
sprite_image = pg.transform.scale(sprite_image, (350, 350))
sprite_rect = sprite_image.get_rect(center=(SCREEN_WIDTH / 2 + 250, SCREEN_HEIGHT / 2 + 150))

fly_image = pg.image.load('images/fly.png')
fly_image = pg.transform.scale(fly_image, (150, 150))
fly_image = pg.transform.rotate(fly_image, 180)
fly_rect = fly_image.get_rect(center=(200, 100))

tongue_image = pg.image.load('images/tongue.png')
tongue_image = pg.transform.scale(tongue_image, (100, 100))
tongue_rect = tongue_image.get_rect(center=(500, 500))

bullet_image_1 = pg.image.load('images/bullet.png')
bullet_image_1 = pg.transform.scale(bullet_image_1, (75, 75))
bullet_image_1 = pg.transform.rotate(bullet_image_1, 45)

bullet_image_2 = pg.image.load('images/bullet.png')
bullet_image_2 = pg.transform.scale(bullet_image_2, (75, 75))
bullet_image_2 = pg.transform.rotate(bullet_image_2, 45)

bullet_image_3 = pg.image.load('images/bullet.png')
bullet_image_3 = pg.transform.scale(bullet_image_3, (75, 75))
bullet_image_3 = pg.transform.rotate(bullet_image_3, 45)

bullet_image_list = []
bullet_image_list.append(bullet_image_1)
bullet_image_list.append(bullet_image_2)
bullet_image_list.append(bullet_image_3)

explosion_image = pg.image.load('images/explosion.png')
explosion_image = pg.transform.scale(explosion_image, (200, 200))
explosion_rect = explosion_image.get_rect()

# Fly movement parameters
fly_wave_amplitude = 100  # Maximum horizontal movement distance from the center
fly_wave_frequency = 0.05  # Frequency of the wave; adjust for faster or slower oscillation

# Initialize a variable to track the horizontal oscillation phase
fly_wave_phase = 0

# Arc parameters
arc_radius = 100
arc_angle_start = 270
arc_angle_end = 360
arc_angle_current = arc_angle_start
arc_speed = 1  # Speed of movement along the arc
moving_forward = True

tongue_shot = None
tongue_shot_alive = False
tongue_shots = [{}, {}, {}]
tongue_shot_count = 0
tongue_shot_x_motion = 10
tongue_shot_y_motion = 10
tongue_shot_rect = pg.Rect(0, 0, 75, 75)

hitbox_scale = 0.2
hitbox_width = int(150 * hitbox_scale)
hitbox_height = int(150 * hitbox_scale)

score = 0
font_size = 36
font_path = "fonts/2P.ttf"

pg.init()
pg.mixer.init()

pg.display.set_caption("cozy frog")

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.DOUBLEBUF)

clock = pg.time.Clock()

show_explosion = False
explosion_counter = 0

explosion_path = 'sounds/explosion.wav'
explosion = pg.mixer.Sound(explosion_path)

shot_sound_path = 'sounds/shot.wav'
shot_sound = pg.mixer.Sound(shot_sound_path)

background_sound_path = "sounds/background.wav"
background_sound = pg.mixer.Sound(background_sound_path)
background_sound.play(loops=-1)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and tongue_shot_count < 3:
            shot_sound.play()
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
    
    fly_wave_phase += fly_wave_frequency
    fly_horizontal_movement = math.sin(fly_wave_phase) * fly_wave_amplitude
    
    fly_rect.centerx = (SCREEN_WIDTH / 2)-200 + fly_horizontal_movement
    fly_rect.centery += FLY_SPEED
    
    fly_hitbox = pg.Rect(
        fly_rect.centerx - hitbox_width // 2,
        fly_rect.centery - hitbox_height // 2,
        hitbox_width,
        hitbox_height
    )
    
    if fly_rect.top > SCREEN_HEIGHT:
        fly_rect.top = -fly_rect.height
    else:
        fly_rect.move_ip(0, FLY_SPEED)
        
    if moving_forward:
        if arc_angle_current <= arc_angle_end:
            angle_rad = math.radians(arc_angle_current)
            tongue_x = sprite_rect.centerx - arc_radius * math.cos(angle_rad)
            tongue_y = sprite_rect.centery + arc_radius * math.sin(angle_rad)
            tongue_rect.center = (tongue_x, tongue_y)
            arc_angle_current += arc_speed
        else:
            moving_forward = False
            arc_angle_current -= arc_speed
    else:
        if arc_angle_current >= arc_angle_start:
            angle_rad = math.radians(arc_angle_current)
            tongue_x = sprite_rect.centerx - arc_radius * math.cos(angle_rad)
            tongue_y = sprite_rect.centery + arc_radius * math.sin(angle_rad)
            tongue_rect.center = (tongue_x, tongue_y)
            arc_angle_current -= arc_speed
        else:
            moving_forward = True
            arc_angle_current += arc_speed
    if any(tongue_shots):
        for i, tongue_shotty in enumerate(tongue_shots):
            if tongue_shotty:
                tongue_shotty['x'] -= tongue_shot_x_motion
                tongue_shotty['y'] -= tongue_shot_y_motion
                tongue_shotty['rect'].topleft = (tongue_shotty['x'], tongue_shotty['y'])
                screen.blit(bullet_image_list[i], (tongue_shotty['x'], tongue_shotty['y']))
                if tongue_shotty['y'] < -50:
                    tongue_shots[i] = {}
                    tongue_shot_count -= 1

    if not any(tongue_shots):
        tongue_shot_count = 0
        
    for i, t in enumerate(tongue_shots):
        if not t:
            bullet_stock_image = pg.image.load('images/bullet.png')
            bullet_stock_image = pg.transform.scale(bullet_stock_image, (100, 100))
            screen.blit(bullet_stock_image, (600+50*i, 700))
        
    for tongue_shot in tongue_shots:
        if tongue_shot:
            if tongue_shot['rect'].colliderect(fly_hitbox):
                fly_rect.top = -fly_rect.height
                explosion_rect = explosion_image.get_rect(center=(tongue_shot['x'], tongue_shot['y']))
                tongue_shot.clear()
                score += 1
                show_explosion = True
                tongue_shot_count -= 1
                explosion.play()                
                break

    font = pg.font.Font(font_path, font_size)

    score_text = f"Score: {score}"
    text_surface = font.render(score_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 25, 25))
    screen.blit(text_surface, text_rect)

    pg.display.update()
    clock.tick(60)

pg.quit()
