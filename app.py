from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import json
import random
import requests
import os

app = Flask(__name__)
CORS(app)

# Mock data for questions
ROLE_QUESTIONS = {
    'sde': {
        'technical': ["Design a URL shortener like bit.ly", "Implement rate limiting", "System design for chat app"],
        'hr': ["Why software engineering?", "Describe your coding journey", "How do you debug complex issues?"],
        'managerial': ["How would you mentor junior developers?", "Prioritize features with tight deadlines", "Handle technical debt"]
    },
    'ml': {
        'technical': ["Build recommendation system", "Handle imbalanced datasets", "Deploy ML model at scale"],
        'hr': ["Why machine learning?", "Explain ML to non-technical person", "Stay updated with ML trends"],
        'managerial': ["Lead ML team", "Choose between model accuracy vs speed", "Manage ML project timeline"]
    },
    'cloud': {
        'technical': ["Design multi-region architecture", "Implement auto-scaling", "Cost optimization strategies"],
        'hr': ["Why cloud computing?", "Explain cloud benefits to client", "Handle cloud migration challenges"],
        'managerial': ["Lead cloud transformation", "Balance security vs accessibility", "Manage cloud budget"]
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🤖 AI Interview Engine</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .header { text-align: center; color: #333; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .button:hover { background: #0056b3; }
        .score { background: #28a745; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .feedback { background: #17a2b8; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; }
        textarea { width: 100%; height: 100px; margin: 10px 0; padding: 10px; border-radius: 5px; border: 1px solid #ddd; }
        select { padding: 10px; margin: 10px; border-radius: 5px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🤖 AI Mock Interview Engine</h1>
        
        <div class="section">
            <h3>🎯 Interview Settings</h3>
            <select id="role">
                <option value="sde">SDE (Software Engineer)</option>
                <option value="ml">ML (Machine Learning)</option>
                <option value="cloud">Cloud Engineer</option>
            </select>
            <select id="round">
                <option value="technical">Technical Round</option>
                <option value="hr">HR Round</option>
                <option value="managerial">Managerial Round</option>
            </select>
            <select id="difficulty">
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
            </select>
        </div>

        <div class="section">
            <button class="button" onclick="getQuestion()">🎯 Get New Question</button>
            <button class="button" onclick="showAIAnswer()">🤖 Show AI Answer</button>
        </div>

        <div class="section" id="questionSection" style="display:none;">
            <h3>📋 Interview Question</h3>
            <div id="question"></div>
            <textarea id="answer" placeholder="Type your detailed answer here..."></textarea>
            <button class="button" onclick="submitAnswer()">📊 Submit & Get Evaluation</button>
        </div>

        <div class="section" id="resultsSection" style="display:none;">
            <h3>📈 Results</h3>
            <div id="results"></div>
        </div>

        <div class="section" id="aiAnswerSection" style="display:none;">
            <h3>🤖 AI Generated Answer</h3>
            <div id="aiAnswer"></div>
        </div>
    </div>

    <script>
        let currentQuestion = '';

        function getQuestion() {
            const role = document.getElementById('role').value;
            const round = document.getElementById('round').value;
            
            fetch('/api/question', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({role, round})
            })
            .then(response => response.json())
            .then(data => {
                currentQuestion = data.question;
                document.getElementById('question').innerHTML = `<strong>${data.question}</strong>`;
                document.getElementById('questionSection').style.display = 'block';
                document.getElementById('resultsSection').style.display = 'none';
                document.getElementById('aiAnswerSection').style.display = 'none';
            });
        }

        function submitAnswer() {
            const answer = document.getElementById('answer').value;
            if (!answer.trim()) {
                alert('Please provide an answer');
                return;
            }

            fetch('/api/evaluate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: currentQuestion, answer})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('results').innerHTML = `
                    <div class="score">🎯 Overall Score: ${data.overall_score}/10</div>
                    <div class="feedback">💡 Feedback: ${data.feedback}</div>
                    <div class="feedback">✨ Improved Answer: ${data.improved_answer}</div>
                `;
                document.getElementById('resultsSection').style.display = 'block';
            });
        }

        function showAIAnswer() {
            if (!currentQuestion) {
                alert('Please get a question first');
                return;
            }

            fetch('/api/ai-answer', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: currentQuestion})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('aiAnswer').innerHTML = `<div class="feedback">${data.ai_answer}</div>`;
                document.getElementById('aiAnswerSection').style.display = 'block';
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/question', methods=['POST'])
def get_question():
    data = request.json
    role = data.get('role', 'sde')
    round_type = data.get('round', 'technical')
    
    # Try Lambda API
    lambda_url = os.getenv('LAMBDA_API_URL')
    if lambda_url:
        try:
            response = requests.post(f"{lambda_url}/question", 
                                   json={
                                       'difficulty': 'medium',
                                       'category': round_type,
                                       'role': role,
                                       'personality': 'friendly'
                                   }, timeout=10)
            
            if response.status_code == 200:
                return jsonify(response.json())
        except:
            pass
    
    # Fallback to mock
    questions = ROLE_QUESTIONS.get(role, {}).get(round_type, ["Tell me about yourself"])
    question = random.choice(questions)
    return jsonify({'question': question})

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    question = data.get('question', '')
    answer = data.get('answer', '')
    
    # Try Lambda API
    lambda_url = os.getenv('LAMBDA_API_URL')
    if lambda_url:
        try:
            response = requests.post(f"{lambda_url}/evaluate", 
                                   json={
                                       'question': question,
                                       'answer': answer,
                                       'category': 'technical',
                                       'role': 'sde'
                                   }, timeout=15)
            
            if response.status_code == 200:
                return jsonify(response.json())
        except:
            pass
    
    # Fallback to mock
    scores = {
        'technical_accuracy': random.randint(6, 10),
        'clarity': random.randint(6, 10),
        'confidence': random.randint(5, 9),
        'communication': random.randint(6, 10),
        'relevance': random.randint(7, 10)
    }
    
    overall = round(sum(scores.values()) / 5, 1)
    
    return jsonify({
        'overall_score': overall,
        'feedback': f'Good answer! Score: {overall}/10. Consider adding more specific examples.',
        'improved_answer': 'Your answer could be enhanced by including concrete examples and quantifiable results.'
    })

@app.route('/api/ai-answer', methods=['POST'])
def ai_answer():
    data = request.json
    question = data.get('question', '')
    
    ai_response = f"Ideal answer for '{question[:50]}...': A comprehensive response would include specific examples, technical details, step-by-step approach, and practical implementation considerations."
    
    return jsonify({'ai_answer': ai_response})

if __name__ == '__main__':
    app.run(debug=True)