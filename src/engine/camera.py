from config import screen_width, screen_height ,platform_height

class Camera:
    
    def __init__(self,screen,platforms,enemies,shot_bullets,hero,explosions,scroll,ninja,Arman):
        self.screen=screen
        self.platforms=platforms
        self.enemies=enemies
        self.shot_bullets=shot_bullets
        self.hero=hero
        self.explosions=explosions
        self.scroll=scroll
        self.ninja=ninja
        self.terrorist=Arman
        
        
        
    def render(self):
        
      
        

        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen,self.scroll)

        for enemy in self.enemies:
            enemy.display(self.screen,self.scroll)

        for bullet in self.shot_bullets:
            bullet.draw(self.screen,self.scroll)

        #self.hero.display(self.screen,self.scroll)
        
        self.ninja.display(self.screen, self.scroll)
        self.terrorist.display(self.screen,self.scroll)
        
        # handeling explosions:
        for explosion in self.explosions[:]:
            if not explosion.draw(self.screen,self.scroll):  # If expired, remove it
                self.explosions.remove(explosion)

        
        