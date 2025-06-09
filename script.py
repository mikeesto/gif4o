from PIL import Image

img_path = "./blonde_2.png"
img = Image.open(img_path)

# Define the grid size
grid_width = 3  # columns
grid_height = 4  # rows

# Calculate dimensions of each frame
frame_width = img.width // grid_width
frame_height = img.height // grid_height


# Crop 5% from each side and upscale by 1.01
def crop_and_upscale(frame):
    crop_margin_w = int(frame.width * 0.05)
    crop_margin_h = int(frame.height * 0.05)
    cropped = frame.crop(
        (
            crop_margin_w,
            crop_margin_h,
            frame.width - crop_margin_w,
            frame.height - crop_margin_h,
        )
    )
    new_size = (int(cropped.width * 1.01), int(cropped.height * 1.01))
    return cropped.resize(new_size, Image.LANCZOS)


# Slice the grid
frames = []
for row in range(grid_height):
    for col in range(grid_width):
        left = col * frame_width
        upper = row * frame_height
        right = left + frame_width
        lower = upper + frame_height
        frame = img.crop((left, upper, right, lower))
        processed_frame = crop_and_upscale(frame)
        frames.append(processed_frame)

# Save as GIF
gif_path = "./blonde_2.gif"
frames[0].save(
    gif_path,
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=150,
    loop=0,
)
