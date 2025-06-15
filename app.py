from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from generate import create_gif_from_grid
from openai import OpenAI
import base64
import shortuuid
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__, static_folder="generations", static_url_path="/generations")

limiter = Limiter(
    key_func=get_remote_address, app=app, default_limits=["200 per day", "50 per hour"]
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_gif", methods=["POST"])
@limiter.limit("3 per day")
def generate_gif():
    data = request.get_json()
    user_input = data.get("userInput")
    style = data.get("style")

    prompts = {
        "ghibli": f"A square image containing a 3 row by 4 column grid containing 12 panels of a scene as though each panel was a frame in a gif. The scene is of a cozy, anime-style illustration of {user_input}. Be sure to depict each panel in sequential order. The art style is soft and hand-drawn, with subtle shading and gentle pastel colors, reminiscent of Studio Ghibli or slice-of-life anime.",
        "claymation": f"A square image containing a 3 row by 4 column grid containing 12 panels of a scene as though each panel was a frame in a gif. The scene is of a cozy, claymation-style illustration of {user_input}. Be sure to depict each panel in sequential order. The art style is textured and three-dimensional, with visible fingerprints and imperfections, reminiscent of classic stop-motion animation.",
    }
    prompt = prompts.get(style)

    # Initialize client (ensure OPENAI_API_KEY is set in env)
    client = OpenAI()

    response = client.images.generate(
        model="gpt-image-1",  # GPT-4o’s image model
        prompt=prompt,
        size="1024x1536",
        quality="medium",
        n=1,
    )

    # Extract and save the image
    b64 = response.data[0].b64_json
    image_uuid = shortuuid.uuid()

    with open(f"generations/{image_uuid}.png", "wb") as f:
        f.write(base64.b64decode(b64))

    print(f"Saved medium-quality image to generations/{image_uuid}.png")

    # Generate GIF from the saved image
    try:
        create_gif_from_grid(f"{image_uuid}.png")
        gif_file_name = f"{image_uuid}.gif"
        return jsonify({"success": True, "file_name": gif_file_name})
    except Exception as e:
        return jsonify({"success": False, "error": f"Error generating GIF: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=3000)
