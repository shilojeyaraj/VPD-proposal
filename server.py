from flask import Flask, request, render_template, jsonify

import difflib
import sys
from html import escape

import openai
import os
from dotenv import load_dotenv



# Load environment variables from a .env file
load_dotenv()

KEY = os.getenv("OPENAI_VPD_API_KEY")
openai.api_key = KEY

#initialize client
client = openai.OpenAI(api_key=KEY)
app = Flask(__name__)

# Initialize conversation history
conversation = [
    {"role": "system", "content": "You are a tech consultant generating proposals tailored to clients' needs."}
]

# Helper function to add a message
def add_message(role, content):
    conversation.append({"role": role, "content": content})

# Generate response
def generate_response():
    print("generating response")
    response = client.responses.create(
        model="gpt-4",
        input=conversation
    )
    reply = response.output_text
    add_message("assistant", reply)
    return reply


def generate_html_diff(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        text1 = f1.readlines()
        text2 = f2.readlines()
    
    # Create the diff
    d = difflib.HtmlDiff()
    html_diff = d.make_file(text1, text2, file1, file2)
    
    # Write the result to output file
    with open(output_file, 'w') as f:
        f.write(html_diff)

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# POST route to handle input from the button's text box
@app.route('/reply', methods=['POST'])
def reply():
    user_input = request.json.get('input')
    add_message("user", user_input)  # Specify the role as "user"

    response = "nothing"
    generate_html_diff("proposal_one.txt", "proposal_two.txt", "proposal_viewer.html")

    return jsonify({'response': response})
if __name__ == '__main__':
    app.run(debug=True)  # Replace 5001 with your desired port number