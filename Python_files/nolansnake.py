import pygame
import sys
import time
import random

# Import pygame.sprite module
import pygame.sprite

pygame.init()

frame_size_x = 1450
frame_size_y = 1300

# Define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
header_color = pygame.Color(255, 140, 0)

difficulty = 10

game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption('Snake Eater')

fps_controller = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load("sound_files/Background_music.mp3")
pygame.mixer.music.play(-1)
eat_sound = pygame.mixer.Sound("sound_files/Eat_sound.wav")
game_over_sound = pygame.mixer.Sound("sound_files/Game_over_sound.wav")

# Load all apple images
apple_images = [pygame.image.load(f"assets/{i}.png") for i in range(1, 144)]
apple_images = [pygame.transform.scale(img, (150,150)) for img in apple_images]

# Load monster idle frames
monster_idle_frames = [pygame.image.load(f"assets/0_Monster_Idle_{i:03}.png") for i in range(18)]
monster_idle_frames = [pygame.transform.scale(frame, (130, 130)) for frame in monster_idle_frames]

snake_pos = [frame_size_x // 2, frame_size_y // 2]
snake_body = [
    [frame_size_x // 2, frame_size_y // 2],
    [frame_size_x // 2 - 40, frame_size_y // 2],
    [frame_size_x // 2 - 80, frame_size_y // 2]
]

food_pos = [random.randrange(1, (frame_size_x // 10)) * 10,
            random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True

# Initial random apple image
current_apple_image = random.choice(apple_images)
is_animation = current_apple_image in monster_idle_frames
animation_index = 0

snake_zone_img = pygame.image.load("assets/snakebody.png")
snake_zone_img = pygame.transform.scale(snake_zone_img, (60, 60))

stranger_snake_logo = pygame.image.load("assets/strangersnake_logo.png")
stranger_snake_logo = pygame.transform.scale(stranger_snake_logo, (int(frame_size_x * 0.8), int(frame_size_y * 0.1)))

direction = 'RIGHT'
change_to = direction
score = 0



# Function to handle game over
def game_over():
    global score, snake_pos, snake_body
    pygame.mixer.Sound.play(game_over_sound)
    my_font = pygame.font.SysFont('times new roman', 60)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)

    game_window.fill(black)  # Fill the screen with black

    # Clear the logo
    game_window.blit(background_image, (0, 0))

    game_window.blit(game_over_surface, game_over_rect)

    dev_font = pygame.font.SysFont('times new roman', 30)
    dev_text = 'Game developed by Nolan and Father'
    dev_surface = dev_font.render(dev_text, True, white)
    dev_rect = dev_surface.get_rect()
    dev_rect.midtop = (frame_size_x / 2, frame_size_y / 2 + 60)
    game_window.blit(dev_surface, dev_rect)

    restart_font = pygame.font.SysFont('times new roman', 25)
    restart_text = 'Please wait. Game is restarting...'
    restart_surface = restart_font.render(restart_text, True, white)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (frame_size_x / 2, frame_size_y / 2 + 100)
    game_window.blit(restart_surface, restart_rect)

    show_score(0, red, 'times', 30)
    pygame.display.flip()
    time.sleep(3)
    
    # Clear game variables
    score = 0
    snake_pos = [frame_size_x // 2, frame_size_y // 2]
    snake_body = [
        [frame_size_x // 2, frame_size_y // 2],
        [frame_size_x // 2 - 40, frame_size_y // 2],
        [frame_size_x // 2 - 80, frame_size_y // 2]
    ]

# Function to show score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()

    if choice == 1:
        background_rect = pygame.Rect((0, 0), (score_rect.width + 20, score_rect.height + 20))
        background_rect.center = (frame_size_x / 2, 15)
        pygame.draw.rect(game_window, white, background_rect)
        pygame.draw.rect(game_window, color, background_rect, 3)

        score_rect.topleft = (background_rect.left + 10, background_rect.top + 12)
        game_window.blit(score_surface, score_rect.topleft)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 4 + 100)
        game_window.blit(score_surface, score_rect)

# Function to show game description
def show_description():
    description_font = pygame.font.SysFont('consolas', 30)
    description_lines = [
        "Snake Eater is a fun game where you control a snake to eat apples.",
        "You eat an apple, your score increases and the snake grows longer.",
        "Avoid running into the walls or the snake's own body!"
    ]
    y_offset = frame_size_y + 50

    for line in description_lines[:2]:
        description_surface = description_font.render(line, True, white)
        description_rect = description_surface.get_rect()
        description_rect.midtop = (frame_size_x / 2, y_offset)
        game_window.blit(description_surface, description_rect)
        y_offset += 40

    logo_img = pygame.image.load("assets/strangersnake_logo.png")
    logo_img = pygame.transform.scale(logo_img, (400, 200))
    logo_rect = logo_img.get_rect()
    logo_rect.midtop = (frame_size_x / 2, y_offset + 10)
    game_window.blit(logo_img, logo_rect)

def show_controls():
    controls_font = pygame.font.SysFont('consolas', 30)
    header_font = pygame.font.SysFont('consolas', 35, bold=True)
    header_surface = header_font.render('Controls:', True, header_color)
    header_rect = header_surface.get_rect()
    header_rect.midtop = (frame_size_x / 2, frame_size_y + 300)
    game_window.blit(header_surface, header_rect)

    controls_surface = controls_font.render('T (UP), A (LEFT), L (RIGHT), V (DOWN)', True, white)
    controls_rect = controls_surface.get_rect()
    controls_rect.midtop = (frame_size_x / 2, frame_size_y + 340)
    game_window.blit(controls_surface, controls_rect)

# Load background images
background_images = [
    pygame.image.load("assets/bg1.png"),
    pygame.image.load("assets/bg2.png")
]

# Select a random background image initially
background_image = random.choice(background_images)
background_image = pygame.transform.scale(background_image, (frame_size_x, frame_size_y))

# Main game loop
while True:
    # Draw the background image
    game_window.blit(background_image, (0, 0))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('t'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('v'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('l'):
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Direction change logic
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move snake
    if direction == 'UP':
        snake_pos[1] -= 15
    if direction == 'DOWN':
        snake_pos[1] += 15
    if direction == 'LEFT':
        snake_pos[0] -= 15
    if direction == 'RIGHT':
        snake_pos[0] += 15

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))

    # Collision detection with border
    if snake_pos[0] < 0 or snake_pos[0] >= frame_size_x or snake_pos[1] < 0 or snake_pos[1] >= frame_size_y:
        game_over()
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # Check if the snake collides with the food
    snake_mask = pygame.mask.from_surface(snake_zone_img)
    if is_animation:
        food_mask = pygame.mask.from_surface(monster_idle_frames[animation_index])
    else:
        food_mask = pygame.mask.from_surface(current_apple_image)

    offset = (food_pos[0] - snake_pos[0], food_pos[1] - snake_pos[1])
    overlap = snake_mask.overlap(food_mask, offset)

    if overlap:
        pygame.mixer.Sound.play(eat_sound)
        score += 1
        food_spawn = False
        if score % 5 == 0:
            # Change the background image after eating 5 foods
            background_image = random.choice(background_images)
            background_image = pygame.transform.scale(background_image, (frame_size_x, frame_size_y))
        
    else:
        snake_body.pop()
# Spawning new food within the border
    if not food_spawn:
        food_spawn = True
        if is_animation:
            current_apple_image = random.choice(monster_idle_frames)
        else:
            current_apple_image = random.choice(apple_images)
            
        animation_index = 0
        # Generate random positions within the background image bounds
        border_offset = 20  # Adjust as needed
        max_x = frame_size_x - border_offset - current_apple_image.get_width()
        max_y = frame_size_y - border_offset - current_apple_image.get_height()
        food_pos = [random.randint(border_offset, max_x),
                    random.randint(border_offset, max_y)]

    # Drawing everything
    # Draw food within the border
    if is_animation:
        current_frame = monster_idle_frames[animation_index]
        game_window.blit(current_frame, (food_pos[0], food_pos[1]))
        animation_index = (animation_index + 1) % len(monster_idle_frames)
    else:
        game_window.blit(current_apple_image, (food_pos[0], food_pos[1]))

    # Draw snake within the border
    for pos in snake_body:
        game_window.blit(snake_zone_img, (pos[0], pos[1]))

# Draw border
    pygame.draw.rect(game_window, black, pygame.Rect(0, 0, frame_size_x, frame_size_y),10)
    show_score(1, black, 'consolas', 35)
    show_description()
    show_controls()

    pygame.display.update()
    fps_controller.tick(difficulty)
