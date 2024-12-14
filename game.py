import pygame
from sys import exit
import random  # Import to randomize snail and fly reappearance

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('RUNNERS')
clock = pygame.time.Clock()
tFont = pygame.font.Font('font/Pixeltype.ttf', 50)

# Load player assets
player_walk_right = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_jump_right = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_walk_left = pygame.transform.flip(player_walk_right, True, False)
player_jump_left = pygame.transform.flip(player_jump_right, True, False)
player_surf = player_walk_right
player_rect = player_surf.get_rect(topleft=(80, 300))

# Load other assets
sky_surface = pygame.image.load('graphics/bgwar.png').convert()
sky_surface = pygame.transform.scale(sky_surface, (800, 400))
ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_surface = pygame.transform.scale(ground_surface, (1000, 100))
ground_rect = ground_surface.get_rect(center=(400, 350))

snail_surface = pygame.image.load('graphics/redtank/tank_red_left.png').convert_alpha()
snail_surface = pygame.transform.scale(snail_surface, (120, 70))
snail_rect = snail_surface.get_rect(bottomright=(200, 300))
fly_surf = pygame.image.load('planes/plane_2/plane_2_red.png').convert_alpha()
fly_surf = pygame.transform.flip(fly_surf, True, False)
fly_surf = pygame.transform.scale(fly_surf, (150, 50))
fly_rect = fly_surf.get_rect(bottomright=(1000, 100))

# Load and scale the flag
bendera_surf = pygame.image.load('graphics/benderaIndonesia.png').convert_alpha()
bendera_surf = pygame.transform.scale(bendera_surf, (player_rect.width, player_rect.height))  # Scale to player size
bendera_rect = bendera_surf.get_rect(center=(player_rect.centerx, player_rect.centery))  # Center the flag on the player

# Load torpedo asset
torpedo_surface = pygame.image.load('planes/torpedo/torpedo.png').convert_alpha()
torpedo_surface = pygame.transform.scale(torpedo_surface, (50, 20))
torpedoes = []  # List to hold active torpedoes

# Flag offset and direction
bendera_offset_x = -30  
bendera_offset_y = 0

# Variables for jump and gravity
player_gravity = 0
player_direction = "right"

# Game state variables
game_active = True
score = 0  # Initialize the score
innitScoreTime = 0
score_stack = []  # Stack to store scores

# Spawn delay variables
snail_spawn_delay = random.randint(30, 60)  # Faster respawn (frames)
snail_timer = snail_spawn_delay

fly_spawn_delay = random.randint(50, 100)  # Faster respawn (frames)
fly_timer = fly_spawn_delay

snail_speed = 2
fly_speed = 6

tick = 60

