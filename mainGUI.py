import pygame
import sys
from config import *
from button import Button
import time
from GameGUI import GameGUI

class MainMenu:
    def __init__(self,name):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Main Menu")
        pygame.mixer.music.load(MAINMENU_BGM)
        
        self.background_image = pygame.image.load(MAIN_MENU_BACKGROUND_IMAGE)
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                
        self.buttons = []
        self.initial_buttons()
        
        self.name = name

    def initial_buttons(self):
        self.buttons.clear()
        
        singleplayer_position = SINGLEPLAYER_BUTTON_POS
        multiplayer_position = MULTIPLAYER_BUTTON_POS
        instructions_position = INSTRUCTIONS_BUTTON_POS
        credits_position = CREDITS_BUTTON_POS
        
        singleplayer_size = SINGLEPLAYER_BUTTON_SIZE
        multiplayer_size = MULTIPLAYER_BUTTON_SIZE
        instructions_size = INSTRUCTIONS_BUTTON_SIZE
        credits_size = CREDITS_BUTTON_SIZE
        
        self.buttons.append(Button(None, singleplayer_size, singleplayer_position, function=self.start_game))
        self.buttons.append(Button(None, multiplayer_size, multiplayer_position, function=self.multiplayer_game))
        self.buttons.append(Button(None, instructions_size, instructions_position, function=self.show_instructions))
        self.buttons.append(Button(None, credits_size, credits_position, function=self.show_credits))
        
    def start_game(self):

        pygame.mixer.music.stop()
        GameGUI(self, self.name).run()

    def multiplayer_game(self):
        print("Multiplayer selected")  # Placeholder function
        # Implement multiplayer game logic here

    def show_instructions(self):
        print("Instructions selected")  # Placeholder function
        # Implement instructions display logic here

    def show_credits(self):
        print("Credits selected")  # Placeholder function
        # Implement credits display logic here

    def quit_game(self):
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()
        
    
    def print_coordinates(self, pos):
        print(f"Mouse clicked at: {pos}")

    def run(self):
        pygame.mixer.music.load(MAINMENU_BGM)
        pygame.mixer.music.play(-1)  # Play the music on loop
        running = True
        while running:
            cursor_changed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.print_coordinates(event.pos)
                    for button in self.buttons:
                        if button.is_clicked(event.pos):
                            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                            button.click()
                            break
            
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(mouse_pos):
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                    cursor_changed = True
                    break
                
            if not cursor_changed:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

            # Draw the background image
            self.screen.blit(self.background_image, (0, 0))

            # Draw the buttons
            for button in self.buttons:
                button.draw(self.screen)

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()
