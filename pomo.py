from flask import Flask, render_template, request, jsonify
import time
import threading

app = Flask(__name__)

# Shared data to store the remaining time
remaining_time = 0
stop_thread = False

def countdown(minutes):
    global remaining_time, stop_thread
    seconds = minutes * 60
    while seconds > 0 and not stop_thread:
        remaining_time = seconds
        time.sleep(1)
        seconds -= 1
    remaining_time = 0

@app.route('/')
def index():
    return render_template('pomo.html')

@app.route('/start_timer', methods=['POST'])
def start_timer():
    global stop_thread
    stop_thread = True  # Stop any existing timer
    data = request.json
    minutes = int(data['minutes'])
    stop_thread = False
    threading.Thread(target=countdown, args=(minutes,)).start()
    return jsonify({"status": "Timer started for {} minutes".format(minutes)})

@app.route('/get_time', methods=['GET'])
def get_time():
    global remaining_time
    mins, secs = divmod(remaining_time, 60)
    return jsonify({"minutes": mins, "seconds": secs})

if __name__ == '__main__':
    app.run(debug=True)
