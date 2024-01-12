import pygame

class TextDisplay:
    def __init__(self, messages):
        self.messages = messages
        self.current_message_index = 0
        self.current_message = ''

    def update(self):
        # Display the entire message without scrolling
        self.current_message = self.messages[self.current_message_index]

    def draw(self, rect):
        pygame.draw.rect(screen, 'black', rect)
        pygame.draw.rect(screen, 'dark gray', rect, 5)
        text_lines = self.current_message.split('\n')

        for i, line in enumerate(text_lines):
            text_surface = dialogue_font.render(line, True, 'white')
            # Adjusted to start at the top-left corner of the black rect
            text_rect = text_surface.get_rect(topleft=(rect.left + 10, rect.top + 10 + i * dialogue_font.get_linesize()))

            screen.blit(text_surface, text_rect.topleft)

        # Adding a clickable "Click" button with centered text
        button_rect = pygame.Rect(rect.left + 10, rect.bottom - 30, 60, 20)
        pygame.draw.rect(screen, 'white', button_rect)
        button_text = dialogue_font.render('Click', True, 'black')
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect.topleft)

        return button_rect  # Return the button rectangle for click detection

    def next_message(self):
        self.current_message_index = (self.current_message_index + 1) % len(self.messages)
        self.update()

    def handle_event(self, event, rect):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos):  # Check if the mouse click is within the rectangle
                self.next_message()

# Example usage:
pygame.init()
screen = pygame.display.set_mode((800, 600))
dialogue_font = pygame.font.Font(None, 24)

messages = ["Message 1", "Message 2", "Message 3"]
text_display = TextDisplay(messages)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        text_display.handle_event(event, text_display.draw(pygame.Rect(200, 50, 300, 200)))

    pygame.display.flip()

pygame.quit()

