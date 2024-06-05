import pygame
from config import *

class Button:
    def __init__(self, image_path, size, position, function=None, text=None, font_size=30, text_color=(0, 0, 0)):
        self.image_path = image_path
        self.size = size
        self.position = position
        self.original_position = position
        self.original_size = size
        self.target_size = size
        self.load_image()
        self.rect = pygame.Rect(position, size)  # Use pygame.Rect to define the button's area
        self.function = function
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)  # Initialize the font
        self.animating = False
        self.animation_frames = 0
        
    def load_image(self):
        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, self.size)
            self.original_image = self.image
        else:
            self.image = None
            self.original_image = None
            
    def start_animation(self, target_size, frames=30):
        self.target_size = target_size
        self.animating = True
        self.animation_frames = frames
        
    def update(self):
        if self.animating and self.animation_frames > 0:
            step_size = ((self.target_size[0] - self.size[0]) / self.animation_frames,
                         (self.target_size[1] - self.size[1]) / self.animation_frames)
            self.size = (self.size[0] + step_size[0], self.size[1] + step_size[1])
            self.position = (self.position[0] - step_size[0] / 2, self.position[1] - step_size[1] / 2)
            self.rect = pygame.Rect(self.position, self.size)
            if self.image_path:
                self.image = pygame.transform.scale(self.original_image, (int(self.size[0]), int(self.size[1])))
            self.animation_frames -= 1
            if self.animation_frames <= 0:
                self.animating = False

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def is_clicked(self, position):
        return self.rect.collidepoint(position)

    def click(self):
        if self.function:
            play_mp3(BUTTON_SOUND)
            self.function()

    def blink(self, state):
        self.image = self.original_image if state else None

    def get_position(self):
        return self.rect.topleft
