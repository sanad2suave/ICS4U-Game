import pygame

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 14)
screen = pygame.display.set_mode([500, 500])
timer = pygame.time.Clock()

messages = [
    'Hello detective!, I heard that there has been murders here.',
    'This condo has 7 floors including the lobby. You are welcome to explore all of them!',
    'Happy Hunting!'
]

snip = font.render('', True, 'white')
counter = 0
speed = 3
active_message = 0
message = messages[active_message]
done = False

def render_multiline_text(text, width):
    words = text.split()
    lines = []
    current_line = []
    current_line_width = 0

    for word in words:
        word_width, _ = font.size(word)

        if current_line_width + word_width <= width:
            current_line.append(word)
            current_line_width += word_width + font.size(' ')[0]  # Add space width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_line_width = word_width + font.size(' ')[0]

    if current_line:
        lines.append(' '.join(current_line))

    return lines

run = True
while run:
    screen.fill('dark grey')
    timer.tick(60)
    pygame.draw.rect(screen, 'black', [0, 300, 800, 200])

    if counter < speed * len(message):
        counter += 1
    elif counter >= speed * len(message):
        done = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and done and active_message < len(messages) - 1:
                active_message += 1
                done = False
                message = messages[active_message]
                counter = 0

    rendered_lines = render_multiline_text(message[0:counter // speed], 480)
    for i, line in enumerate(rendered_lines):
        snip = font.render(line, True, "White")
        screen.blit(snip, (10, 310 + i * font.get_height()))

    pygame.display.flip()

pygame.quit()
