import pygame
import os

class Character:
    def __init__(self, x, y, settings):
        self.x = float(x)
        self.y = float(y)
        self.settings = settings

        self.base_width = 250
        self.base_height = 250

        self.velocity_y = 0
        self.is_jumping = False

        self.facing_right = True

        self.frame_index = 0
        self.current_action = "idle"

        # ❤️ HEALTH SYSTEM
        self.max_health = 67
        self.health = 67

        # LEVEL SYSTEM
        self.level = 1
        self.xp = 0

# STAMINA SYSTEM
        self.max_stamina = 100
        self.stamina = 100
        self.is_running = False

# DAMAGE FEEDBACK
        self.hit_flash_timer = 0

# ATTACK COOLDOWN
        self.attack_cooldown = 0
# SWORD SYSTEM
        self.has_sword = False
        self.is_drawing_sword = False
        self.is_attacking = False
        self.is_attack_ending = False

        self.animations = self.load_animations()

    # ---------------- LOAD FRAMES ----------------
    def load_frames(self, folder):
        frames = []

        if not os.path.exists(folder):
            return frames

        for file in sorted(os.listdir(folder)):
            if file.endswith(".png"):
                img = pygame.image.load(os.path.join(folder, file)).convert_alpha()
                img = pygame.transform.scale(img, (self.base_width, self.base_height))
                frames.append(img)

        return frames

    def load_animations(self):
        return {
            "idle": self.load_frames("images/idle"),
            "walk": self.load_frames("images/walk"),
            "run": self.load_frames("images/run"),
            "jump": self.load_frames("images/jump"),
            "draw_sword": self.load_frames("images/draw_sword"),
            "attack_slash": self.load_frames("images/attack_slash"),
            "attack_end": self.load_frames("images/attack_end")
        }

    # ---------------- UPDATE ----------------
    def update(self, keys):
        speed = self.settings.PLAYER_SPEED

        running = keys[pygame.K_LSHIFT]
        if running:
            speed = self.settings.PLAYER_RUN_SPEED

        moving = False

        if keys[pygame.K_RIGHT]:
            self.x += speed
            self.facing_right = True
            moving = True

        if keys[pygame.K_LEFT]:
            self.x -= speed
            self.facing_right = False
            moving = True

        # GRAVITY
        self.velocity_y += self.settings.GRAVITY
        self.y += self.velocity_y

        ground_y = self.settings.START_Y_OFFSET + self.settings.SCREEN_CENTER_Y

        if self.y >= ground_y:
            self.y = ground_y
            self.velocity_y = 0
            self.is_jumping = False

        # ANIMATION
        if self.is_jumping:
            self.current_action = "jump"
        elif moving and running:
            self.current_action = "run"
        elif moving:
            self.current_action = "walk"
        else:
            self.current_action = "idle"

        # 🗡️ DRAW SWORD
        if self.is_drawing_sword:
            self.current_action = "draw_sword"

            if self.frame_index >= len(self.animations["draw_sword"]) - 1:
                self.is_drawing_sword = False
                self.has_sword = True
                self.frame_index = 0

            return


# ⚔️ ATTACK SLASH
        if self.is_attacking:
            self.current_action = "attack_slash"

    # HIT FRAME (adjust later)
            if int(self.frame_index) == 3:
                print("HIT!")

            if self.frame_index >= len(self.animations["attack_slash"]) - 1:
                self.is_attacking = False
                self.is_attack_ending = True
                self.frame_index = 0

            return
        
# 🧩 ATTACK END 
        if self.is_attack_ending:
            self.current_action = "attack_end"

            if self.frame_index >= len(self.animations["attack_end"]) - 1:
                self.is_attack_ending = False
                self.frame_index = 0

            return

    # ---------------- JUMP ----------------
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.settings.JUMP_POWER
            self.is_jumping = True
            self.frame_index = 0

    def attack(self):
    # If sword not drawn → draw first
        if not self.has_sword:
            self.is_drawing_sword = True
            self.frame_index = 0
            return

    # Prevent spam
        if self.is_attacking or self.is_attack_ending:
            return

    # Start attack
        self.is_attacking = True
        self.frame_index = 0

    # ---------------- DAMAGE ----------------
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    # ---------------- DRAW PLAYER ----------------
    def draw(self, screen, camera_x):
        frames = self.animations.get(self.current_action, [])

        if not frames:
            return

        self.frame_index += self.settings.ANIMATION_SPEED

        if self.frame_index >= len(frames):
            if self.current_action in ["draw_sword", "attack_slash", "attack_end"]:
                self.frame_index = len(frames) - 1
            else:
                self.frame_index = 0


        frame = frames[int(self.frame_index)]

        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        rect = frame.get_rect(center=(int(self.x - camera_x), int(self.y)))
        screen.blit(frame, rect)

    # ---------------- DRAW HEALTH BAR ----------------
    def draw_health_bar(self, screen):
        bar_width = 200
        bar_height = 20
        x = 20
        y = 20

        # Background (red)
        pygame.draw.rect(screen, (200, 0, 0), (x, y, bar_width, bar_height))

        # Health (green)
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 200, 0), (x, y, bar_width * ratio, bar_height))

        # Border
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

        # Text
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"{int(self.health)} / {self.max_health}", True, (255,255,255))
        screen.blit(text, (x + 50, y - 2))