from PIL import Image
import os


def create_gif_from_grid(
    img_file_name,
    output_path="./generations",
    grid_width=3,
    grid_height=4,
    crop_percent=0.05,
    upscale_factor=1.01,
    duration=150,
):
    """
    Convert a grid of frames in an image to an animated GIF.

    Args:
        img_file_name (str): File name of the input image
        output_path (str): Path for output GIF
        grid_width (int): Number of columns in the grid
        grid_height (int): Number of rows in the grid
        crop_percent (float): Percentage to crop from each side (0.0-0.5)
        upscale_factor (float): Factor to upscale cropped frames
        duration (int): Duration between frames in milliseconds
    """
    img_path = os.path.join(output_path, img_file_name)

    # Input validation
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image file not found: {img_path}")

    if crop_percent < 0 or crop_percent >= 0.5:
        raise ValueError("crop_percent must be between 0 and 0.5")

    # Generate output GIF path
    base_name = os.path.splitext(img_file_name)[0]
    gif_output_path = os.path.join(output_path, f"{base_name}.gif")

    try:
        img = Image.open(img_path)

        # Calculate frame dimensions
        frame_width = img.width // grid_width
        frame_height = img.height // grid_height

        if frame_width == 0 or frame_height == 0:
            raise ValueError("Grid size is too large for the image dimensions")

        def crop_and_upscale(frame):
            """Crop and upscale a single frame."""
            crop_margin_w = int(frame.width * crop_percent)
            crop_margin_h = int(frame.height * crop_percent)

            cropped = frame.crop(
                (
                    crop_margin_w,
                    crop_margin_h,
                    frame.width - crop_margin_w,
                    frame.height - crop_margin_h,
                )
            )

            new_size = (
                int(cropped.width * upscale_factor),
                int(cropped.height * upscale_factor),
            )
            return cropped.resize(new_size, Image.LANCZOS)

        # Extract and process frames
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

        if not frames:
            raise ValueError("No frames were extracted from the image")

        # Save as GIF
        frames[0].save(
            gif_output_path,
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=duration,
            loop=0,
        )

        print(f"GIF created successfully: {gif_output_path}")
        print(f"Generated {len(frames)} frames from {grid_width}x{grid_height} grid")

    except Exception as e:
        print(f"Error creating GIF: {e}")
        raise


# Usage example for testing
if __name__ == "__main__":
    img_file_name = "blonde_girl_reading.png"
    create_gif_from_grid(img_file_name)
