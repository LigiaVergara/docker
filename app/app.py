import time
import redis
from flask import Flask, render_template
import os
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv() 
cache = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379,  password=os.getenv('REDIS_PASSWORD'))
app = Flask(__name__)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name= "BIPM", count = count)

@app.route('/Titanic')
def titanic():
    df = pd.read_csv("titanic.csv")
    # Calculate number of male and female survivors
    survived_by_sex = df[df['survived'] == 1]['sex'].value_counts()
    # Convert NumPy integer values to Python integers
    bar_labels = ['Male', 'Female']
    bar_data = [int(survived_by_sex.get('male', 0)), int(survived_by_sex.get('female', 0))]

    # Render HTML table
    html_table = df.head().to_html()

    # Render bar chart data
    bar_labels_json = json.dumps(bar_labels)
    bar_data_json = json.dumps(bar_data)

    return render_template('titanic.html', table=html_table, bar_labels=bar_labels, bar_data=bar_data)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
