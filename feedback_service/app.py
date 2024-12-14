from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'feedback.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)



# POST route to handle feedback submission
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    feedback = Feedback(name=name, email=email, message=message)
    db.session.add(feedback)
    db.session.commit()

    return jsonify({"message": "Feedback submitted successfully!"}), 201

@app.route('/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = Feedback.query.all()
    return jsonify([{
        "id": fb.id,
        "name": fb.name,
        "email": fb.email,
        "message": fb.message
    } for fb in feedbacks])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)
