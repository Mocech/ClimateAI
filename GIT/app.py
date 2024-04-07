import imaplib
import email
import random
import requests
import schedule
import sqlite3
import time

from flask import Flask, render_template, request

app = Flask(__name__,render_template="template")

# SQLite database initialization
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             email TEXT NOT NULL,
             location TEXT NOT NULL,
             password TEXT NOT NULL)''')
conn.commit()

def generate_verification_token():
    return ''.join(random.choices('0123456789abcdef', k=16))

def fetch_weather():
    API_KEY = 'your_openweathermap_api_key'
    CITY = 'your_city_name'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    return f'Weather in {CITY}: {weather_description}, Temperature: {temperature}°C'

def send_weather_update():
    weather_data = fetch_weather()
    for row in c.execute('SELECT email FROM users'):
        email = row[0]
        # Here you can call the function to send email to 'email' with weather data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    location = request.form['location']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    c.execute("SELECT * FROM users WHERE email=?", (email,))
    existing_user = c.fetchone()
    if existing_user:
        return 'Email already exists. Please use a different email.'
    else:
        c.execute("INSERT INTO users (email, location, password) VALUES (?, ?, ?)", (email, location, password))
        conn.commit()
        # Send weather data immediately after registration
        weather_data = fetch_weather()
        # Here you can call the function to send email to 'email' with weather data
        # Schedule daily weather updates
        schedule.every().day.at('09:00').do(send_weather_update)
        return 'Registration successful!'

if __name__ == '__main__':
    app.run(debug=True)
    while True:
        schedule.run_pending()
        time.sleep(1)