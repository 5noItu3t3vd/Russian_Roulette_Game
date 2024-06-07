import pygame
import time
from PIL import Image
import os
import sys
import random
from pydub import AudioSegment
from pydub.playback import play
from playaudio import play_mp3
from playaudio import frozen_play
from collections import Counter
import threading

# random.seed(1)

# STRING VARIABLES
REVEAL = 'reveal'
ITEMS = 'items'
HEAL = 'heal'
POWER = 'power'
QUIT = 'quit'
CHECK = 'check'
SHOOT = 'shoot'
SELF = 'self'
OPP = 'opp'
DECISION = 'decision'

INITIAL = 'initial'
GAMEOVER = 'gameover'

TALK = 'talk'
LIVE = 'live'
BLANK = 'blank'
ATTACK = 'attack'
UNKNOWN = 'unknown'

SUCCEED = 'succeed'
FAIL = 'fail'

SELFSUC = 'selfsuc'
SELFAIL = 'selffail'
OPPSUC = 'oppsuc'
OPPFAIL = 'oppfail'

DEATH = 'death'
SWICHTURN = 'swichturn'

PLAYERDEAD ='playerdead'
PLAYERAGAIN = 'playeragain'

OPPDEAD = 'oppdead'
OPPNEXTROUND = 'oppnextround'
OPPAGAIN = 'oppagain'
OPPTURN = 'oppturn'

AI = "ai"
PLAYER = "player"



CLOUD_IMAGE = "resources//cloud.png"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

MAIN_BUTTON_SIZE = (100,100)

SINGLEPLAYER_BUTTON_POS = (523,393)
SINGLEPLAYER_BUTTON_SIZE = (922-SINGLEPLAYER_BUTTON_POS[0],442-SINGLEPLAYER_BUTTON_POS[1])

MULTIPLAYER_BUTTON_POS = (538, 473)
MULTIPLAYER_BUTTON_SIZE = (907-MULTIPLAYER_BUTTON_POS[0],525-MULTIPLAYER_BUTTON_POS[1])

CREDITS_BUTTON_POS = (604, 662)
CREDITS_BUTTON_SIZE = (831-CREDITS_BUTTON_POS[0],714-CREDITS_BUTTON_POS[1])

INSTRUCTIONS_BUTTON_POS = (532, 575)
INSTRUCTIONS_BUTTON_SIZE = (913-INSTRUCTIONS_BUTTON_POS[0],599-INSTRUCTIONS_BUTTON_POS[0])

MAIN_MENU_BACKGROUND_IMAGE = "resources\\mainmenyu.png"
PLAY_BACKGROUND_IMAGE = "resources\\playbackground_new.png"
MAIN_MENU_BUTTONS = "resources\mainbutton.png"
MAINMENU_BGM = "resources\\START.mp3"

INFORMATION_BOX_BACKGROUND = 'resources\\information_box.png'
LIVE_BULLET_IMAGE = 'resources\\live.png'
BLANK_BULLET_IMAGE = 'resources\\blank.png'

ATTACK_BUTTON = "resources\\ATTACKKKK.png"
CHECK2_BUTTON = "resources\\TAKEALOOK.png"
ITEM_BUTTON = "resources\\ITEMMMMMMMM.png"
ENEMY_BUTTON = "resources\\ENEMYLOGO.png"
HEAL_BUTTON = "resources\\HEALLLLL.png"
YOU_BUTTON = "resources\YOU.  UUUU.png"
SIGHT_BUTTON = "resources\\revealer.png"
POWER_BUTTON = "resources\powerup.png"
QUIT_BUTTON = "resources\QUIT2.png"
SHOOT_BUTTON = "resources\\SHOOOT.png"

GUN_ANIMATION_SIZE = (600*1.1,472*1.1)
GUN_ANIMATION_POS = (350,20)

UNDO_BUTTON = "resources\\buttons\\back1.png"
# UNDO_BUTTON = "resources\\buttons\\back2.png"
UNDO_BUTTON_SIZE = (75,75)

INITIAL_BUTTON_LIST = [ITEM_BUTTON,ATTACK_BUTTON,CHECK2_BUTTON]
ITEM_BUTTON_LIST = [POWER_BUTTON,HEAL_BUTTON,SIGHT_BUTTON]
ATTACK_BUTTON_LIST = [YOU_BUTTON,ENEMY_BUTTON]
DECISION_BUTTON_LIST = [SHOOT_BUTTON,QUIT_BUTTON]

