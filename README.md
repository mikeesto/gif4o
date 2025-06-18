# GIF4o

GIF4o is a small web application that generates short animations by prompting GPT-4o for a grid of sequential frames. These frames are then processed into an animated GIF. You can choose between "Whimsical" and "Claymation" art styles.

This project explores a quick and cost-effective method for creating AI-generated animations.

**Blog Post:**
I have written some words about this project here: [Animating GPT-4o image grids](https://mikeesto.com/posts/animating-gpt4o-image-grids/).

**Running Locally:**
To run GIF4o on your own machine, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/mikeesto/gif4o.git
    cd gif4o
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set your OpenAI API Key:**
    You will need an OpenAI API key with access to GPT-4o image generation models.
    Create a `.env` file in the root directory of the project and add your API key like so:

    ```
    OPENAI_API_KEY="your_actual_openai_api_key_here"
    ```

    Using the OpenAI API will incur costs based on your usage. Please be mindful of this.

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will then be accessible in your web browser at `http://localhost:3000`.

---
