from PIL import Image

def get_frame_dimensions(spritesheet_path):
    # Open the spritesheet using Pillow
    spritesheet = Image.open(spritesheet_path)

    # Get the dimensions of a single frame (assuming the frames are arranged horizontally)
    frame_width = spritesheet.width // num_frames
    frame_height = spritesheet.height

    return frame_width, frame_height

# Replace 'your_spritesheet.png' with the actual path to your spritesheet
spritesheet_path = './ICS4U-Project/Source/Characters/Soldier2_attack.png'
num_frames = 8  # Update with the actual number of frames in your spritesheet

frame_width, frame_height = get_frame_dimensions(spritesheet_path)

print(f"Frame Width: {frame_width}, Frame Height: {frame_height}")
