import pygame
from paths import ASSETS_DIR
import time
import random

SKELETONS_DIR = ASSETS_DIR / "Skeleton"
ORCS_DIR = ASSETS_DIR / "Orc_Berserk"


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health, damage):
        super().__init__()
        self.x = x
        self.y = y
        # self.width = width
        # self.height = height
        # self.hitbox = (self.x, self.y, self.width, self.height)

        # Set up the sprite sheets
        self.idle_sheet = pygame.image.load(
            SKELETONS_DIR / "Idle.png").convert_alpha()
        self.run_sheet = pygame.image.load(
            SKELETONS_DIR / "Run.png").convert_alpha()
        self.attack_sheet = pygame.image.load(
            SKELETONS_DIR / "Attack_1.png").convert_alpha()
        self.dead_sheet = pygame.image.load(
            SKELETONS_DIR / "Dead.png").convert_alpha()
        self.hurt_sheet = pygame.image.load(
            SKELETONS_DIR / "Hurt.png").convert_alpha()

        # Scale the sprite sheets
        scale_factor = 1

        # Load the frames for animations
        self.idle_frames = self.load_frames_from_sheet(
            self.idle_sheet, 7, scale_factor)
        self.run_frames = self.load_frames_from_sheet(
            self.run_sheet, 7, scale_factor)
        self.attack_frames = self.load_frames_from_sheet(
            self.attack_sheet, 7, scale_factor)
        self.dead_frames = self.load_frames_from_sheet(
            self.dead_sheet, 3, scale_factor)
        self.hurt_frames = self.load_frames_from_sheet(
            self.hurt_sheet, 3, scale_factor)

        # Set the initial animation to idle
        self.frames = self.idle_frames

        # Initialize the current frame and its image
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Setting initial position
        self.rect.x = random.randint(0, 1200)
        self.rect.y = random.randint(0, 800)

        # Player attributes
        self.facing_right = True
        self.is_facing_left = False
        self.is_attacking = False
        self.is_moving = False
        self.can_move = True
        self.is_hurt = False
        self.is_dead = False
        self.is_dying = False
        self.speed = 1  # Normal walking speed
        self.health = health
        self.max_health = health
        self.damage = damage
        self.death_time = 0  # Time when death animation ends
        self.death_delay = 5000  # Delay in milliseconds before removal
        self.hurt_time = 0  # Time when hurt animation ends
        self.hurt_duration = 100  # Delay in milliseconds before removal

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

    def update(self, player):
        """Update the enemy's position and animation based on player's position."""
        if self.is_dying:
            if self.death_time == 0:
                self.death_time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.death_time > self.death_delay:
                self.kill()  # Remove the enemy after the delay
                return  # Stop further processing

            # Play the death animation
            self.frames = self.dead_frames
            self.animate()
        else:
            # Handle hurt state
            if self.is_hurt:
                if pygame.time.get_ticks() - self.hurt_time > self.hurt_duration:
                    self.is_hurt = False
                    self.frames = self.idle_frames  # Reset to idle frames
                    self.can_move = True  # Re-enable movement after being hurt
                else:
                    self.frames = self.hurt_frames
                    self.can_move = False  # Disable movement while hurt
            elif self.is_moving:
                # Switch to moving animation
                self.frames = self.run_frames
            else:
                # Switch back to idle animation
                self.frames = self.idle_frames

            # Move towards player if not hurt or dying
            if not self.is_hurt and not self.is_dying:
                self.move_towards_player(player)

            self.animate()

            # Check if the enemy's health has reached zero and is not already dying
            if self.health <= 0 and not self.is_dying:
                self.is_dying = True  # Mark as dying to start the death animation
                self.current_frame = 0
                self.death_time = 0
                self.death_delay = 5000  # 5000 milliseconds delay

    def move_towards_player(self, player):
        """Move the enemy towards the player, including diagonally, if not immobilized."""
        if not self.can_move:
            # Stop the movement if the enemy is not allowed to move
            self.is_moving = False
            return

        self.is_moving = True
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distance = (dx**2 + dy**2)**0.5

        if distance != 0:
            # Normalize the direction vector
            dx, dy = dx / distance, dy / distance

            # Move the enemy
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            # Check if the enemy should flip based on the direction
            if dx < 0:
                # Enemy is moving left, flip the sprite
                self.is_facing_left = True
            else:
                # Enemy is moving right, use the sprite's original orientation
                self.is_facing_left = False

    def animate(self):
        """Update the enemy's animation based on its current frame."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1

            # Reset the animation at the end of its sequence
            if self.current_frame >= len(self.frames):
                if self.is_dying:
                    # If the enemy is dying, stop the animation at the last frame
                    self.current_frame = len(self.frames) - 1
                else:
                    # Otherwise, loop the animation
                    self.current_frame = 0

            self.image = self.frames[self.current_frame]

            # Flip the image if the enemy is facing left
            if self.is_facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

            # Reset the attack animation at the end of its sequence
            if self.is_attacking and self.current_frame == len(self.frames) - 1:
                self.is_attacking = False

            # Remove the enemy from the game after its death animation has finished playing
            if self.is_dead and self.current_frame == 0:
                self.kill()  # This removes the enemy from all groups it's a member of

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

    # Enemy actions
    def attack(self):
        """Handles the attack action."""
        if not self.is_attacking:
            self.is_attacking = True
            self.frames = self.attack_frames
            self.current_frame = 0

    def hurt(self):
        """Play the hurt animation and immobilize briefly."""
        self.is_hurt = True
        self.frames = self.hurt_frames
        self.current_frame = 0
        self.hurt_time = pygame.time.get_ticks()  # Start the hurt timer
        # Set a timer for re-enabling movement, can be same as hurt_duration
        self.immobilize_time = pygame.time.get_ticks()

    def die(self):
        """Handles the death action."""
        if not self.is_dead:
            self.is_dead = True
            self.frames = self.dead_frames
            self.current_frame = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health > 0:
            self.hurt()
            self.can_move = False  # Disable movement when hurt

    def draw(self, screen):
        """Draws the enemy sprite and a health bar on the screen."""
        # Draw the sprite
        screen.blit(self.image, self.rect.topleft)

        # Check if health bar should be drawn
        if self.health > 0:
            # Draw the health bar
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x,
                             self.rect.y - 20, 100, 10))  # Red bar
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y -
                             # Green bar
                                                   20, 100 * (self.health / self.max_health), 10))