# Function to display the Game Over screen
def display_game_over():
    screen.fill((255, 255, 255))  # Fill screen with white
    game_over_text = tFont.render('Game Over', False, 'Black')
    game_over_rect = game_over_text.get_rect(center=(400, 150))
    retry_text = tFont.render('Press SPACE to Retry', False, 'Black')
    retry_rect = retry_text.get_rect(center=(400, 250))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(retry_text, retry_rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()

    # Display the last and highest scores
    if score_stack:
        last_score_text = tFont.render(f'Last Score: {score_stack[-1]}', False, 'Black')
        last_score_rect = last_score_text.get_rect(center=(400, 300))
        screen.blit(last_score_text, last_score_rect)

        highest_score = max(score_stack)
        high_score_text = tFont.render(f'High Score: {highest_score}', False, 'Black')
        high_score_rect = high_score_text.get_rect(center=(400, 350))
        screen.blit(high_score_text, high_score_rect)

# Torpedo cooldown
torpedo_cooldown = 3000  # 5 seconds in milliseconds
last_torpedo_time = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Handle jumping in active gameplay
        if game_active:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP) and player_rect.bottom == 300:
                player_gravity = -20

            # Shoot torpedo when DOWN key is pressed and cooldown is over
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                current_time = pygame.time.get_ticks()
                if current_time - last_torpedo_time >= torpedo_cooldown:
                    torpedo_rect = torpedo_surface.get_rect(midleft=player_rect.midright if player_direction == "right" else player_rect.midleft)
                    torpedo_speed = 10 if player_direction == "right" else -10
                    torpedoes.append({"rect": torpedo_rect, "speed": torpedo_speed})
                    last_torpedo_time = current_time

        # Restart game on Game Over screen
        if not game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True
            snail_rect.left = 800
            fly_rect.left = 1000
            player_rect.topleft = (80, 300)
            player_gravity = 0
            score = 0  # Reset score
            snail_timer = random.randint(30, 60)
            fly_timer = random.randint(50, 100)
            snail_speed = 2
            fly_speed = 6

    if game_active:
        # Update score based on time survived
        tick = 60
        tick += 0.01
        current_time = pygame.time.get_ticks() 
        if current_time - innitScoreTime >= 1000: 
            score += 1
            innitScoreTime = current_time

            # Increase snail and fly speed over time
            snail_speed = 2 + score * 0.1
            fly_speed = 6 + score * 0.2

        # Apply gravity
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        if player_rect.bottom < 300:
            if player_direction == "right":
                player_surf = player_jump_right
            else:
                player_surf = player_jump_left
        else:
            if player_direction == "right":
                player_surf = player_walk_right
            else:
                player_surf = player_walk_left

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player_rect.x += 5
            player_direction = "right"
            ground_rect.x -= 5
            if ground_rect.x < -50:
                ground_rect.x = 0
        if keys[pygame.K_a]:
            player_rect.x -= 5
            player_direction = "left"
            ground_rect.x += 5
            if ground_rect.x > 1:
                ground_rect.x = 0

        # Prevent player from leaving the screen
        if player_rect.left <= 0:
            player_rect.left = 0

        # Snail movement
        if snail_timer <= 0:  # Move the snail when the timer is up
            snail_rect.x -= snail_speed
            if snail_rect.right <= 0:
                snail_rect.left = random.randint(800, 900) 
                snail_spawn_delay = random.randint(30, 60)  
                snail_timer = snail_spawn_delay
        else:
            snail_timer -= 1.5  

        # Fly movement
        if fly_timer <= 0:  # Move the fly when the timer is up
            fly_rect.x -= fly_speed
            if fly_rect.right <= 0:
                fly_rect.left = random.randint(900, 1100)  
                fly_spawn_delay = random.randint(50, 100)  
                fly_timer = fly_spawn_delay
        else:
            fly_timer -= 1  

        # Update torpedo positions
        for torpedo in torpedoes[:]:
            torpedo["rect"].x += torpedo["speed"]
            if torpedo["rect"].right < 0 or torpedo["rect"].left > 800:
                torpedoes.remove(torpedo)  # Remove torpedoes that leave the screen

        # Check torpedo collisions with snail and fly
        for torpedo in torpedoes[:]:
            if torpedo["rect"].colliderect(snail_rect):
                snail_rect.left = random.randint(800, 900)  # Respawn snail
                torpedoes.remove(torpedo)
            elif torpedo["rect"].colliderect(fly_rect):
                fly_rect.left = random.randint(900, 1100)  # Respawn fly
                torpedoes.remove(torpedo)

        # Posisi relatif bendera
        if player_direction == "right":
            bendera_rect.center = (player_rect.centerx + bendera_offset_x, player_rect.centery + bendera_offset_y)
        else:
            bendera_rect.center = (player_rect.centerx - bendera_offset_x, player_rect.centery + bendera_offset_y)

        # Draw background and ground
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, ground_rect)
        

        # Render and display score
        score_surf = tFont.render(f'Score: {score}', False, 'Black')
        score_rect = score_surf.get_rect(topright=(750, 25))
        screen.blit(score_surf, score_rect)

        # Draw snail and fly
        screen.blit(snail_surface, snail_rect)
        screen.blit(fly_surf, fly_rect)

        # Draw the flag
        screen.blit(bendera_surf, bendera_rect)

        # Draw player
        screen.blit(player_surf, player_rect)

        # Draw torpedoes
        for torpedo in torpedoes:
            screen.blit(torpedo_surface, torpedo["rect"])

        # Collision detection
        if player_rect.colliderect(snail_rect) or player_rect.colliderect(fly_rect):
            game_active = False
            score_stack.append(score)  # Save the score to stack

    else:
        # Display Game Over screen
        display_game_over()

    # Update display
    pygame.display.update()
    clock.tick(tick)