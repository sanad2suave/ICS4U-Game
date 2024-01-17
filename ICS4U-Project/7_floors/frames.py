import pygame

def count_frames(spritesheet_path, frame_width, frame_height):
    spritesheet = pygame.image.load(spritesheet_path)
    spritesheet_width, spritesheet_height = spritesheet.get_size()

    num_frames_horizontal = spritesheet_width // frame_width
    num_frames_vertical = spritesheet_height // frame_height

    total_frames = num_frames_horizontal * num_frames_vertical

    return total_frames

# Example usage:
spritesheet_path = './ICS4U-Project/Source/Characters/Jason_walk.png'
frame_width = 128
frame_height = 128

num_frames = count_frames(spritesheet_path, frame_width, frame_height)
print(f"Number of frames: {num_frames}")