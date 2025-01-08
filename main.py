from flask import Flask, request, jsonify
import os
import openai

api_key = "replace with user's openai api-key"
openai.api_key = api_key
app = Flask(__name__)
CORS(app)

############### FUNCTION TO PREDICT SPECIALIST ###################
def userinfo():
    data = request.get_json()
    name = data['name']
    symptoms = data['symptoms']
    listToStr = ', '.join([str(elem) for elem in symptoms])

    def get_response(prompt):
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.3
        )
        return response.choices[0].text.strip()

    user_input = ("I have " + listToStr + "symptoms can you suggest me the name of a doctor specialist I should consult? give one word answer only")
    prompt = "User: " + user_input + "\nAI:"
    response = get_response(prompt)
    return jsonify({"Name": name, "Symptoms": listToStr, "Specialist": response})

# Route for Specialist Prediction
@app.route('/userinfo', methods=['POST'])
def auth():
    val = request.headers.get("Authorization")
    if val == auth_key:
        return userinfo()
    else:
        return ("Authorization Error !")
