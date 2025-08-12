from src.engine.Ninja import Ninja
import os
import pygame
class NinjaGirl(Ninja):
    def __init__(self, x, y, screen_width, screen_height, attack_targets,hero_creation_index,username='Player',loadflag=True,soundflag=True):
        super().__init__(x, y, screen_width, screen_height, attack_targets,hero_creation_index,username)
        self.load_girl_sprites()
        self.hero_creation_index=hero_creation_index
        self.ninja_health_bar=pygame.image.load("src/assets/images/NinjaGirl/health_bar.png")
        self.ninja_health_bar_frame =pygame.image.load("src/assets/images/NinjaGirl/health_bar_frame.png")
        self.ninja_profile_picture = pygame.image.load("src/assets/images/NinjaGirl/profile.png")
        self.SOUND_FLAG=soundflag
        if self.SOUND_FLAG:
            self.hurt_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "NinjaGirl", "ninjagirl hurt.mp3"))
    def hurt(self):
        if self.SOUND_FLAG:
            self.hurt_sound.play()
        self.events.append("ninjagirl hurt")
        if self.health <= 0:
            self.die()

    def load_girl_sprites(self):
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
        
        
        self.SuperPower_pic=pygame.transform.scale(
            pygame.image.load(os.path.join(base_path,"super power.png")),
            (118,118)
        )
        
        sizes=[(70,118),(83,118),(93,108),(102,90),(104,70),(118,78),(118,73),(118,78),(118,78),(118,79)]
        self.death_frames=[]
        for i in range(10):
            self.death_frames.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(base_path,'death',f"Dead__00{i}.png")
                    ),
                    sizes[i]
                )
            )
            
            
    def serialize(self):
        frame_source_name = "idle_frames"
        frame_index_val = 0
        if len(self.guard_drone)==1:
            drone_data=self.guard_drone[0].serialize()
        else:
            drone_data='None'
        if hasattr(self, 'frame_address') and self.frame_address:
             frame_source_name = self.frame_address[0]
             frame_index_val = self.frame_address[1]
             
        data={
            "x_pos": self.x_pos,
            "y_pos": self.y_pos,
            "look": self.Look,
            "health": self.health,
            "username": self.username,
            "frame_source": frame_source_name,
            "frame_index": frame_index_val,
            "character": 'NinjaGirl',
            "creation_index": self.hero_creation_index,
            "events": self.events,
            "drone":drone_data,
        }
        return data