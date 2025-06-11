import pygame

class InputHandler:
    def __init__(self, hero, bullet_class, shot_bullets):
        self.hero = hero
        self.bullet_class = bullet_class
        self.shot_bullets = shot_bullets

        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        self.shooting_triggered = False

    def handle_keyboard(self):
        keys = pygame.key.get_pressed()
        self.hero.is_moving_horizontally = False
        
        if keys[pygame.K_d]:
            self.hero.move_right()
            self.hero.is_moving_horizontally = True
        if keys[pygame.K_a]:
            self.hero.move_left()
            self.hero.is_moving_horizontally = True
        if keys[pygame.K_SPACE]:
            self.hero.jump()
        if keys[pygame.K_r]:
            self.hero.respawn()
        if keys[pygame.K_j]:
            self.hero.activate_jetpack()

    def handle_gamepad(self):
        if not self.joystick:
            return

        axis_x = self.joystick.get_axis(0)
        trigger_r2 = self.joystick.get_axis(5)  # R2 usually axis 5
        l1 = self.joystick.get_button(4)  # L1
        r1 = self.joystick.get_button(5)  # R1
        a_button = self.joystick.get_button(0)  # Jump

        if axis_x > 0.2:
            self.hero.move_right()
            self.hero.is_moving_horizontally = True
        elif axis_x < -0.2:
            self.hero.move_left()
            self.hero.is_moving_horizontally = True

        if a_button:
            self.hero.jump()

        if trigger_r2 > 0.5:
            if not self.shooting_triggered:
                self.hero.shoot(self.shot_bullets, self.bullet_class)
                self.shooting_triggered = True
        else:
            self.shooting_triggered = False 

        if l1 and r1:
            self.hero.respawn()

    def handle_all_inputs(self):
        self.handle_keyboard()
        self.handle_gamepad()
