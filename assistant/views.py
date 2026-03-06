import os
from datetime import datetime
from django.shortcuts import render, redirect
from openai import OpenAI

DIFFICULTY_RULES = {
    'easy': 'EASY - Use only basic definitions and very simple explanations. Avoid jargon.',
    'medium': 'MEDIUM - Provide explanations with real-world examples to illustrate ideas.',
    'hard': 'HARD - Include deeper analysis, edge cases, comparisons, and technical depth.',
}

SYSTEM_PROMPT = """You are a friendly AI Study Assistant helping students review and learn any topic.

OUTPUT FORMAT (STRICT):

1. Title
   [Create a clear, relevant title]

2. Key Concepts
   [List the most important ideas or terms as bullet points]

3. Explanation
   [Explain the topic in simple language using bullet points and short paragraphs]

4. Examples
   [Provide simple, clear examples or illustrations]

5. Quick Summary
   [Summarize in 3-5 bullet points]

6. Review Questions + Answers
   [Create 5-10 exam-style questions with clear answers]
   Q1: [question]
   A1: [answer]

========================
FLASHCARD QUIZ
========================

Create 10-20 flashcards. Each MUST follow this format exactly:

Flashcard 1
Q: [short, clear question]
A: [concise, student-friendly answer]

Flashcard 2
Q: [question]
A: [answer]

[continue for all flashcards]

RULES:
- Use simple, beginner-friendly language
- Use bullet points and short sections
- Keep answers short and easy to memorize
- Do NOT mention file types, uploads, sessions, cookies, or tech internals
- Do NOT reference yourself or the AI
- Do NOT ask follow-up questions
- No emojis"""


def get_client():
    from django.conf import settings
    api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def build_prompt(difficulty, extra_instructions=''):
    rule = DIFFICULTY_RULES.get(difficulty, DIFFICULTY_RULES['medium'])
    base = f"Difficulty Level: {rule}\n\nConvert the provided content into a structured Study Reviewer and Flashcard Quiz following the strict output format."
    if extra_instructions and extra_instructions.strip():
        base += f"\n\nExtra Instructions from the student: {extra_instructions.strip()}"
    return base


def call_ai_text(text_content, difficulty,  extra_instructions=''):
    client = get_client()
    prompt = build_prompt(difficulty, extra_instructions) + f"\n\nContent to study:\n{text_content}"
    response = client.chat.completions.create(
        model="arcee-ai/trinity-large-preview:free",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
    )
    return response.choices[0].message.content



def format_response(raw_text):
    sections = {'reviewer': '', 'flashcards': []}

    # Try multiple possible separators
    split_markers = [
        '========================\nFLASHCARD QUIZ\n========================',
        'FLASHCARD QUIZ\n========================',
        '========================\nFLASHCARD QUIZ',
        'FLASHCARD QUIZ',
        'Flashcard Quiz',
        'flashcard quiz',
    ]

    flashcard_text = ''
    for marker in split_markers:
        if marker in raw_text:
            idx = raw_text.index(marker)
            sections['reviewer'] = raw_text[:idx].strip()
            flashcard_text = raw_text[idx:].strip()
            break

    if not flashcard_text:
        # Check if flashcards exist by looking for "Flashcard 1"
        for marker in ['Flashcard 1', 'flashcard 1', 'FLASHCARD 1']:
            if marker in raw_text:
                idx = raw_text.index(marker)
                sections['reviewer'] = raw_text[:idx].strip()
                flashcard_text = raw_text[idx:].strip()
                break

    if not flashcard_text:
        sections['reviewer'] = raw_text
        return sections

    if flashcard_text:
        cards = []
        lines = flashcard_text.split('\n')
        current_card = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Match "Flashcard 1", "Flashcard 1:", "FLASHCARD 1" etc
            lower = line.lower()
            if lower.startswith('flashcard ') and not lower.startswith('flashcard quiz'):
                if current_card and current_card.get('q'):
                    cards.append(current_card)
                # Extract number
                parts = line.split(' ')
                num = parts[-1].rstrip(':').strip() if len(parts) > 1 else str(len(cards)+1)
                current_card = {'num': num, 'q': '', 'a': ''}
            elif line.startswith('Q:') and current_card is not None:
                current_card['q'] = line[2:].strip()
            elif line.startswith('A:') and current_card is not None:
                current_card['a'] = line[2:].strip()
            elif current_card and current_card.get('a') and line and not line.startswith('='):
                current_card['a'] += ' ' + line
        if current_card and current_card.get('q'):
            cards.append(current_card)
        sections['flashcards'] = cards

    return sections


