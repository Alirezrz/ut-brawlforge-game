from src.engine.Ninja import Ninja
import os
import pygame
class NinjaGirl(Ninja):
    def __init__(self, x, y, screen_width, screen_height, attack_targets, health_bar_frame=None, health_bar=None):
        super().__init__(x, y, screen_width, screen_height, attack_targets, health_bar_frame, health_bar)
        self.load_girl_sprites()
        self.hurt=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "ninja girl", "ninjagirl hurt.mp3"))
          
    def hurt(self):
        self.hurt.play()

    def load_girl_sprites(self):
        # Replace this with code that loads the girl's custom animations
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "NinjaGirl")
        # Load Idle frames
        self.idle_frames = []
        for i in range(0, 10): 
            img_path = os.path.join(base_path, "Idle", f"Idle__00{i}.png")
            tmp = pygame.image.load(img_path)
            self.idle_frames.append(pygame.transform.scale(tmp, (68, 118)))

        # Load Run frames
        size=[82,77,77,90,88,82,78,78,83,84]
        self.run_frames = []
        for i in range(1, 10):
            img_path = os.path.join(base_path, "Run", f"Run__00{i}.png")
            tmp = pygame.image.load(img_path)
            self.run_frames.append(pygame.transform.scale(tmp, (size[i], 118)))
            
        # Load Jump frames
        self.jump_frames = []
        sizes = [75, 70,71,71,72,71,78,77,79,79]
        for i in range(0, 10):
            img_path = os.path.join(base_path, "Jump", f"Jump__00{i}.png")
            tmp = pygame.image.load(img_path)
            self.jump_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))  
            
        # Load Kunai
        img_path = os.path.join(base_path, "Kunai.png")
        self.Kunai_pic = pygame.image.load(img_path)
        self.Kunai_pic = pygame.transform.scale(self.Kunai_pic, (60, 12))
        
        img_path = os.path.join(base_path, "FiredKunai.png") 
        self.Fired_kunai_pic=pygame.image.load(img_path)
        self.Fired_kunai_pic= pygame.transform.scale(self.Fired_kunai_pic, (70, 24))
        
        self.Kunai=self.Kunai_pic
        
        # Load Throw frames
        self.throw_frames = []
        throw_widths = [70,68,73,85,69,68,68,77,73,67]
        for i in range(10):
            img_path = os.path.join(base_path, "Throw", f"Throw__00{i}.png")
            tmp = pygame.image.load(img_path)
            scaled = pygame.transform.scale(tmp, (throw_widths[i], 118))
            self.throw_frames.append(scaled)
          
        # Load Jump throw frames
        self.jumpThrow_frames = []
        sizes = [79,77,82,92,94,97,95,89,80,79]
        for i in range(0, 10):
            img_path = os.path.join(base_path, "JumpThrow", f"Jump_Throw__00{i}.png")
            tmp = pygame.image.load(img_path)
            self.jumpThrow_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))
            
            
        self.Attack_frames=[]
        sizes = [70,70,76,118,121,130,129,127,124,118]
        self.with_sword_width= [70,70,76,69,84,94,92,91,99,91]
        for i in range(0, 10):
            img_path = os.path.join(base_path, "Attack", f"Attack__00{i}.png")
            tmp = pygame.image.load(img_path)
            self.Attack_frames.append(pygame.transform.scale(tmp, (sizes[i], 118)))
            
        self.JumpAttack_frames=[]
        self.jumpattack_sizes=[(71,118),(67,118),(68,118),(108,118),(108,118),(115,128),(118,133),(119,134),(118,129),(92,118)]
        for i in range(0, 10):
            img_path = os.path.join(base_path, "JumpAttack", f"Jump_Attack__00{i}.png")
            tmp = pygame.image.load(img_path)
            self.JumpAttack_frames.append(pygame.transform.scale(tmp, self.jumpattack_sizes[i]))
            
        self.freezed_frame=pygame.transform.scale(
            pygame.image.load(os.path.join(base_path,"freezed.png")),
            (68,118)
        )
