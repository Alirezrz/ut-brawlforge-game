from config import screen_width, screen_height ,platform_height

class Camera:
    
    def __init__(self,screen,platforms,enemies,shot_bullets,hero,explosions):
        self.screen=screen
        self.platforms=platforms
        self.enemies=enemies
        self.shot_bullets=shot_bullets
        self.hero=hero
        self.explosions=explosions
        
        
        
        
    def render(self):
        
      
        

        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)

        for enemy in self.enemies:
            enemy.display(self.screen)

        for bullet in self.shot_bullets:
            bullet.draw(self.screen)

        self.hero.display(self.screen)
        
        
        
        # handeling explosions:
        for explosion in self.explosions[:]:
            if not explosion.draw(self.screen):  # If expired, remove it
                self.explosions.remove(explosion)

        
        