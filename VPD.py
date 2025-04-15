from flask import Flask, request, render_template
import os
import json
import openai
from datetime import datetime

# Configure OpenAI API Key (ensure to set this as an environment variable for security)
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

app = Flask(__name__, template_folder="frontend")

def generate_responses(prompt_type, input_brief, run_id, num_generations=3):
    """Generates multiple responses using OpenAI GPT-4-turbo and saves them in a structured directory."""
    base_dir = f"runs/{run_id}/{prompt_type}"
    os.makedirs(base_dir, exist_ok=True)

    metadata = {
        "run_id": run_id,
        "prompt_type": prompt_type,
        "input_brief": input_brief,
        "timestamp": datetime.now().isoformat(),
        "num_generations": num_generations
    }

    with open(os.path.join(base_dir, "metadata.json"), "w") as meta_file:
        json.dump(metadata, meta_file, indent=4)

    responses = []
    for i in range(num_generations):
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Use gpt-4-turbo model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI designed to generate a value proposition design proposal structure template "
                        "where you will define a reusable proposal structure template with sections: "
                        "Executive Summary/Overview, Client/Proposed Context & Market Opportunity, "
                        "Proposed Value Proposition Design Approach, Key Deliverables, Timeline, Price & Engagement Model."
                    )
                },
                {"role": "user", "content": input_brief}
            ],
            max_tokens=1500,  # Adjust token limit as needed
            temperature=0.7
        )
        response_text = response["choices"][0]["message"]["content"].strip()  # Extract the response text
        responses.append(response_text)

        response_filename = os.path.join(base_dir, f"response_{i+1}.txt")
        with open(response_filename, "w") as resp_file:
            resp_file.write(response_text)

    return responses

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    prompt_type = request.form["prompt_type"]
    input_brief = request.form["input_brief"]
    run_id = request.form["run_id"]
    num_generations = int(request.form["num_generations"])

    responses = generate_responses(prompt_type, input_brief, run_id, num_generations)
    return f"<h1>Responses Generated</h1><p>{len(responses)} responses saved successfully.</p>"

if __name__ == "__main__":
    app.run(debug=True)
