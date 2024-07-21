from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for
from gtts import gTTS
from translate import Translator
import time
import json
import os, re
import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
app = Flask(__name__)

# for hindi

API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-hi"
headers = {"Authorization": "Bearer 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"}

#for jap

#API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-tatoeba-en-ja"
#headers = {"Authorization": "Bearer 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"}
 
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']

        # Load user data from the JSON file
        try:
            with open('user_data.json', 'r') as json_file:
                user_data_list = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            user_data_list = []

        # Check if the entered username and password match any user in the list
        for user_data in user_data_list:
            if user_data['username'] == entered_username and user_data['password'] == entered_password:
                # Extract name and post from user_data
                name = user_data['name']
                post = user_data['post']
                url = url_for('profile', name=name, post=post)

                return render_template('1.html', name=name, post=post)

        return jsonify({'error': 'Invalid username or password'})
    
    return render_template('login.html')
    
@app.route('/signup1', methods=['POST'])
def update():
    data = {
        'name': request.form['name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': request.form['password'],
        'post': request.form['post']
    }
    try:
        with open('user_data.json', 'r') as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # Add the new data to the list
    existing_data.append(data)

    # Save the updated data to the JSON file
    with open('user_data.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=2)
    return redirect(url_for('login'))


@app.route('/signup')
def sign_up():
    return render_template('signup.html')

def get_next_serial_number():
    try:
        with open('translation_output.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return len(data) + 1
    except FileNotFoundError:
        return 1
    
def translate(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    translation = response.json()
    return translation[0]['translation_text']

@app.route('/translat', methods=['POST']) 
def translat():
    twt = request.get_json()
    tex = twt.get('text')
    translator = Translator(to_lang="ja")
    translation_test = translator.translate(tex)
    
    # Translate text using the Hugging Face model
    translation = translate(tex)
    
    # Get the next serial number
    serial_number = get_next_serial_number()
    
    # Load existing data from the file or initialize an empty list
    try:
        with open('translation_output.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []

    # Append the new translation with serial number to the list
    output_data = {
        "serial_number": serial_number,
        "original_text": tex,
        "translated_text": translation,
        "translation_check": translation_test
    }
    data.append(output_data)
    
    # Save the updated list to the file
    with open('translation_output.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(translation)
    return jsonify({"serial_number": serial_number, "translated_text": translation}), 200

    
@app.route('/speech', methods=['POST'])
def speech():
    twt = request.get_json()
    serial_number = twt.get('serial_number')
    print(serial_number)

    # Load translation data from the file
    try:
        with open('translation_output.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        return jsonify({"error": "Translation data not found"}), 404

    # Find the entry with the specified serial number
    entry = next((item for item in data if item["serial_number"] == serial_number), None)
    if entry is None:
        return jsonify({"error": f"Translation with serial number {serial_number} not found"}), 404

    # Use the translated text for text-to-speech
    text_to_speech_text = entry["translated_text"] 

    # Generate a unique filename using a timestamp
    timestamp = str(int(time.time()))
    audio_filename = f"static/{timestamp}.mp3"

    # Convert text to speech and save with the unique filename
    tts = gTTS(text_to_speech_text, lang="ja")
    tts.save(audio_filename)
    print("Audio filename:", audio_filename)

    # Create the audio URL with the unique filename
    audio_url = f'/{audio_filename}'

    return jsonify(audio_url=audio_url)

@app.route('/output/<filename>')
def serve_audio(filename):
    path_to_file = f"static/{filename}"
    print(path_to_file)

    return send_file(
        path_to_file,
        mimetype="audio/mp3",
        as_attachment=True,
        attachment_filename=filename
    )

@app.route('/profile')
def profile():
    name = request.args.get('name')
    post = request.args.get('post')


    # Sample JSON data (replace this with your actual JSON data)
    json_data = '''
    {
        "categories": ["Category A", "Category B", "Category C"],
        "percentages": [30, 50, 20]
    }
    '''

    # Load JSON data
    data = json.loads(json_data)
    categories = data['categories']
    percentages = data['percentages']

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.pie(percentages, labels=categories, autopct='%1.1f%%', startangle=140, colors=['lightblue', 'lightgreen', 'lightcoral'])
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f'Pie Chart of Categories by Percentage for {name}')

    # Generate filename based on name variable
    chart_filename = f'static/pie_chart_{name}.png'
    plt.savefig(chart_filename)


    # Generate URL for the saved chart file
    chart_url = url_for('static', filename=f'pie_chart_{name}.png')

    return render_template('profile.html', name=name, post=post, chart_url=chart_url)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
