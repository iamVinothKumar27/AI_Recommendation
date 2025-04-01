from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini model
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/movie')
def movie():
    return render_template('movie.html')

@app.route('/recommend_food', methods=['POST'])
def recommend_food():
    data = request.json
    emotion = data['emotion']
    location = data['location']
    time = data['time']

    prompt = f"""
    You are a travel guide. Your tourist is feeling sleepy and also {emotion} around {location} at {time}.
    They are driving a car and need some food to refresh.
    Suggest two food items for them: one vegan and one non-vegan.
    Format the response as:
    "Hey buddy, why not a <food suggestion> at <restaurant nearby> now?" or
    "A cup of coffee would make you feel better."
    """

    response = model.generate_content(prompt)
    recommendation = response.text.strip()

    return jsonify({"recommendation": recommendation})

@app.route('/recommend_movie', methods=['POST'])
def recommend_movie():
    data = request.json
    mood = data['mood']
    language = data['language']
    genre = data['genre']

    prompt = f"""You're an expert movie recommender, tasked with suggesting films based on emotional states and language preferences.
    Your client is feeling {mood} and speaks {language}. You know that when someone is {mood}, a {genre} movie can be particularly resonant.
    Please recommend a specific {genre} film that would align well with a {mood} mood."""

    response = model.generate_content(prompt)
    recommendation = response.text.strip()

    return jsonify({"recommendation": recommendation})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
