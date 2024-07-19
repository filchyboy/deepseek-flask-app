"""Simple Deepseek Flask App for local use"""

import os
import json
from dotenv import load_dotenv
import requests
from flask import Flask, request, render_template, jsonify

load_dotenv()
app = Flask(__name__)


def get_deepseek_coder_response(user_input):
    """
    This function sends a POST request to the DeepSeek API to get a response
    to the user's input. The response is then returned to the caller.
    """
    url = "https://api.deepseek.com/chat/completions"
    payload = json.dumps(
        {
            "messages": [
                {
                    "content": "You are a helpful coding assistant.",
                    "role": "system"
                },
                {"content": user_input, "role": "user"},
            ],
            "model": "deepseek-coder",
            "max_tokens": 2048,
            "temperature": 0.5,
            "top_p": 1,
            "stream": False,
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("DEEPSEEK_API_KEY"),
    }

    response = requests.post(url, headers=headers, data=payload, timeout=60)
    if response.status_code == 200:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return {"content": content}
    else:
        return {"Error": response.status_code, "Message": response.text}


@app.route("/", methods=["GET", "POST"])
def index():
    """
    This function is the main function that handles the GET and
    POST requests to the root URL. It uses AJAX for POST requests
    to dynamically update the output based on user input without 
    reloading the page.
    """
    if request.method == "POST":
        data = request.get_json()  # Ensure JSON data is correctly parsed
        user_input = data["user_input"]
        response = get_deepseek_coder_response(user_input)
        return jsonify(response)  # Return the processed response
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
