import pygame
import os
import json

pygame.init()

# Important initializations
WIDTH, HEIGHT = 500, 500
fps = 60
timer = pygame.time.Clock()
main_menu = False

# Define screen characteristics
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Se7en Floors")
menu_background = pygame.transform.scale(pygame.image.load('./ICS4U-Project/Source/sprite_background/6.png'), (WIDTH, HEIGHT))

# Define fonts
font = pygame.font.Font("./ICS4U-Project/Fonts/Bombing.ttf", 30)
title_font = pygame.font.Font("./ICS4U-Project/Fonts/Bombing.ttf", 50)
text_font = pygame.font.Font("./ICS4U-Project/Fonts/Bombing.ttf", 26)
dialogue_font = pygame.font.Font('freesansbold.ttf', 14)

class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))

    def draw(self):
        pygame.draw.rect(screen, 'black', self.button, 0, 5)
        pygame.draw.rect(screen, 'dark gray', self.button, 5, 5)
        text = font.render(self.text, True, 'white')
        screen.blit(text, (self.pos[0] + 100, self.pos[1] + 7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return self.text
        else:
            return None
        
class FloorsButton(Button):
    def __init__(self, txt, pos):
        super().__init__(txt, pos)

class SpriteAnimation:
    def __init__(self, spritesheet_path, frame_dimensions, num_frames, frame_duration):
        self.spritesheet = pygame.image.load(spritesheet_path)
        self.frame_width, self.frame_height = frame_dimensions
        self.num_frames = num_frames
        self.frame_duration = frame_duration
        self.frames = self.extract_frames()
        self.current_frame_index = 0
        self.animation_timer = pygame.time.get_ticks()
        self.x = 20  # Initial x-coordinate of the sprite

    def extract_frames(self):
        frames = []
        spritesheet_width, spritesheet_height = self.spritesheet.get_size()

        for i in range(self.num_frames):
            rect = pygame.Rect(
                i * self.frame_width, 0,
                min(self.frame_width, spritesheet_width - i * self.frame_width),
                min(self.frame_height, spritesheet_height)
            )
            frame = self.spritesheet.subsurface(rect)
            frames.append(frame)

        return frames

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.frame_duration:
            self.current_frame_index = (self.current_frame_index + 1) % self.num_frames
            self.animation_timer = current_time

            # Update the x-coordinate to make the sprite move from left to right
            self.x += 6  # You can adjust the speed as needed

    def get_current_frame(self):
        return self.frames[self.current_frame_index]
    
class TextDisplay:
    def __init__(self, messages):
        self.messages = messages
        self.current_message_index = 0
        self.current_message = ''
        self.show_continue_text = True  # Add a flag to control when to show the "Click to Continue" text
        

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

        if self.show_continue_text:
            # Adding a clickable "Click" button with centered text
            button_rect = pygame.Rect(rect.right - 75, rect.bottom - 30, 60, 20)
            pygame.draw.rect(screen, 'white', button_rect)
            button_text = dialogue_font.render('Click', True, 'black')
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect.topleft)

            return button_rect  # Return the button rectangle for click detection

    def next_message(self):
        self.current_message_index = (self.current_message_index + 1) % len(self.messages)
        self.update()
        self.show_continue_text = True  # Reset the flag when showing the next message

    def handle_event(self, event, rect):
        if event and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos):  # Check if the mouse click is within the rectangle
                self.next_message()


