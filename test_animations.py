import pygame
import sys
import os
from config import *

# Define the screen dimensions and frame size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_SIZE = (600, 472)

# Paths to your animation frame folders
LOOP_SHOOT = LOOP_SHOOT
AI_SHOOT_ANIMATIONS = {
    'self_suc': SUCCEED_AI_SELF,
    'opp_suc': SUCCEED_AI_OPP,
    'self_fail': FAIL_AI_SELF,
    'opp_fail': FAIL_AI_OPP
}

def load_animation_frames(folder, frame_size):
    frames = []
    try:
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.png'):
                frame = pygame.image.load(os.path.join(folder, filename))
                frame = pygame.transform.scale(frame, frame_size)
                frames.append(frame)
        if not frames:
            print(f"No frames loaded from {folder}")
    except Exception as e:
        print(f"Error loading frames from {folder}: {e}")
    return frames

def play_animation(frames, screen, position, loop=True, delay=100):
    frame_index = 0
    running = True
    timig = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        if frames:
            screen.fill((0, 0, 0))  # Clear the screen with a black color
            screen.blit(frames[frame_index], position)
            pygame.display.flip()
            if frame_index == 40:
                
            print(frame_index)
            frame_index = (frame_index + 1) % len(frames)
            if not loop and frame_index == 0:
                running = False

            pygame.time.delay(delay)
        else:
            print("No frames to display.")
            running = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test Animation")

    # Load the animation frames
    loop_frames = load_animation_frames(LOOP_SHOOT, FRAME_SIZE)
    self_suc_frames = load_animation_frames(AI_SHOOT_ANIMATIONS['self_suc'], FRAME_SIZE)
    opp_suc_frames = load_animation_frames(AI_SHOOT_ANIMATIONS['opp_suc'], FRAME_SIZE)
    self_fail_frames = load_animation_frames(AI_SHOOT_ANIMATIONS['self_fail'], FRAME_SIZE)
    opp_fail_frames = load_animation_frames(AI_SHOOT_ANIMATIONS['opp_fail'], FRAME_SIZE)

    center_position = ((SCREEN_WIDTH - FRAME_SIZE[0]) // 2, (SCREEN_HEIGHT - FRAME_SIZE[1]) // 2)

    # Test loop animation
    play_animation(loop_frames, screen, center_position, loop=True)

    # Test ending animations
    play_animation(self_suc_frames, screen, center_position, loop=False)
    play_animation(opp_suc_frames, screen, center_position, loop=False)
    play_animation(self_fail_frames, screen, center_position, loop=False)
    play_animation(opp_fail_frames, screen, center_position, loop=False)

    pygame.quit()
    
main()