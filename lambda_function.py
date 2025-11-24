import json
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    path = event.get('path', '')
    body = json.loads(event.get('body', '{}'))
    
    if path == '/question':
        return generate_question(body)
    elif path == '/evaluate':
        return evaluate_answer(body)
    
    return {'statusCode': 404, 'body': json.dumps({'error': 'Not found'})}

def generate_question(data):
    difficulty = data.get('difficulty', 'easy')
    category = data.get('category', 'technical')
    personality = data.get('personality', 'friendly')
    
    personalities = {
        'friendly': 'Ask in a warm, encouraging tone',
        'strict': 'Ask in a direct, no-nonsense professional manner', 
        'expert': 'Ask with deep technical expertise and precision'
    }
    
    prompt = f"""
    Generate a {difficulty} level {category} interview question.
    {personalities[personality]}.
    
    Categories:
    - Technical: Programming, system design, algorithms
    - HR: Experience, teamwork, goals, challenges
    - Behavioral: Situational, problem-solving, leadership
    
    Return only the question, no extra text.
    """
    
    response = bedrock.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body=json.dumps({
            'inputText': prompt,
            'textGenerationConfig': {
                'maxTokenCount': 200,
                'temperature': 0.7
            }
        })
    )
    
    result = json.loads(response['body'].read())
    question = result['results'][0]['outputText'].strip()
    
    return {
        'statusCode': 200,
        'body': json.dumps({'question': question})
    }

def evaluate_answer(data):
    prompt = f"""
    Question: {data['question']}
    Answer: {data['answer']}
    
    Evaluate this interview answer on 5 criteria (1-10 each):
    1. Technical Accuracy - correctness of information
    2. Clarity - how clear and understandable
    3. Confidence - demonstrates self-assurance
    4. Communication - articulation and structure
    5. Relevance - directly addresses the question
    
    Also provide:
    - Overall score (average of 5 scores)
    - Constructive feedback (2-3 sentences)
    - Improved answer suggestion
    
    Return JSON format:
    {{
        "technical_accuracy": X,
        "clarity": X,
        "confidence": X,
        "communication": X,
        "relevance": X,
        "overall_score": X,
        "feedback": "...",
        "improved_answer": "..."
    }}
    """
    
    response = bedrock.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body=json.dumps({
            'inputText': prompt,
            'textGenerationConfig': {
                'maxTokenCount': 500,
                'temperature': 0.3
            }
        })
    )
    
    result = json.loads(response['body'].read())
    evaluation = json.loads(result['results'][0]['outputText'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(evaluation)
    }