class ScrollingBackground:
    def __init__(self, image_path, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.speed = 2
        self.x = 0

    def update(self):
        self.x -= self.speed
        if self.x < -self.rect.width:
            self.x = 0

    def draw(self):
        x_pos = self.x
        while x_pos < WIDTH:
            screen.blit(self.image, (x_pos, 0))
            x_pos += self.rect.width

class TextBubble:
    def __init__(self, text):
        self.text = text
        self.x = 20
        self.y = HEIGHT - 180
        self.width = WIDTH - 40
        self.height = HEIGHT - self.y - 20
        self.text_color = (255, 255, 255)
        self.font = text_font
        self.rendered_text = self.render_text()
        self.show_continue_text = True

    def render_text(self):
        lines = self.text.splitlines()
        rendered_lines = [self.font.render(line, True, self.text_color) for line in lines]
        return rendered_lines

    def draw(self):
        y_offset = 20
        for line in self.rendered_text:
            screen.blit(line, (self.x + 20, self.y + y_offset))
            y_offset += line.get_height() + 5

        if self.show_continue_text:
            continue_text = font.render('Click to Continue', True, 'white')
            screen.blit(continue_text, (WIDTH - 180, HEIGHT - 60))

class ImageScreen:
    def __init__(self, image_path, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self):
        screen.blit(self.image, (0, 0))

class NextButton(Button):
    def __init__(self, txt, pos):
        super().__init__(txt, pos)


# Save and Load Functions
def save_game(state):
    with open('save_file.json', 'w') as file:
        json.dump(state, file)

def load_game():
    try:
        with open('save_file.json', 'r') as file:
            state = json.load(file)
            return state
    except FileNotFoundError:
        # Handle the case where the file doesn't exist (no saved game)
        return None

class SaveButton(Button):
    def __init__(self, txt, pos):
        super().__init__(txt, pos)

def draw_game():
    title = title_font.render('Se7en Floors', True, 'white')
    screen.blit(title, (145, 10))
    button = Button('Start', (120, 250))
    button.draw()
    return button.check_clicked()

def draw_menu():
    pygame.draw.rect(screen, 'black', [100, 100, 300, 300])

    menu_btn = Button('Exit', (120, 350))
    new_game_btn = Button('New Game', (120, 150))
    load_game_btn = Button('Load Game', (120, 200))
    settings_btn = Button('Settings', (120, 250))
    credits_btn = Button('Credits', (120, 300))

    menu_btn.draw()
    new_game_btn.draw()
    load_game_btn.draw()
    settings_btn.draw()
    credits_btn.draw()

    clicked_button = None
    for button in [load_game_btn, settings_btn, credits_btn, menu_btn, new_game_btn]:
        clicked_button = button.check_clicked()
        if clicked_button:
            break

    if clicked_button == 'Load Game':
        loaded_state = load_game()
        if loaded_state is not None:
            print("Loaded Game!")
            # Implement loading game state logic here
            if 'screen' in loaded_state:
                if loaded_state['screen'] == 'new_game':
                    draw_new_game(loaded_state)  # Pass loaded state to the new game function
                    return True  # Return True to continue the game

        else:
            print("No saved game found!")
    elif clicked_button == 'Settings':
        print("Settings button clicked! Perform Settings action.")
        # Add your code for the "Settings" action here
    elif clicked_button == 'Credits':
        print("Credits button clicked! Perform Credits action.")
        # Add your code for the "Credits" action here
    elif clicked_button == 'New Game':
        print("New Game button clicked! Perform New Game action.")
        draw_new_game()
    elif clicked_button == 'Exit':
        return False

    return True


def draw_new_game(saved_state=None, event=None):
    scrolling_background = ScrollingBackground('./ICS4U-Project/Source/sprite_background/8.png', WIDTH, HEIGHT)
    text_bubble = TextBubble("The year is 2007. You are Detective Wayne, and you \nhave been called up to investigate multiple \nmurders in a condo in the city.")

    # Load sprite sheet for the car animation
    car_animation = SpriteAnimation('./ICS4U-Project/Source/Characters/Ride.png', (256, 256), 8, 100)

    # Load druggie sprite
    druggie = SpriteAnimation('./ICS4U-Project/Source/Characters/Druggie.png', (36, 48), 6, 100)
    druggie.x = 100

    # Load receptionist sprite
    receptionist = SpriteAnimation('./ICS4U-Project/Source/Characters/Receptionist.png', (24, 48), 4, 100)
    receptionist.x = 300  

    # Load Lucy sprite
    lucy = SpriteAnimation('./ICS4U-Project/Source/Characters/Lucy.png', (24, 48), 4, 100)
    lucy.x = 25

    # load Chad sprite
    chad = SpriteAnimation('./ICS4U-Project/Source/Characters/Chad.png', (24,48), 4, 100)
    chad.x = 25

    # Adjust speed and size for the soldier character
    mc_speed = 3  # Adjust the speed as needed
    mc_animation_walk = SpriteAnimation('./ICS4U-Project/Source/Characters/Soldier2_walk.png', (128, 128), 8, 100)
    mc_animation_idle = SpriteAnimation('./ICS4U-Project/Source/Characters/Soldier2_idle.png', (144, 128), 9, 100)
    mc_animation_walk_left_screen = False
    mc_x = 350
    last_movement_direction = "left"

    lobby_background = ImageScreen('./ICS4U-Project/Source/sprite_background/lobby.png', WIDTH, HEIGHT)
    city_background = ImageScreen('./ICS4U-Project/Source/sprite_background/City2_pale.png', WIDTH, HEIGHT)
    outside_lobby_background = ImageScreen('./ICS4U-Project/Source/sprite_background/Outside_lobby.png', WIDTH, HEIGHT)
    floor_2_background = ImageScreen('./ICS4U-Project/Source/sprite_background/Room.png', WIDTH, HEIGHT)
    floor_3_background = ImageScreen('./ICS4U-Project/Source/sprite_background/Room.png', WIDTH, HEIGHT)
    save_button = SaveButton('Save', (WIDTH - 260, 20))  # Move Save button to the top right corner
    floor1_button = FloorsButton('Next Floor', (WIDTH - 260, 70))
    floor2_button = FloorsButton('Next Floor', (WIDTH - 260, 70))
    floor3_button = FloorsButton('Next Floor', (WIDTH - 260, 70))
    floor4_button = FloorsButton('Next Floor', (WIDTH - 260, 70))

    # Initialize game state
    if saved_state is None:
        game_state = {
            'screen': 'new_game',  # Replace with the current screen or game state identifier
            'scrolling_phase': True,  # Initial scrolling phase
            'car_left_screen': False,  # Initial car left screen state
            'mc_animation_walk_left_screen': False, # Initial mc_animation_walk left screen state
            'floor_2': False, 
            'floor_3': False,
            'floor_4': False,
            'floor_5': False,
            'floor_6': False,
            'floor_7': False

            # Add any other relevant information to save
        }
    else:
        game_state = saved_state

    scrolling_phase = game_state['scrolling_phase']
    car_left_screen = game_state['car_left_screen']
    mc_animation_walk_left_screen = game_state['mc_animation_walk_left_screen']
    floor_2 = game_state['floor_2']
    floor_3 = game_state['floor_3']
    floor_4 = game_state['floor_4']
    # floor_5 = game_state['floor_5']
    # floor_6 = game_state['floor_6']
    # floor_7 = game_state['floor_7']

    # Set initial positions for car and mc_animation_walk based on saved state
    car_animation.x = game_state.get('car_x', 20)
    mc_animation_walk.x = game_state.get('mc_x', 20)

    text_display = TextDisplay(['Druggie: Hey Stranger, if you know whats best for you, youll \nturn back around',
                                 'Todd: And if I dont want to?', 
                                 'Druggie: Youre gonna wish you did', 
                                 'Todd: Is that a threat?',
                                 'Druggie: Im not threatening you. Im warning you. I told the \nblonde fella the same thing. I havent seen him in... its been a \nwhile. Call me crazy but he did look like you ',
                                 'Todd: Did he have that smug look on his face?',
                                 'Druggie: Yeah actually, yeah he did! He had that same brutish \nlook youre giving me right now. Is yall related or somthin?',
                                 'Todd: Im done talking.',
                                 'Druggie: Keep walking, dont let the door hit you on the way in.'])
    text_display.update()
    button_rect = None
    recep_display = TextDisplay(['Todd: Hey you!', 
                                 'Receptionist: Me?',
                                 'Todd: You see anyone else in the room?',
                                 'Receptionist: Sorry. How may I help you sir?',
                                 'Todd: Im gonna ask you once and once only. I traced a call \nfrom someone who sounded a lot like my brother. It led me here. \nWhere is Jason Morgan?',
                                 'Receptionist: I dont know who that is sir.',
                                 'Todd: 6 foot blonde brute? Youre telling me you havent seen \n him once?',
                                 'Receptionist: I dont know what to tell you.',
                                 'Todd: "We are in a prison".',
                                 'Receptionist: What?',
                                 'Todd: Thats what he said to me on the call. So it sounds like \nyoure lying',
                                 'Receptionist: I dont know what youre talking about.',
                                 'Todd: Listen carefully, if you dont point me in the direction \nof where theyre keeping him ill bash your head into your \ncomputer more times than you can think.',
                                 'Receptionist: gulps* head upstairs.'])
    recep_display.update()
    button_rect_recep = None
    lucy_display = TextDisplay(['Lucy: Woah, who are you? You aint from round here thats for \nsure. You and that big gun of yours. At least youll be able to \nhandle yourself round the big boy.', 
                                'Todd: What big boy?',
                                'Lucy: Wanna see what I can do for a dolla?',
                                'Todd: No.',
                                'Lucy: Fine by me. That blonde print of a man left me wanting \nmore.',
                                'Todd: Did that man ever mention his name?',
                                'Lucy: Nah, we were neva on a first name basis with eachother..\nHold on wait, nevermind. That might have been someone else. I \nthink his name was Jackie-no Jason.',
                                'Todd: Where is he?',
                                'Lucy: Whats it to you big boy?',
                                'Todd: Tell me and ill make it worth your while.',
                                'Lucy: Ohh now youse flirting?',
                                'Todd: If you say so.',
                                'Lucy: After we were done, you know... He had to go and \nsounded very brief then went upstairs. That was 3 weeks ago \nor somethin',
                                'Todd: And you never seen him since?',
                                'Lucy: I wish. Anyways are we gonna...',
                                'Todd: No.',
                                'Lucy: Alright mista.. I see how it is. Cant even have a little \nfun round these parts. You and that gun of yours. At least youll \nhandle yourself with that big dog.'])
    lucy_display.update()
    button_rect_lucy = None
    chad_display = TextDisplay(['H', 'o'])
    chad_display.update()
    button_rect_chad = None

    while True:
        screen.fill((0, 0, 0))

        if scrolling_phase:
            scrolling_background.update()
            scrolling_background.draw()
            text_bubble.draw()

            # Check if the car has left the screen
            if car_animation.x > WIDTH:
                car_left_screen = True
        else:
            if not car_left_screen:
                city_background.draw()
            else:
                outside_lobby_background.draw()
                distance_to_druggie = abs(mc_x - druggie.x)

                keys = pygame.key.get_pressed()
                movement_dict = {pygame.K_LEFT: -mc_speed, pygame.K_RIGHT: mc_speed}

                for key, speed in movement_dict.items():
                    if keys[key]:
                        mc_x += speed
                        last_movement_direction = "left" if speed < 0 else "right"

                mc_animation_walk.update()

                if not any(keys):
                    #mc_animation_idle.update()
                    current_frame_soldier = pygame.transform.scale(mc_animation_idle.get_current_frame(), (220, 220))

                    # Mirror the idle sprite based on the last movement direction
                    if last_movement_direction == "left":
                        current_frame_soldier = pygame.transform.flip(current_frame_soldier, True, False)
                else:
                    current_frame_soldier = pygame.transform.scale(mc_animation_walk.get_current_frame(), (220, 220))

                    # Mirror the sprite based on the last movement direction
                    if last_movement_direction == "left":
                        current_frame_soldier = pygame.transform.flip(current_frame_soldier, True, False)

                screen.blit(current_frame_soldier, (mc_x, HEIGHT - current_frame_soldier.get_height() - 55))

                current_frame_druggie = pygame.transform.scale(druggie.get_current_frame(), (70, 130))
                screen.blit(current_frame_druggie, (druggie.x, HEIGHT - current_frame_druggie.get_height() - 55))

                if distance_to_druggie < 25:
                    rect_for_text_display = pygame.Rect(20, HEIGHT - 100, WIDTH - 40, 80)
                    button_rect = text_display.draw(rect_for_text_display)

                    if button_rect:
                        text_display.handle_event(event, rect_for_text_display)

                

                if mc_x < current_frame_soldier.get_width() - 380:
                    mc_animation_walk_left_screen = True

                if mc_animation_walk_left_screen:
                    lobby_background.draw()
                    floor1_button.draw()

                    current_frame_receptionist = pygame.transform.flip(receptionist.get_current_frame(), True, False)
                    current_frame_receptionist = pygame.transform.scale(current_frame_receptionist, (70, 150))
                    screen.blit(current_frame_receptionist, (receptionist.x, HEIGHT - current_frame_receptionist.get_height() - 85))

                    screen.blit(current_frame_soldier, (100 + mc_x, HEIGHT - current_frame_soldier.get_height() - 85))

                    if mc_x > receptionist.x - 250 and mc_x < receptionist.x + 250:
                        rect_for_recep_display = pygame.Rect(20, HEIGHT - 100, WIDTH - 40, 80)
                        button_rect_recep = recep_display.draw(rect_for_recep_display)

                        if button_rect_recep:
                            recep_display.handle_event(event, rect_for_recep_display)

                    if floor1_button.check_clicked():
                        floor_2 = True
                    if floor_2:
                        floor_2_background.draw()
                        floor2_button.draw()

                        current_frame_lucy = pygame.transform.scale(lucy.get_current_frame(), (70, 130))
                        screen.blit(current_frame_lucy, (lucy.x, HEIGHT - current_frame_lucy.get_height() - 67))
                        
                        screen.blit(current_frame_soldier, (100 + mc_x, HEIGHT - current_frame_soldier.get_height() - 65))

                        distance_to_lucy = abs(mc_x - (lucy.x - 100))

                        if distance_to_lucy < 25:
                            rect_for_lucy_display = pygame.Rect(20, HEIGHT - 100, WIDTH - 40, 80)
                            button_rect_lucy = lucy_display.draw(rect_for_lucy_display)

                            if button_rect_lucy:
                                lucy_display.handle_event(event, rect_for_lucy_display)
                        
                        if  mc_x > current_frame_soldier.get_width() + 100:
                            floor_3 = True
                        if floor_3:
                            floor_3_background.draw()
                            floor3_button.draw()

                            current_frame_chad = pygame.transform.scale(chad.get_current_frame(), (80, 140))
                            screen.blit(current_frame_chad, (chad.x, HEIGHT - current_frame_chad.get_height() - 67))

                            screen.blit(current_frame_soldier, (mc_x, HEIGHT - current_frame_soldier.get_height() - 65))

                            distance_to_chad = abs(mc_x - (chad.x - 100))    

                            if distance_to_chad < 80:
                                rect_for_chad_display = pygame.Rect(20, HEIGHT - 100, WIDTH - 40, 80) 
                                button_rect_chad = chad_display.draw(rect_for_chad_display)   

                                if button_rect_chad:
                                    chad_display.handle_event(event, rect_for_chad_display)

                            if floor3_button.check_clicked():
                                floor_4 = True
                            if floor_4:
                                floor_2_background.draw()
                                floor4_button.draw()                  

            car_animation.update()
            current_frame = car_animation.get_current_frame()
            screen.blit(current_frame, (car_animation.x, HEIGHT - current_frame.get_height() - 20))

            if car_animation.x > WIDTH:
                car_left_screen = True

        if not text_bubble.show_continue_text:
            scrolling_phase = False

        if scrolling_phase:
            text_bubble.show_continue_text = True
            continue_text = font.render('Click to Continue', True, 'white')
            screen.blit(continue_text, (WIDTH - 180, HEIGHT - 60))

        save_button.draw()

        pygame.display.flip()
        timer.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_bubble.show_continue_text:
                    text_bubble.show_continue_text = False
                elif distance_to_druggie < 25 and button_rect:
                    text_display.handle_event(event, rect_for_text_display)
                elif mc_x > receptionist.x - 250 and mc_x < receptionist.x + 250 and button_rect_recep:
                    recep_display.handle_event(event, rect_for_recep_display)
                else:
                    save_clicked = save_button.check_clicked()
                    if save_clicked:
                        game_state['scrolling_phase'] = scrolling_phase
                        game_state['car_left_screen'] = car_left_screen
                        game_state['mc_animation_walk_left_screen'] = mc_animation_walk_left_screen
                        game_state['floor_2'] = floor_2
                        game_state['floor_3'] = floor_3
                        game_state['floor_4'] = floor_4
                        # game_state['floor_5'] = floor_5
                        # game_state['floor_6'] = floor_6
                        # game_state['floor_7'] = floor_7
                        game_state['car_x'] = car_animation.x
                        game_state['mc_x'] = mc_x

                        save_game(game_state)
                        print("Game Saved!")

                    print("Clicked on the background!")
                

    return True


run = True
while run:
    screen.blit(menu_background, (0, 0))
    timer.tick(fps)
    if main_menu:
        main_menu = draw_menu()
    else:
        main_menu = draw_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()

