from flask import Flask, jsonify, render_template
from datetime import datetime
from collections import deque

app = Flask(__name__)

# Store the request counts and timestamps
request_counts = deque([0]*60, maxlen=60)  # Store counts for the last 60 seconds
last_update = datetime.now()

@app.route('/')
def index():
    # Return our graph
    return render_template('index.html')

@app.route('/data')
def data():
    # Return our request count
    return jsonify(list(request_counts))

@app.before_request
def before_request():
    global last_update
    now = datetime.now()
    current_second = int(now.timestamp())
    last_second = int(last_update.timestamp())

    # # If its been longer than a second reset
    while last_second < current_second:
        last_second += 1 
        request_counts.append(0)  # Add a zero count for each second

    # Update the current second's count
    request_counts[-1] += 1
    last_update = now

if __name__ == '__main__':
    app.run(debug=True)
