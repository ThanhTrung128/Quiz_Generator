```
1. Create a new environment: venv or conda
2. activate the environment: pip install -r requirements.txt
3. Access to https://platform.openai.com/docs/guides/chat to get API_KEY and fill in the API_KEY to app.py
4. Run python app.py
5. Request via postman with json body

http://localhost:5000/generate_quiz
method: POST
{
    "input_type": "url",
    "input_data" : "https://en.wikipedia.org/wiki/L%C3%BD_S%C6%A1n_district",
    "num_questions": 3,
    "question_type": "true_false",
    "language_type":"vietnamese",
    "difficulty_type":"medium"
}

input_text : text, url
input_data: url link , paragraph
num_questions: number of questions which want to generate in a quiz
question_type: thr type of question: true_false, multiple_choice, short_answer
language_type: the language what you want to generate
difficulty_type: the level of question
```
