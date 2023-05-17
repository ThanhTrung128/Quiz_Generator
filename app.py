from flask import Flask, jsonify, request
import requests
from data_processing.text_process import parse_multiple_choices_quiz,parse_true_false_quiz,parse_short_answer

app = Flask(__name__)
API_KEY = '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'

# QUESTION_TYPE_PROMPTS = {
#     'multiple_choice': 'Generate {num} multiple choice questions based on the following {in_type}:\n{data}\n',
#     'true_false': 'Generate {num} true/false questions, each with correct answer based on the following {in_type}:\n{data}\n',
#     'short_answer': 'Generate {num} short answer questions and answer  based on the following {in_type}:\n{data}\n',
# }

QUESTION_TYPE_PROMPTS = {
    'multiple_choice': 'Generate {num} multiple-choice questions in {language}, each with four options, correct answer and also follow the {in_type}:\n{data}\n',
    'true_false': 'Generate {num} true/false format questions in {language}, each with correct answer. The difficulty level is {difficulty_level} and also follow the {in_type}:\n{data}\n',
    'short_answer': 'Generate {num} short answer questions and answer questions in {language}. The difficulty level is {difficulty_level} and also follow the {in_type}:\n{data}\n',
}

def generate_quiz_questions(prompt,question_type,num_questions):
    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'text-davinci-003',
            'prompt': prompt,
            'temperature': 0.5,
            'max_tokens': int(num_questions)*128,
            'n': 1,
            'stop': None
        }
    )
    if response.ok:
        output = response.json()['choices'][0]['text'].strip()
        result = None
        print(output)
        # response_json = response.json()
        if question_type == 'multiple_choice':
            result = parse_multiple_choices_quiz(output)
        elif question_type == 'true_false':
            result = parse_true_false_quiz(output)
        elif question_type == 'short_answer':
            result = parse_short_answer(output)
        return result

    response.raise_for_status()


@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    try:
        data = request.get_json()
        input_type = data.get('input_type')
        input_data = data.get('input_data')
        num_questions = data.get('num_questions')
        question_type = data.get('question_type')
        language_type = data.get('language_type')
        difficulty_type = data.get('difficulty_type')
        if not input_data or not question_type:
            raise ValueError('Invalid input')
        
        prompt = QUESTION_TYPE_PROMPTS[question_type].format(
            num=num_questions, in_type = input_type, data=input_data,language = language_type,difficulty_level = difficulty_type
        )
        quiz_questions = generate_quiz_questions(prompt,question_type,num_questions)
        return jsonify({'quiz_questions': quiz_questions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)