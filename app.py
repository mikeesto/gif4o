from flask import Flask, render_template, jsonify, request
from generate import create_gif_from_grid

app = Flask(__name__, static_folder="generations", static_url_path="/generations")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_gif", methods=["POST"])
def generate_gif():
    data = request.get_json()
    prompt = data.get("prompt")
    style = data.get("style")

    # TODO: Make request to openAI to generate image
    # TODO: Save the generated image as in the "generations" folder

    image_file_name = "blonde_2.png"
    try:
        create_gif_from_grid(image_file_name)
        gif_file_name = image_file_name.replace(".png", ".gif")
        return jsonify({"success": True, "file_name": gif_file_name})
    except Exception as e:
        return jsonify({"success": False, "error": f"Error generating GIF: {e}"})


if __name__ == "__main__":
    app.run(debug=True, port=3000)
