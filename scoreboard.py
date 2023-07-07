import pygame.font

class Scoreboard:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Font settings for score and ship count
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Initialize score and ship count
        self.score = 0
        self.ship_count = settings.ship_limit

    def reset(self):
        """Reset the score and ship count"""
        self.score = 0
        self.ship_count = self.settings.ship_limit

    def update_score(self):
        """Update the score display"""
        score_str = "Score: " + str(self.score)
        score_image = self.font.render(score_str, True, self.text_color)
        self.screen.blit(score_image, (10, 10))

    def update_ships(self):
        """Update the remaining ship count display"""
        ship_str = "Ships: " + str(self.ship_count)
        ship_image = self.font.render(ship_str, True, self.text_color)
        self.screen.blit(ship_image, (self.screen_rect.width - ship_image.get_width() - 10, 10))

    def decrease_ship(self):
        """Decrease the ship count"""
        self.ship_count -= 1

    def show_game_over(self):
        """Display the 'game over' message"""
        game_over_text = self.font.render("Game Over", True, self.text_color)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = self.screen_rect.center
        self.screen.blit(game_over_text, game_over_rect)
