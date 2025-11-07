from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    weather_data=None
    error= False
    submitted=False

    if request.method == 'POST':
        submitted = True
        city=request.form['city']
        api_key=os.getenv("OPEN_WEATHER_API_KEY","8a6c9a617f53a03d040199d25ef2d2be")
        url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response=requests.get(url)

        if response.status_code==200:
            weather_data=response.json()
            icon_code =weather_data['weather'][0]['icon']
            icon_url=f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            weather_data={
                'city':city,
                'temp':weather_data['main']['temp'],
                'description':weather_data['weather'][0]['description'],
                'humidity':weather_data['main']['humidity'],
                'icon':icon_url,
            }
        elif request.method == 'GET':
            submitted = False
        else:
            error = True
        return render_template('index2.html',weather=weather_data, error=error, submitted=submitted)

if __name__=='__main__':
    app.run(debug=True)