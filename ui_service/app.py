from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

FEEDBACK_SERVICE_URL = 'http://localhost:5001'

@app.route('/')
def index():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    
    feedback_data = {
        'name': name,
        'email': email,
        'message': message
    }
    response = requests.post(f"{FEEDBACK_SERVICE_URL}/submit_feedback", json=feedback_data)

    if response.status_code == 201:
        return redirect(url_for('view_feedback'))
    else:
        return "Error submitting feedback", 500

# Route to display all feedback
@app.route('/feedbacks')
def view_feedback():
    response = requests.get(f"{FEEDBACK_SERVICE_URL}/feedbacks")
    feedbacks = response.json() if response.status_code == 200 else []
    return render_template('show_feedbacks.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
