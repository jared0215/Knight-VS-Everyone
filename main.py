import sys
import pygame
from components.player.player import Player
from components.level.level import Level
from components.enemy.enemy import Enemy
from components.music.music import MusicLoopComponent


def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    player = Player(0, 0, 100)
    level = Level('map/Map.tmx', 1.25)
    clock = pygame.time.Clock()
    debug_font = pygame.font.SysFont(None, 24)
    shift_pressed = False

    enemies = pygame.sprite.Group()
    # Create enemies and add them to the group
    enemy1 = Enemy(100, 100, 40, 10)  # Example enemy
    enemy2 = Enemy(100, 100, 40, 10)  # Example enemy
    enemy3 = Enemy(100, 100, 40, 10)  # Example enemy
    enemy4 = Enemy(100, 100, 40, 10)  # Example enemy
    enemy5 = Enemy(100, 100, 40, 10)  # Example enemy
    enemy6 = Enemy(100, 100, 40, 10)  # Example enemy
    enemy7 = Enemy(100, 100, 40, 10)  # Example enemy
    enemy8 = Enemy(100, 100, 40, 10)  # Example enemy
    enemy9 = Enemy(100, 100, 40, 10)  # Example enemy
    enemy10 = Enemy(100, 100, 40, 10)  # Example enemy
    enemies.add(enemy1, enemy2, enemy3, enemy4, enemy5,
                enemy6, enemy7, enemy8, enemy9, enemy10)

    # # Add Music Loop Component
    # music_loop_component = MusicLoopComponent("data/assets/Song(s)/UH OH!.wav")
    # # Auto play the music when the game starts
    # music_loop_component.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    player.attack(enemies)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and not shift_pressed:
                    player.roll()
                    shift_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    shift_pressed = False

        keys = pygame.key.get_pressed()

        # Update enemies
        enemies.update(player)
        player.update(keys, screen, enemies)

        # Correct drawing order
        screen.fill((0, 117, 57))  # Fill background first
        level.draw(screen)  # Draw the level

        # Draw the enemy
        for enemy in enemies:
            enemy.draw(screen)  # Assuming draw method in Enemy class

        # Draw the player
        player.draw(screen)  # Assuming draw method in Player class

        # Display player's coordinates
        text = debug_font.render(f'x: {player.rect.x}, y: {
            player.rect.y}', True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # ********** D   E   B   U   G   G   I   N   G ***************
        # pygame.font.init()  # Initialize the font module
        # debug_font = pygame.font.SysFont('Arial', 20)  # Create a font object

        # for enemy in enemies:
        #     # Render the enemy's health
        #     health_text = debug_font.render(
        #         # Red color for health
        #         f'Health: {enemy.health}', True, (255, 0, 0))
        #     # Position above the enemy
        #     screen.blit(health_text, (enemy.rect.x, enemy.rect.y - 20))

        #     # Display player's attack damage somewhere on the screen
        #     attack_damage_text = debug_font.render(f'Player Damage: {
        #                                            player_attack_damage}', True, (0, 255, 0))  # Green color for attack damage
        #     screen.blit(attack_damage_text, (10, 10))  # Top-left corner

        # pygame.draw.rect(screen, (255, 255, 0), (0, 0, 50, 50)
        #                  )  # Yellow square at (0, 0)

        # # Red rectangle around the player
        # pygame.draw.rect(screen, (255, 0, 0), player.rect, 1)

        # ********** D   E   B   U   G   G   I   N   G  ***************

        pygame.display.flip()  # Update the display
        clock.tick(60)


if __name__ == "__main__":
    main()
