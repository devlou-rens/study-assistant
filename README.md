# AI Reviewer — Free AI Study Assistant

## Project Overview

AI Reviewer (Agents) is a free web application that converts study materials such as notes, PDFs, and Word documents into structured study reviewers and flashcard quizzes using AI.

The application helps students quickly understand complex topics by generating summaries, explanations, examples, and review questions automatically.

## Project Structure

```
study-assistant/
│
├── manage.py
├── requirements.txt
├── study-assistant/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── assistant/
    ├── __init__.py
    ├── urls.py
    ├── views.py
    ├── static/
    │   └── assistant/
    │       ├── css/
    │       │   └── style.css
    │       └── js/
    │           └── app.js
    │
    └── templates/
        └── assistant/
            ├── base.html
            ├── index.html
            ├── result.html
            └── history.html
```

## Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/devlou-rens/study-assistant.git
cd study-assistant
```

2. **Create a Virtual Environment**

```bash
python -m venv venv
```

Activate the environment:

Windows

```
venv\Scripts\activate
```

macOS / Linux

```
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

Main dependencies include:

* Django
* pdfplumber
* python-docx
* Pillow

4. **Configure Environment Variables**

Create a `.env` file in the project root and add your API key.

```
ANTHROPIC_API_KEY=your_api_key_here
```

5. **Run Database Migrations**

```bash
python manage.py migrate
```

6. **Start the Development Server**

```bash
python manage.py runserver
```

7. **Access the Application**

Open your browser and go to:

```
http://127.0.0.1:8000/
```

## Features

* Text input for study notes
* PDF file upload support
* Word document (.docx) support
* AI-generated study reviewers
* Flashcard quizzes with flip interaction
* Difficulty levels (Easy, Medium, Hard)
* Session-based history
* Minimal dark theme interface

## Supported Content Types

| Type | Format      |
| ---- | ----------- |
| Text | Plain text  |
| PDF  | .pdf        |
| Word | .docx, .doc |

## Difficulty Levels

| Level  | Description                               |
| ------ | ----------------------------------------- |
| Easy   | Basic definitions and simple explanations |
| Medium | Balanced explanations with examples       |
| Hard   | Deeper explanations and technical details |

## Running in Production

Install Gunicorn:

```bash
pip install gunicorn
```

Run the server:

```bash
gunicorn study_assistant.wsgi:application --bind 0.0.0.0:8000
```

Make sure to configure the following in `settings.py`:

```
DEBUG = False
SECRET_KEY = your-secret-key
```

## Common Issues

**API Key Not Configured**

Ensure the environment variable `ANTHROPIC_API_KEY` is properly set.

**Module Not Found Errors**

Activate the virtual environment before running the server.

**File Upload Errors**

Check that the file type is supported and the file size does not exceed the allowed limit.
 
## Acknowledgments

* OpenRouter for providing access to AI models.
* Arcee AI for the Trinity Large Preview model.
* The Django community for the web framework.

## License

This project is intended for educational use.
