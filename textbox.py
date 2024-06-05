from config import *


class TextBox:
    def __init__(self, pos, size, font_size=32, text_color=(255, 255, 255), callback=None, indicator_image_path=INDICATOR_PNG, indicator_size=INDICATOR_SIZE):
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.SysFont('mars', font_size)
        self.text_color = text_color
        self.callback = callback
        self.dialogues = []
        self.current_text = ""
        self.dialogue_index = 0
        self.char_index = 0
        self.time_since_last_char = 0
        self.char_delay = 50  # milliseconds per character
        self.indicator_image = pygame.image.load(indicator_image_path) if indicator_image_path else None
        self.indicator_image = pygame.transform.scale(self.indicator_image, indicator_size)
        self.indicator_pos = (self.rect.right - 50, self.rect.bottom - 50)

    def add_dialogues(self, dialogues):
        self.dialogues.extend(dialogues)
        self.dialogue_index = 0
        self.current_text = ""
        self.char_index = 0

    def update(self):
        if self.dialogue_index < len(self.dialogues):
            self.time_since_last_char += pygame.time.get_ticks()
            if self.time_since_last_char >= self.char_delay:
                self.time_since_last_char = 0
                if self.char_index < len(self.dialogues[self.dialogue_index]):
                    self.current_text += self.dialogues[self.dialogue_index][self.char_index]
                    self.char_index += 1

    def draw(self, screen):
        words = self.current_text.split(' ')
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if self.font.size(current_line + ' ' + word)[0] < self.rect.width - 20:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        y_offset = 10
        for line in lines[-3:]:
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
            y_offset += self.font.get_height()

        if self.indicator_image and self.dialogue_index < len(self.dialogues) - 1:
            screen.blit(self.indicator_image, self.indicator_pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        if self.dialogue_index < len(self.dialogues) - 1:
            self.dialogue_index += 1
            self.current_text = ""
            self.char_index = 0
        else:
            self.dialogue_index = 0
            self.current_text = ""
            self.char_index = 0
            if self.callback:
                self.callback()
                
