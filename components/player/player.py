import pygame
from paths import KNIGHT_DIR


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__()
        self.x = x
        self.y = y
        self.health = health

        self.attack_damage = 10  # Set the damage value for each attack
        self.attack_damage_frames = [2, 5]  # Frames where damage is dealt
        # Count of frames where damage has been dealt in the current attack
        self.damage_dealt_frames = set()  # Track frames where damage has been dealt

        # Load sprite sheets
        self.idle_sheet = pygame.image.load(
            KNIGHT_DIR / "_Idle.png").convert_alpha()
        self.run_sheet = pygame.image.load(
            KNIGHT_DIR / "_Run.png").convert_alpha()
        self.attack_sheet = pygame.image.load(
            KNIGHT_DIR / "_AttackComboNoMovement.png").convert_alpha()
        self.roll_sheet = pygame.image.load(
            KNIGHT_DIR / "_Roll.png").convert_alpha()

        # Scaling factor for the sprite size
        scale_factor = 1.5

        # Load frames for animations
        self.idle_frames = self.load_frames_from_sheet(
            self.idle_sheet, 10, scale_factor)
        self.run_frames = self.load_frames_from_sheet(
            self.run_sheet, 10, scale_factor)
        self.attack_frames = self.load_frames_from_sheet(
            self.attack_sheet, 10, scale_factor)
        self.roll_frames = self.load_frames_from_sheet(
            self.roll_sheet, 12, scale_factor)

        # Set the initial animation to idle
        self.frames = self.idle_frames

        # Initialize the current frame and its image
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Setting initial position
        self.rect.x = 0
        self.rect.y = 0

        # Player attributes
        self.facing_right = True
        self.is_attacking = False
        self.is_rolling = False
        self.speed = 2  # Normal walking speed
        self.roll_speed = 4  # Faster speed for rolling

        # Initialize last_update for animation timing
        self.last_update = pygame.time.get_ticks()
        # Animation frame rate in milliseconds
        self.frame_rate = 60

    def load_frames_from_sheet(self, sheet, frame_count, scale_factor):
        # Assuming the frames are arranged horizontally in the sprite sheet
        sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // frame_count

        frames = []
        for frame_number in range(frame_count):
            frame = pygame.Surface(
                (frame_width, sheet_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (frame_number *
                                       frame_width, 0, frame_width, sheet_height))

            # Get the bounding rectangle of the non-transparent area
            bounding_rect = frame.get_bounding_rect()

            # Create a new Surface with the size of the bounding rectangle and blit the frame onto it
            cropped_frame = pygame.Surface(bounding_rect.size, pygame.SRCALPHA)
            cropped_frame.blit(frame, (0, 0), bounding_rect)

            # Scale the frame
            scaled_frame = pygame.transform.scale(cropped_frame, (int(
                bounding_rect.width * scale_factor), int(bounding_rect.height * scale_factor)))

            frames.append(scaled_frame)

        return frames

    def update(self, keys, screen, enemies):
        """Update the player's position and animation based on input."""
        self.is_moving = False

        # Movement logic
        if self.is_rolling:
            movement_speed = self.roll_speed
            self.rect.x += movement_speed if self.facing_right else -movement_speed

        # Key press logic
        if not self.is_attacking and not self.is_rolling:
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
                self.is_moving = True
                self.facing_right = False
            if keys[pygame.K_d]:
                self.rect.x += self.speed
                self.is_moving = True
                self.facing_right = True
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
                self.is_moving = True
            if keys[pygame.K_s]:
                self.rect.y += self.speed
                self.is_moving = True

        # Determine current frames based on action
        if self.is_attacking:
            self.frames = self.attack_frames
        elif self.is_rolling:
            self.frames = self.roll_frames
        elif self.is_moving:
            self.frames = self.run_frames
        else:
            self.frames = self.idle_frames

        self.animate()
        # Boundary conditions
        self.apply_boundaries()

        if self.is_attacking:
            # Deal damage on specific frames
            if self.current_frame in self.attack_damage_frames:
                if self.current_frame not in self.damage_dealt_frames:
                    self.deal_damage(enemies)
                    self.damage_dealt_frames.add(self.current_frame)

            # Reset damage dealt frames if the attack animation is over
            if self.current_frame == 0:
                self.damage_dealt_frames.clear()

    def animate(self):
        """Handles the animation of the sprite."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

            # Reset attack or roll animation at the end of its sequence

            if self.is_attacking and self.current_frame == 0:
                self.is_attacking = False
                self.frames = self.idle_frames

            elif self.is_rolling and self.current_frame == 0:
                self.is_rolling = False
                self.frames = self.idle_frames

    def apply_boundaries(self):
        """Applies boundary conditions to keep the player within the screen."""
        map_width, map_height = 1200, 800
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > map_width:
            self.rect.right = map_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > map_height:
            self.rect.bottom = map_height

    # Player actions

    def attack(self, enemies):
        if not self.is_attacking:
            self.is_attacking = True
            self.is_rolling = False
            self.frames = self.attack_frames
            self.current_frame = 0
            # Reset damage dealt frames at the start of attack
            self.damage_dealt_frames.clear()

    def attack_area(self):
        """Define the attack range."""
        attack_range = 50
        attack_area_height = self.rect.height

        if self.facing_right:
            return pygame.Rect(self.rect.right, self.rect.y, attack_range, attack_area_height)
        else:
            return pygame.Rect(self.rect.left - attack_range, self.rect.y, attack_range, attack_area_height)

    def roll(self):
        """Handles the roll action."""
        if not self.is_rolling:
            self.is_attacking = False
            self.is_rolling = True
            self.frames = self.roll_frames
            self.current_frame = 0

    def draw(self, screen):
        """Draws the player sprite on the screen."""
        screen.blit(self.image, self.rect.topleft)

    def take_damage(self, damage):
        self.health -= damage

    def deal_damage(self, enemies):
        for enemy in enemies:
            # Check for collision with enemy in the attack area
            if self.attack_area().colliderect(enemy.rect):
                enemy.take_damage(self.attack_damage)
