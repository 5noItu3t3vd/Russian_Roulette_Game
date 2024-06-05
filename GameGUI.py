import pygame
import sys
import os
from config import *
from button import Button
from engine import Engine
from Characters.Player import Player
from textbox import TextBox
from actionhandler import ActionHandler

class GameGUI:
    def __init__(self, mainmenu, name):
        self.mainmenu = mainmenu
        self.name = name
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(BATTLEBGM)
        pygame.mixer.music.set_volume(0.5)


        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Single Player Mode")

        # Load the background image
        self.background_image = pygame.image.load(PLAY_BACKGROUND_IMAGE)
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load the Opponent Image
        self.opponent_image = pygame.image.load(OPPONENT_DEFAULT_IMAGE)
        self.opponent_image = pygame.transform.scale(self.opponent_image, ENEMY_SIZE)
        
        self.round1_image = pygame.image.load(ROUND1IMAGE)
        self.round2_image = pygame.image.load(ROUND2IMAGE)
        self.round3_image = pygame.image.load(ROUND3IMAGE)
        self.round1_image = pygame.transform.scale(self.round1_image, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.round2_image = pygame.transform.scale(self.round2_image, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.round3_image = pygame.transform.scale(self.round3_image, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

        # Load smaller ui
        self.check_grid = pygame.image.load(INFORMATION_BOX_BACKGROUND)
        self.check_grid = pygame.transform.scale(self.check_grid, (SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.9))
        self.check_grid_pos = ((SCREEN_WIDTH - self.check_grid.get_width()) // 2, (SCREEN_HEIGHT - self.check_grid.get_height()) // 2)
        
        # Blinking state
        self.blinking = False
        self.blink_start_time = None
        self.blink_interval = 0.5  # Blink interval in seconds

        # State management
        self.state = INITIAL
        self.special_state = None
        self.last_click_time = 0
        self.click_delay = 0.2  # Delay in seconds to prevent immediate clicks

        # Animation frames
        self.frames = []
        self.frame_size = GUN_ANIMATION_SIZE
        self.center_position = GUN_ANIMATION_POS
        self.animation_running = False

        self.player_animation_dict = {SELF+SUCCEED: [], OPP+SUCCEED: [], SELF+FAIL: [], OPP+FAIL: []}
        self.ai_animation_dict = {SELF+SUCCEED: [], OPP+SUCCEED: [], SELF+FAIL: [], OPP+FAIL: []}

        # Game Engine Variables

        self.engine = Engine(player=Player(name=self.name))
        self.player = self.engine.get_player()
        self.opponent = self.engine.get_opponent()
        self.shotgun = self.engine.get_shotgun()
        self.current_player = self.engine.get_current_player()
        self.other_player = self.engine.get_other_player()

        self.sight = UNKNOWN
        
        self.buttons = []
        self.textbox = None
        self.next_shot = None
        self.shot_counts = None
        self.isExhausted = None
        self.items_used = []
        self.game_round = 1
        
        self.dialogues = DIALOGUES
        self.talk_done = None
        
        self.action_manager = ActionHandler(self, self.engine.get_player(), self.engine.get_opponent())
        
        self.undo_button_var = None
        self.itm_button_var = None
        self.atk_button_var = None
        self.chk_button_var = None
        self.you_button_var = None
        self.opp_button_var = None
        self.sek_button_var = None
        self.pow_button_var = None
        self.heal_button_var = None
        
        
        self.small_icon_size = (SCREEN_WIDTH//20,SCREEN_HEIGHT//20)
        self.heart_img = pygame.image.load(FULL_HEART_IMAGE)
        self.heart_img = pygame.transform.scale(self.heart_img,self.small_icon_size)
        self.noheart_img = pygame.image.load(LOST_HEART_IMAGE)
        self.noheart_img = pygame.transform.scale(self.heart_img,self.small_icon_size)
        
        self.opponent_heart_pos = (512, 168)
        self.player_heart_pos = (989, 650)
        self.heart_spacing = 50 
        
        self.heart_opponent_button_var = None
        self.heart_player_button_var = None
        self.noheart_player_button_var = None
        self.noheart_player_button_var = None
        
            

        # Init functions
        self.initialize_shot_frames()
        self.talk_sequence(self.dialogues, self.start_round)
        # self.initial_buttons()
        # self.start_round()
        
        
        
    def start_round(self,):
        self.engine.reset_all()
        round_image = None
        if self.game_round == 1:
            round_image = self.round1_image
        elif self.game_round == 2:
            round_image = self.round2_image
        elif self.game_round == 3:
            round_image = self.round3_image
        
        if round_image:
            self.animate_round_image(round_image)
            
        self.next_shot = self.engine.start_round(self.game_round)
        self.action()
        
    def wave_start(self):
        if self.special_state:
            self.create_check_buttons()
            
        
        self.engine.reload_all_bullets(self.game_round)
        
        dialogue = [f"You have {self.engine.get_player().itemToString()}", f"Player {self.opponent.name} has {self.engine.get_opponent().itemToString()}"]
        self.talk_sequence(dialogue, self.action)
        
    def action(self):
        
        if type(self.engine.get_current_player()) == Player:
            self.initial_buttons()
        elif self.engine.get_opponent() == self.opponent:
            action = self.engine.get_opponent().get_action(self.shotgun, self.sight)
            self.handle_opponent_action(action)
        else:
            raise AssertionError("This cannot happen")
        
    def handle_opponent_action(self, action):
        if action == LIVE:
            self.state = REVEAL
            self.action_manager.handle_revealer(self.opponent, self.action)
        elif action == BLANK:
            self.state = REVEAL
            self.action_manager.handle_revealer(self.opponent, self.action)
        elif action == HEALING:
            self.state = HEAL
            self.action_manager.handle_healing(self.opponent, self.action)
        elif action == STRENGTH:
            self.state = STRENGTH
            self.action_manager.handle_strength(self.opponent, self.action)
        elif action == OPP:
            self.state = OPP
            self.action_manager.handle_opp(self.opponent, lambda: self.computer_shoot(self.state))
        elif action == SELF:
            self.state = SELF
            self.action_manager.handle_self(self.opponent, lambda: self.computer_shoot(self.state))
        else:
            raise AssertionError("WHAT?")
        
    def computer_shoot(self,decision):
        if decision==SELF:
            result = self.engine.get_opponent().take_damage(self.engine.get_shotgun())
        elif decision==OPP:
            result = self.engine.get_player().take_damage(self.engine.get_shotgun())
        self.play_ending_animation(self.ai_animation_dict[decision+SUCCEED] if result==1 else self.ai_animation_dict[decision+FAIL],decision=decision,result=result)        
        self.take_damage_sequence(decision,result)
        

    def shoot_animation(self,decision):
        if self.next_shot is None:
            raise ValueError("You don't have any more rounds")

        self.play_looping_animation(self.loop_animation, GUN_ANIMATION_POS, decision)
        
    def take_damage_sequence(self,decision,result):
        if decision == OPP:
            if result:
                print("The result was a Success!!!!")
                if self.engine.get_other_player().is_dead():
                    dialogue = [f"{self.engine.get_other_player().get_name()}'s lifepoint is over"]
                    self.state = PLAYERDEAD if type(self.engine.other_player) == Player else OPPDEAD
                    self.talk_sequence(dialogue, self.process_next_wave)
                else:
                    dialogue = [f"{self.engine.get_other_player().get_name()}'s heart has been taken!"]
                    self.state = SWICHTURN
                    self.talk_sequence(dialogue, self.process_next_wave)
            else:
                dialogue = [f"{self.engine.get_other_player().get_name()} survived the shot!","It was a blank shot"]
                self.state = SWICHTURN
                self.talk_sequence(dialogue, self.process_next_wave)

        elif decision == SELF:
            if result:
                print("The result was a Success!!!! But Self.....")
                if self.engine.get_current_player().is_dead():
                    dialogue = [f"{self.engine.get_current_player().get_name()}'s lifepoint is over"]
                    self.state = PLAYERDEAD if type(self.engine.get_current_player()) == Player else OPPDEAD
                    self.talk_sequence(dialogue, self.process_next_wave)
                else:
                    dialogue = [f"{self.engine.get_current_player().get_name()}'s heart has been taken!"]
                    self.state = SWICHTURN
                    self.talk_sequence(dialogue, self.process_next_wave)
            else:
                dialogue = [f"{self.engine.get_current_player().get_name()} survived the shot!","It was a blank shot"]
                self.state = PLAYERAGAIN if type(self.engine.get_current_player())==Player else OPPAGAIN
                self.talk_sequence(dialogue, self.process_next_wave)
        

        
    def talk_sequence(self, dialogues, function=None):
        self.buttons.clear()
        self.textbox = TextBox(font_size=50, pos=MESSAGE_BOX_POS, size=MESSAGE_BOX_SIZE, callback=function)
        self.textbox.add_dialogues(dialogues)
        
    def clear_dialogue(self):
        self.textbox = None

    def round_2_start(self):
        if self.game_round>3:
            self.gameover()
        self.game_round += 1
        self.engine.reset_all()
        self.start_round()
        
    def gameover(self):
        # Game over logic
        if self.state==GAMEOVER:
            print("Player loses!")
        pygame.quit()
        sys.exit()
        
    def process_next_wave(self):
        result = self.state
        self.sight = UNKNOWN
        
        if result==PLAYERDEAD:
            self.state = GAMEOVER
            dialogue = ["It is Game over then"]
            self.talk_sequence(dialogue, self.gameover)
        elif result==OPPDEAD:
            if self.game_round > 3:
                self.state = GAMEOVER
                dialogue = ["You've Won"]
                self.talk_sequence(dialogue, self.gameover)
            else:
                self.state = INITIAL
                dialogue = [f"{self.opponent.get_name()}: ..........."]
                self.talk_sequence(dialogue, self.round_2_start)
        elif result==PLAYERAGAIN:
            self.state = INITIAL
            dialogue = [f"{self.opponent.get_name()}: ...!"]
            self.talk_sequence(dialogue, self.next_turn)
        elif result==OPPAGAIN:
            self.state = OPPTURN
            dialogue = [f"{self.opponent.get_name()}: .....you'll see"]
            self.talk_sequence(dialogue, self.next_turn)
        elif result==SWICHTURN:
            dialogue = [f"{self.opponent.get_name()}: ......"]
            self.engine.role_switch()
            self.talk_sequence(dialogue, self.next_turn)
                        
    def next_turn(self):
        self.textbox = None
        if not self.engine.shotgun.is_exhausted():
            self.wave_start()
        else:
            self.special_state = True
            dialogue = ["Guns are being reloaded"]
            self.talk_sequence(dialogue,self.wave_start)
            
    
    

    def initial_buttons(self):
        self.textbox = None
        dialogue = ["Your Move"]
        self.talk_sequence(dialogue)
        self.buttons.clear()
        self.state = INITIAL
        self.button_functions = [self.create_your_items_button, self.create_attack_buttons, self.create_check_buttons]
        button_x = MAIN_BUTTON_SIZE[0] - 30
        for i in range(3):
            button_y = 230 + i * (MAIN_BUTTON_SIZE[1] + 20)  
            position = (button_x, button_y)
            self.buttons.append(Button(INITIAL_BUTTON_LIST[i], MAIN_BUTTON_SIZE, position, self.button_functions[i]))
        
        self.itm_button_var = self.buttons[0]
        self.atk_button_var = self.buttons[1]
        self.chk_button_var = self.buttons[2]
        
    def create_undo_button(self, prev_button=None):
        if prev_button is None:
            button_y = SCREEN_HEIGHT - UNDO_BUTTON_SIZE[1] - 20
            button_x = 25 + (UNDO_BUTTON_SIZE[0] + 30)
            position = (button_x, button_y)
            self.undo_button_var = Button(UNDO_BUTTON, UNDO_BUTTON_SIZE, position, function=self.undo_button_func)
            self.buttons.append(self.undo_button_var)
            return
            
        self.buttons.append(Button(prev_button.image_path, prev_button.size, prev_button.position, self.undo_button_func))

    def undo_button_func(self):
        if self.special_state == True:
            self.special_state = False
            self.wave_start()

        elif self.state in ['you', 'enemy']:
            self.create_attack_buttons()
            
        elif self.state == INITIAL:
            return
        else:
            self.initial_buttons()

    def create_attack_buttons(self):
        self.buttons.clear()
        self.state = ATTACK
        self.create_undo_button(self.atk_button_var)
        new_button_functions = [self.you_button, self.enemy_button]
        new_button_images = ATTACK_BUTTON_LIST
        button_x = MAIN_BUTTON_SIZE[0]*2
        for i in range(2):
            button_y = (430 + (i-1) * (MAIN_BUTTON_SIZE[1] + (100)))
            position = (button_x, button_y)
            new_button = Button(new_button_images[i], MAIN_BUTTON_SIZE, position, new_button_functions[i])
            new_button.start_animation((int(MAIN_BUTTON_SIZE[0]*1.3), int(MAIN_BUTTON_SIZE[1]*1.3)), frames=10) 
            self.buttons.append(new_button)
                     
    def create_check_buttons(self):
        self.engine.reload_all_bullets(self.game_round)
        self.buttons.clear()
        self.state = CHECK
        
        self.create_undo_button()
        
        # Load bullet images
        self.live_bullet_image = pygame.image.load(LIVE_BULLET_IMAGE)
        self.blank_bullet_image = pygame.image.load(BLANK_BULLET_IMAGE)
        
        # Calculate the size of each bullet image
        grid_height = self.check_grid.get_height()
        bullet_height = int(grid_height * 3 / 10)
        bullet_size = (bullet_height, bullet_height)  # Keep it square for simplicity
        
        self.live_bullet_image = pygame.transform.scale(self.live_bullet_image, bullet_size)
        self.blank_bullet_image = pygame.transform.scale(self.blank_bullet_image, bullet_size)

        # Determine bullet counts
        live_bullets_count = sum(self.engine.shotgun.get_rounds()) 
        blank_bullets_count = len(self.engine.shotgun.get_rounds()) - live_bullets_count

        # Calculate positions to line up the bullets
        bullet_x = self.check_grid_pos[0] + 20  
        live_bullet_y = self.check_grid_pos[1] + 20  
        blank_bullet_y = self.check_grid_pos[1] + self.check_grid.get_height() - 200 - bullet_height

        # Create lists of positions for live and blank bullets
        self.live_bullet_positions = [(bullet_x + 0.5*i * (bullet_size[0] + 10), live_bullet_y) for i in range(live_bullets_count)]
        self.blank_bullet_positions = [(bullet_x + 0.5*i * (bullet_size[0] + 10), blank_bullet_y) for i in range(blank_bullets_count)]

        # Load and position the next shot image
        self.next_shot_image = pygame.image.load(NEXTSHOTREVEAL)
        self.next_shot_image = pygame.transform.scale(self.next_shot_image, bullet_size)  # Same size as bullets
        self.next_result = None
        self.cloud =  pygame.image.load(SIGHT_BUTTON)
        self.cloud = pygame.transform.scale(self.cloud, bullet_size)
        
        
        next_shot_x = self.check_grid_pos[0] + self.check_grid.get_width() - bullet_size[0] - 200 
        next_shot_y = live_bullet_y + 50
        cloud_shot_y = blank_bullet_y
        cloud_shot_x = next_shot_x
        
        
        self.next_shot_position = (next_shot_x, next_shot_y)
        self.cloud_position = (cloud_shot_x,cloud_shot_y)
        self.revealed_shot_position = None
        
        
        
        if self.sight !=UNKNOWN:
            self.next_result = pygame.image.load(LIVE_BULLET_IMAGE) if self.sight==1 else pygame.image.load(BLANK_BULLET_IMAGE)
            self.next_result = pygame.transform.scale(self.next_result, bullet_size)
            revealed_shot_y = blank_bullet_y
            revealed_shot_x = next_shot_x
            self.revealed_shot_position = (revealed_shot_x,revealed_shot_y)



        
    def render_check_screen(self):
        # Draw the smaller background image
        self.screen.blit(self.check_grid, self.check_grid_pos)

        # Draw live bullets
        for pos in self.live_bullet_positions:
            self.screen.blit(self.live_bullet_image, pos)

        # Draw blank bullets
        for pos in self.blank_bullet_positions:
            self.screen.blit(self.blank_bullet_image, pos)

        # Draw next shot image
        self.screen.blit(self.next_shot_image, self.next_shot_position)
        
        if self.sight != UNKNOWN and self.next_result:
            self.screen.blit(self.next_result, self.revealed_shot_position)
        else:
            self.screen.blit(self.cloud, self.cloud_position)

    def animate_round_image(self, image):
        image_rect = image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(0)

        for alpha in range(0, 256, 5):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            self.screen.blit(image, image_rect)
            pygame.display.update()
            pygame.time.delay(30)

        pygame.time.delay(1000)
    
        
    def create_your_items_button(self):
        self.buttons.clear()
        self.state = ITEMS
        self.create_undo_button(self.itm_button_var)
        new_button_functions = [self.your_power_button_func, self.your_heal_button_func, self.your_sight_button_func]
        new_button_images = ITEM_BUTTON_LIST
        
        for i in range(3):
            button_x = 2 * MAIN_BUTTON_SIZE[0] + 30*((-1)**(1+i))
            button_y = 230 + i * (MAIN_BUTTON_SIZE[1] + 20) - (MAIN_BUTTON_SIZE[1] + 20)
            position = (button_x, button_y)
            new_button = Button(new_button_images[i], MAIN_BUTTON_SIZE, position, new_button_functions[i])
            new_button.start_animation((int(MAIN_BUTTON_SIZE[0]*1.3), int(MAIN_BUTTON_SIZE[1]*1.3)), frames=10) 
            self.buttons.append(new_button)

        self.pow_button_var = self.buttons[0]
        self.heal_button_var = self.buttons[1]
        self.sek_button_var = self.buttons[2]
        
    def create_decision_button(self, decision):
        self.buttons.clear()
        new_button_functions = [lambda: self.shoot_button(decision),self.quit_button]
        new_button_images = DECISION_BUTTON_LIST
        button_size = (MAIN_BUTTON_SIZE[0] * 2, MAIN_BUTTON_SIZE[1] * 2)
        button_y = SCREEN_HEIGHT - button_size[1] - 20
        for i in range(2):
            button_x = 300 + i * (button_size[0] + 200)
            position = (button_x, button_y)
            new_button = Button(new_button_images[i], button_size, position, new_button_functions[i])
            new_button.start_animation((int(button_size[0]*1.3), int(button_size[1]*1.3)), frames=10) 
            self.buttons.append(new_button)
            
            
            
            
    
        
    
           
    
            
            

    def your_power_button_func(self):
        if self.engine.player.item_usable(self.shotgun, STRENGTH):
            self.buttons.clear()
            self.state = POWER
            self.action_manager.handle_strength(self.engine.get_player(), self.action)
            
        elif self.engine.get_shotgun().get_damage()==2:
            dialogue = [f"Your shotgun already has {STRENGTH} in this wave!"]
            self.talk_sequence(dialogue, self.create_your_items_button)
            
        else:
            dialogue = ["You don't have that item"]
            self.talk_sequence(dialogue, self.create_your_items_button)
        
    def your_heal_button_func(self):
        if self.engine.player.item_usable(self.shotgun, HEALING):
            self.buttons.clear()
            self.state = HEAL
            self.action_manager.handle_healing(self.engine.get_player(), self.action)

        if self.engine.get_player().get_health()>3:
            dialogue = ["You already have the max health"]
            self.talk_sequence(dialogue, self.create_your_items_button)
        
        else:
            dialogue = ["You don't have that item"]
            self.talk_sequence(dialogue, self.create_your_items_button)
            
    def your_sight_button_func(self):
        
        if self.engine.player.item_usable(self.shotgun, REVEALER):
            self.buttons.clear()
            self.state = REVEAL
            self.sight = self.engine.get_shotgun().get_next_shot()
            self.action_manager.handle_revealer(self.engine.get_player(), self.action)
            
        elif self.sight != UNKNOWN:
            dialogue = [f"You have already used the {REVEALER}, check your magnifying glass"]
            self.talk_sequence(dialogue, self.create_your_items_button)

        else:
            dialogue = ["You don't have that item"]
            self.talk_sequence(dialogue, self.create_your_items_button)

    def you_button(self):
        self.state = SELF
        decision = self.state
        print("You SHOOT SELF")
        self.shoot_animation(decision)
        
    def enemy_button(self):
        self.state = OPP
        decision = self.state
        print("You SHOOT OPP")
        self.shoot_animation(decision)
        
    def shoot_button(self,decision):
        print(f"You shot {self.state}")
        print(f"You are {self.engine.get_player().name}")
        self.buttons.clear()
        if decision==SELF:
            result = self.engine.get_player().take_damage(self.engine.get_shotgun())
        elif decision==OPP:
            result = self.engine.get_opponent().take_damage(self.engine.get_shotgun())
        self.play_ending_animation(self.player_animation_dict[decision+SUCCEED] if result==1 else self.player_animation_dict[decision+FAIL],decision=decision,result=result)        
        self.take_damage_sequence(decision,result)

    def quit_button(self):
        self.buttons.clear()
        self.state = QUIT
        self.create_attack_buttons()







    def initialize_shot_frames(self):
        self.ai_self_soundframe, self.ai_opp_soundframe = AI_SHOT_SOUND_FRAMES[0], AI_SHOT_SOUND_FRAMES[1]
        self.player_self_soundframe, self.player_opp_soundframe = PLAYER_SHOT_SOUND_FRAMES[0], PLAYER_SHOT_SOUND_FRAMES[1]
        
        self.loop_animation = self.load_animation_frames(LOOP_SHOOT)
        """SHOT FRAMES"""
        for index, (n1, playerpath, n2, aipath) in enumerate(zip(PLAYER_SHOT_SOUND_FRAMES, PLAYER_SHOOT_ANIMATIONS, AI_SHOT_SOUND_FRAMES, AI_SHOOT_ANIMATIONS)):
            success_player_frames = self.load_animation_frames(playerpath)
            fail_player_frames = self.load_animation_frames(playerpath, n1)
            success_ai_frames = self.load_animation_frames(aipath)
            fail_ai_frames = self.load_animation_frames(aipath, n2)
            
            if index == 0:
                self.player_animation_dict[SELF + SUCCEED].extend(success_player_frames)
                self.player_animation_dict[SELF + FAIL].extend(fail_player_frames)
                self.ai_animation_dict[SELF + SUCCEED].extend(success_ai_frames)
                self.ai_animation_dict[SELF + FAIL].extend(fail_ai_frames)
            elif index == 1:
                self.player_animation_dict[OPP + SUCCEED].extend(success_player_frames)
                self.player_animation_dict[OPP + FAIL].extend(fail_player_frames)
                self.ai_animation_dict[OPP + SUCCEED].extend(success_ai_frames)
                self.ai_animation_dict[OPP + FAIL].extend(fail_ai_frames)

    def load_animation_frames(self, folder,fail_frame=None):
        frames = []
        frames_index = 0
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.png'):
                frame = pygame.image.load(os.path.join(folder, filename))
                frame = pygame.transform.scale(frame, self.frame_size)
                frames.append(frame)
                if fail_frame and frames_index == fail_frame:
                    break
                frames_index +=1
            
        return frames

    def play_ending_animation(self, frames, decision=None,position=None,result=None):
        if position is None:
            position = self.center_position
        frame_index = 0
        
        for frame in frames:
            
            if result==1:
                if self.engine.get_current_player()==self.engine.get_player():
                    if decision == SELF and frame_index == self.player_self_soundframe:
                        play_mp3(GUN_SHOT_SOUND)
                        
                    elif decision == OPP and frame_index == self.player_opp_soundframe:
                        play_mp3(GUN_SHOT_SOUND)
                elif self.engine.get_current_player()==self.engine.get_opponent():
                    if decision == SELF and frame_index == self.ai_self_soundframe:
                        play_mp3(GUN_SHOT_SOUND)
                    elif decision == OPP and frame_index == self.ai_opp_soundframe:
                        play_mp3(GUN_SHOT_SOUND)
            _num = 0    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    _num += 1
                    return _num==2 # End the animation early if the mouse is clicked

            # Clear the screen by drawing the background
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.opponent_image, ENEMY_POS)

            self.screen.blit(frame, position)
            for button in self.buttons:
                button.draw(self.screen)
            pygame.display.flip()

            frame_index += 1
            pygame.time.delay(100)
        
        if result == 0:
            frozen_play(GUN_BLANK_SOUND)

    def play_looping_animation(self, frames, position, decision):
        if position is None:
            position = self.center_position
        self.animation_running = True
        frame_index = 0

        # Clear previous buttons and add a small delay
        self.buttons.clear()
        pygame.display.flip()
        self.create_decision_button(decision)

        while self.animation_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_clicked(event.pos):
                            button.click()
                            self.animation_running = False
                            break

            if not self.animation_running:
                break

            # Clear the screen by drawing the background
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.opponent_image, ENEMY_POS)

            self.screen.blit(frames[frame_index], position)
            for button in self.buttons:
                button.draw(self.screen)
            pygame.display.flip()

            frame_index = (frame_index + 1) % len(frames)
            pygame.time.delay(100)    
        

    def start_blinking(self):
        self.blinking = True if self.items_used else False
        self.blink_start_time = time.time()

    def update_blinking(self):
        if self.blinking:
            current_time = time.time()
            elapsed_time = current_time - self.blink_start_time
            if elapsed_time > 10:
                self.blinking = False
                for button in self.buttons:
                    button.blink(True)
                    break
            else:
                blink_state = int(elapsed_time / self.blink_interval) % 2 == 0
                for button in self.buttons:
                    button.blink(blink_state)
                    break
                
    def engine_linker(self):
            self.player = self.engine.get_player()
            self.opponent = self.engine.get_opponent()
            self.shotgun = self.engine.get_shotgun()
            self.current_player = self.engine.get_current_player()
            self.other_player = self.engine.get_other_player()

    def print_coordinates(self, pos):
        print(f"Mouse clicked at: {pos}")

    def run(self):
        pygame.mixer.music.play(-1)
        self.start_blinking()
        running = True
        while running:
            self.engine_linker()
            for event in pygame.event.get():
                self.engine_linker()
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.print_coordinates(event.pos)
                    current_time = time.time()
                    if self.textbox and self.textbox.is_clicked(event.pos):
                        self.textbox.click()
                    elif current_time - self.last_click_time > self.click_delay:
                        self.last_click_time = current_time
                        for button in self.buttons:
                            self.engine_linker()
                            if button.is_clicked(event.pos):
                                button.click()
                                break

            self.update_blinking()
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.opponent_image, ENEMY_POS)

            if self.textbox:
                self.textbox.update()
                self.textbox.draw(self.screen)

            for button in self.buttons:
                button.update()  # Update button animations
                button.draw(self.screen)

            # Render the check screen if in CHECK state
            if self.state == CHECK:
                self.render_check_screen()

            pygame.display.flip()

        pygame.mixer.music.stop()
        self.mainmenu.run()
        pygame.quit()
        sys.exit()
