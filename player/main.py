import pygame
import sys
import settings as st
from character import Character
from menu import Menu

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = screen.get_size()
clock = pygame.time.Clock()      

st.SCREEN_CENTER_Y = h // 2

menu = Menu(screen)
player = Character(st.START_X, h // 2 + st.START_Y_OFFSET, st)

state = st.MENU

# WORLD SETTINGS
WORLD_WIDTH = 3000
camera_x = 0

# SYSTEM DATA
player_progress = {"unlocked_level": 1}
selected_map = None
game_bg = None


def start_game():
    global camera_x
    player.x = st.START_X
    player.y = h // 2 + st.START_Y_OFFSET
    player.velocity_y = 0
    player.is_jumping = False
    player.health = player.max_health
    camera_x = 0


running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MENU CLICK
        if state == st.MENU:
            action = menu.handle_click(event)
            if action == "start":
                state = st.MAP_SELECT

        # GAME INPUT
        elif state == st.GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

                if event.key == pygame.K_a:
                    player.attack()

    keys = pygame.key.get_pressed()

    # UPDATE GAME

    if state == st.GAME:
        player.update(keys)

        # TEST DAMAGE (press H)
        if keys[pygame.K_h]:
            player.take_damage(1)

    # 💀 GAME OVER
        if player.health <= 0:
            state = st.MAP_SELECT

        # LIMIT PLAYER IN WORLD
        player.x = max(0, min(player.x, WORLD_WIDTH))

        # 🎥 CAMERA FOLLOW (SMOOTH)
        target_x = player.x - w // 2
        camera_x += (target_x - camera_x) * 0.1

        # LIMIT CAMERA
        camera_x = max(0, min(camera_x, WORLD_WIDTH - w))

        # WIN CONDITION
        if player.x > WORLD_WIDTH - 200:
            if player_progress["unlocked_level"] == 1:
                player_progress["unlocked_level"] = 2
            state = st.MAP_SELECT

    
    # DRAW SYSTEM
   

    if state == st.MENU:
        menu.draw()

  
    # MAP SELECT
    
    elif state == st.MAP_SELECT:
        screen.fill((20, 20, 20))

        font = pygame.font.SysFont(None, 60)
        screen.blit(font.render("SELECT MAP", True, (255,255,255)), (w//2 - 150, 50))

        map_keys = list(st.MAPS.keys())
        buttons = []

        for i, key in enumerate(map_keys):
            rect = pygame.Rect(200 + i*220, 300, 180, 120)
            pygame.draw.rect(screen, (0, 200, 0), rect)

            text = font.render(key.upper(), True, (0,0,0))
            screen.blit(text, (rect.x + 20, rect.y + 40))

            buttons.append((rect, key))

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            for rect, key in buttons:
                if rect.collidepoint(pos):
                    selected_map = key
                    game_bg = pygame.image.load(st.MAPS[selected_map]).convert()

                    # 🔥 IMPORTANT: MAKE BG BIGGER THAN SCREEN
                    game_bg = pygame.transform.scale(game_bg, (WORLD_WIDTH, h))

                    state = st.LEVEL_SELECT

    # =========================
    # LEVEL SELECT
    # =========================
    elif state == st.LEVEL_SELECT:
        screen.fill((0, 0, 0))

        font = pygame.font.SysFont(None, 60)
        screen.blit(font.render("SELECT LEVEL", True, (255,255,255)), (w//2 - 160, 100))

        level1 = pygame.Rect(w//2 - 150, 250, 300, 100)
        pygame.draw.rect(screen, (0, 200, 0), level1)
        screen.blit(font.render("LEVEL 1", True, (0,0,0)), (w//2 - 70, 280))

        level2 = pygame.Rect(w//2 - 150, 400, 300, 100)
        unlocked = player_progress["unlocked_level"] >= 2

        pygame.draw.rect(screen, (0, 200, 0) if unlocked else (100,100,100), level2)
        screen.blit(font.render("LEVEL 2", True, (0,0,0)), (w//2 - 70, 430))

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            if level1.collidepoint(pos):
                state = st.GAME
                start_game()

            if level2.collidepoint(pos) and unlocked:
                state = st.GAME
                start_game()

    # =========================
    # 🎮 GAME WITH CAMERA
    # =========================
    elif state == st.GAME:
        if game_bg:
            screen.blit(game_bg, (-camera_x, 0))
        else:
            screen.fill((50, 50, 50))

        # DRAW PLAYER WITH CAMERA OFFSET
        player.draw(screen, camera_x)

        player.draw_health_bar(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()