def index(request):
    return render(request, 'assistant/index.html', {
        'history': request.session.get('study_history', [])
    })


def generate(request):
    if request.method != 'POST':
        return redirect('index')

    difficulty = request.POST.get('difficulty', 'medium')
    input_type = request.POST.get('input_type', 'text')
    extra_instructions = request.POST.get('extra_instructions', '').strip()
    topic = ''
    raw_response = ''
    error = None

    try:
        if input_type == 'text':
            text_content = request.POST.get('text_content', '').strip()
            if not text_content:
                error = 'Please enter some text content to study.'
            else:
                topic = text_content[:80] + ('...' if len(text_content) > 80 else '')
                raw_response = call_ai_text(text_content, difficulty, extra_instructions)

        elif input_type in ('pdf', 'document'):
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                error = 'Please upload a file.'
            else:
                topic = uploaded_file.name
                file_bytes = uploaded_file.read()

                if input_type == 'pdf':
                    try:
                        import io, pdfplumber
                        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                            text_content = '\n'.join([page.extract_text() or '' for page in pdf.pages])
                        raw_response = call_ai_text(text_content, difficulty, extra_instructions)
                    except Exception:
                        raw_response = call_ai_text(f"Document titled: {uploaded_file.name}", difficulty, extra_instructions)

                else:  # document / docx
                    try:
                        import docx, io
                        doc = docx.Document(io.BytesIO(file_bytes))
                        text_content = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
                        raw_response = call_ai_text(text_content, difficulty, extra_instructions)
                    except Exception:
                        raw_response = call_ai_text(f"Document titled: {uploaded_file.name}", difficulty, extra_instructions)

    except Exception as e:
        error = f'Something went wrong: {str(e)}'

    if error:
        return render(request, 'assistant/result.html', {
            'error': error, 'reviewer': '', 'flashcards': [],
            'topic': '', 'difficulty': difficulty,
        })

    sections = format_response(raw_response)
    import uuid
    history = request.session.get('study_history', [])

    # Trim reviewer to avoid exceeding cookie size limit
    reviewer_trimmed = sections['reviewer'][:3000] if sections['reviewer'] else ''
    flashcards_trimmed = sections['flashcards'][:15] if sections['flashcards'] else []

    history.insert(0, {
        'id': str(uuid.uuid4()),
        'topic': topic,
        'difficulty': difficulty,
        'timestamp': datetime.now().strftime('%b %d, %Y %I:%M %p'),
        'reviewer': reviewer_trimmed,
        'flashcards': flashcards_trimmed,
    })
    request.session['study_history'] = history[:20]
    request.session.modified = True

    return render(request, 'assistant/result.html', {
        'reviewer': sections['reviewer'], 'flashcards': sections['flashcards'],
        'topic': topic, 'difficulty': difficulty, 'error': None,
    })


def history(request):
    return render(request, 'assistant/history.html', {
        'history': request.session.get('study_history', [])
    })

def delete_history_item(request, item_id):
    if request.method == 'POST':
        history = request.session.get('study_history', [])
        history = [item for item in history if item.get('id') != item_id]
        request.session['study_history'] = history
        request.session.modified = True
    return redirect('history')


def clear_history(request):
    if request.method == 'POST':
        request.session['study_history'] = []
        request.session.modified = True
    return redirect('history')