NEXTSHOTREVEAL = "resources\\NEXT!!!!!!.png"

SUCCEED_SELF_SHOOT = "resources\\Succeed_Self_Shot"
SUCCEED_OPP_SHOOT = "resources\\Succeed_Opp_Shot"
# FAIL_SELF_SHOT = "resources\\Failed_Self_Shot"
# FAIL_OPP_SHOT = "resources\\Failed_Opp_Shot"

SUCCEED_AI_SELF = "resources\\SUCCEED_AI_SELF"
SUCCEED_AI_OPP = "resources\\SUCCEED_AI_OPP"
# FAIL_AI_SELF = "resources\\AI_FAIL_SELF"
# FAIL_AI_OPP = "resources\\AI_FAIL_OPP"

# PLAYER_SHOOT_ANIMATIONS = [SUCCEED_SELF_SHOOT,SUCCEED_OPP_SHOOT,FAIL_SELF_SHOT,FAIL_OPP_SHOT]
# AI_SHOOT_ANIMATIONS = [SUCCEED_AI_SELF,SUCCEED_AI_OPP,FAIL_AI_SELF,FAIL_AI_OPP]
PLAYER_SHOOT_ANIMATIONS = [SUCCEED_SELF_SHOOT,SUCCEED_OPP_SHOOT] #.extend([SUCCEED_SELF_SHOOT,SUCCEED_OPP_SHOOT])
AI_SHOOT_ANIMATIONS = [SUCCEED_AI_SELF,SUCCEED_AI_OPP] #.extend([SUCCEED_AI_SELF,SUCCEED_AI_OPP])

PLAYER_SHOT_SOUND_FRAMES = [102,51]
AI_SHOT_SOUND_FRAMES = [50,34]


LOOP_SHOOT = "resources\\looping_holder"

ROUND1IMAGE = "resources\\ROUND ! 11.png"
ROUND2IMAGE = "resources\\ROUND22222.png"
ROUND3IMAGE = "resources\\ROUND 333.png"


OPPONENT_DEFAULT_IMAGE = "resources\\enemy4.png"

# ENEMY_SIZE = (800,800)
# ENEMY_POS = (245, 0)
ENEMY_SIZE = (1180,820)
ENEMY_POS = (75, 30)

# Dialogue stuff
DIALOGUES = ["Holy Macaronia"]

MESSAGE_BOX = "resources\\message_box.png"
MESSAGE_BOX_SIZE = (800,190)
MESSAGE_BOX_POS = (257,569)

INDICATOR_PNG = "resources\\indicator.png"
INDICATOR_SIZE = (50,50)


# Items
HEALING = "Health Kit"
STRENGTH = "Gun Power"
REVEALER = "Revealer"

INITIAL_ITEMS_COMP = {
            HEALING: 0,
            STRENGTH: 0,
            REVEALER: 0
}

INITIAL_ITEMS_SELF = {
            HEALING: 0,
            STRENGTH: 0,
            REVEALER: 0
}
        
#Other UI stuff

FULL_HEART_IMAGE = "resources\LIFE FULL.png"
LOST_HEART_IMAGE = "resources\\LIFE ))))0000.png"

PLAYER_HEART_TEXT = "resources\\your life.png"
OPPONENT_HEART_TEXT = "resources\\ENEMY LIFE POINT.png"

TRUE_BULLET_IMAGE = "resources\実弾.png"    

# SOUND
POWER_UP_SOUND = "resources\\soundeffects\\powerupbgm.mp3"
HEAL_SOUND = "resources\\soundeffects\\healing.mp3"
REVEAL_SOUND = "resources\soundeffects\\revealerused.mp3"

RELOAD_SOUND = "resources\\soundeffects\\reloading.mp3"
GUN_SHOT_SOUND = "resources\\soundeffects\\shooting.mp3"
GUN_BLANK_SOUND = "resources\\soundeffects\\it was a blank.mp3"


BATTLEBGM = "resources\\soundeffects\\fight_bgm.mp3"
BUTTON_SOUND = "resources\ITEM_SELECT_BUTTON.mp3"
ATTACK_SOUND = "resources\soundeffects\clicking.mp3"
TPING_SOUND = "resources\soundeffects\keybouardtyping.mp3"
LAST_HEART_SOUND = "resources\soundeffects\lifepoint_only1.mp3"
HURT_HEART_SOUND = "resources\soundeffects\lifepoint_only2.mp3"