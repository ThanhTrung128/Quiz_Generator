import re

def parse_multiple_choices_quiz(text_lines):
    content_processing = text_lines.strip().split('\n')
    question_regex = re.compile(r'^\s*(?:Q(?:uestion)?|[\d.]+[)\.]?\s*):?\s*(.*)$')
    answer_regex = re.compile(r'^(Answer:|Answer\s:|A:|Đáp án:|Correct Answer:|Câu trả lời đúng:)\s*(.*)$')
    
    questions = []
    answers = []
    options = []
    question_text = None
    answer_text = None
    question_id = 0
    answer_id = 0
    temp_options = []

    for num, line in enumerate(content_processing):
        match = question_regex.match(line)
        if match and line.strip().endswith('?'):
            if len(temp_options) > 0:
                options.append(temp_options)
                temp_options = []
            question_id += 1
            question_text = match.group(1).strip()
            questions.append(question_text)
            if question_id != answer_id + 1:
                answer_text = None
                answers.append(answer_text)
                answer_id += 1
        elif answer_regex.match(line):
            answer_id += 1
            answer_text = answer_regex.match(line).group(2).strip() 
            answers.append(answer_text)
        else:
            if len(line) > 1:
                temp_options.append(line)
        if num == len(content_processing) - 1 and question_id != answer_id:
            answer_text = None
            answers.append(answer_text)
            options.append(temp_options)

    return [{'question': question, 'options': options, 'answer': answer} for question, options, answer in zip(questions, options, answers)]

def parse_true_false_quiz_type_1(text_lines):
    text_content = text_lines
    text_lines = text_lines.strip().split('\n')
    questions = []
    answers = []    
    flag = 0
    pattern_check = r'((?:(q|Q|Question|question)(\d+)[.|:])|(\d+)[.|:])\s(.*?)(?:\?\s*|\.\s+) (.+)(?:(?:\/\w+:\s*)?(\w+))?'
    if re.match(pattern_check,text_lines[1]):
        flag = 1
        
    if flag == 0: 
        pattern = r'(^[1-9]\d*\.|^Q\d[:.]|^q\d[:.])\s*'
        question_id = 0
        answer_id = 0
        question_text = None
        answer_text = None 

        for num,line in enumerate(text_lines):
            if len(line) > 1:
                match = re.match(pattern, line)
                if match:
                    question_text = re.sub(pattern, '', line)
                    questions.append(question_text)
                    question_id += 1
                    if question_id != answer_id + 1:
                        answer_text = None
                        answers.append(answer_text)
                        answer_id += 1
                else:
                    answer_text = line
                    answers.append(answer_text)
                    answer_id += 1
            if num == len(text_lines) - 1 and question_id != answer_id:
                answer_text = None
                answers.append(answer_text)
    else:
        pattern = r'(?i)(?:((q|Q|Question|question)(\d+)[.|:])|(\d+\.?))\s*(.*?)(?:[?\.]\s*|\s*(?:True|False|Đúng|Sai)\s*:?\s*)(.*)'
        matches = re.findall(pattern, text_content)
        for match in matches:
            question = match[4].strip()
            questions.append(question)
            answer = match[5] if match[5] else None
            answers.append(answer)
    return [{'question': question, 'answer': answer} for question, answer in zip(questions, answers)]
def parse_true_false_quiz(text_lines):
    result = None
    if len(text_lines.strip().split('\n\n')) == 2:
        result = parse_short_answer(text_lines)
    else:
        result =  parse_true_false_quiz_type_1(text_lines)
    return result

def parse_short_answer(text_lines):
    try:
        text_lines = text_lines.strip().split('\n\n')
        questions = text_lines[0].split('\n')
        answers = text_lines[1].split('\n') if len(text_lines) > 1 else [None] * len(questions)
        return [{'question': q, 'answer': a} for q, a in zip(questions, answers)]
    except:
        return []