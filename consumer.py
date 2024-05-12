from kafka import KafkaConsumer
import json
from flask import Flask, render_template
import threading

app = Flask(__name__)

# Initialize Kafka consumer
consumer = KafkaConsumer('music_recommendations', bootstrap_servers=['localhost:9092'], group_id='music_recommendation_group')
recommendations_data = []

# Function to process recommendations
def process_recommendations():
    global recommendations_data
    for message in consumer:
        try:
            # Decode and process message
            recommendations = json.loads(message.value.decode('utf-8'))
            recommendations_data = recommendations["track_ids"]
        except Exception as e:
            print("Error processing message:", str(e))

# Start Kafka consumer thread
consumer_thread = threading.Thread(target=process_recommendations)
consumer_thread.daemon = True
consumer_thread.start()

# Route for home page
@app.route('/')
def index():
    return render_template('index.html', recommendations=recommendations_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

