# AI Study Assistant — Setup Guide

## Project Structure

```
study_assistant/
├── manage.py
├── requirements.txt
├── study_assistant/          ← Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── assistant/                ← Main app
    ├── __init__.py
    ├── urls.py
    ├── views.py
    ├── static/
    │   └── assistant/
    │       ├── css/
    │       │   └── style.css
    │       └── js/
    │           └── app.js
    └── templates/
        └── assistant/
            ├── base.html
            ├── index.html
            ├── result.html
            └── history.html
```

---

## Step-by-Step Setup

### Step 1: Install Python

Make sure Python 3.10 or higher is installed.

```bash
python --version
# Should print Python 3.10.x or higher
```

Download from https://www.python.org/downloads/ if needed.

---

### Step 2: Create a Virtual Environment

```bash
# Navigate to the project folder
cd study_assistant

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Django** — web framework
- **anthropic** — Claude AI SDK
- **python-docx** — for reading Word documents
- **Pillow** — image support

---

### Step 4: Get an Anthropic API Key

1. Go to https://console.anthropic.com
2. Create an account (free tier available)
3. Go to **API Keys** → **Create Key**
4. Copy your key (starts with `sk-ant-...`)

---

### Step 5: Set the API Key as Environment Variable

**On Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**On Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**On macOS/Linux:**
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

> Tip: Add this line to your `~/.bashrc` or `~/.zshrc` so it persists between terminal sessions.

---

### Step 6: Run Database Migrations

```bash
python manage.py migrate
```

> Note: This project uses signed cookie sessions — no actual database is needed for study history. This command just initializes Django's content type framework.

---

### Step 7: Start the Development Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

---

### Step 8: Open in Browser

Visit: **http://127.0.0.1:8000**

---

## How to Use

1. **Paste text** — type or paste any notes, textbook content, or study material
2. **Upload a PDF** — upload lecture slides, textbook PDFs
3. **Upload a Word Doc** — `.docx` files from your computer
4. **Upload an Image** — photos of handwritten notes, screenshots, typed notes
5. **Select difficulty** — Easy, Medium, or Hard
6. **Click Generate** — get your Study Reviewer + Flashcard Quiz instantly
7. **Flip flashcards** by clicking on them
8. **View History** tab to revisit past study sessions (stored in browser session for 24 hours)

---

## Content Types Supported

| Type | Format |
|------|--------|
| Text | Plain text input |
| PDF | `.pdf` files |
| Word | `.docx`, `.doc` |
| Image | `.jpg`, `.png`, `.webp`, `.gif` |

---

## Difficulty Levels

| Level | Description |
|-------|-------------|
| Easy | Basic definitions, very simple explanations |
| Medium | Explanations with examples (default) |
| Hard | Deep analysis, technical depth, edge cases |

---

## Running in Production

For a production deployment, consider:

```bash
pip install gunicorn

# Set a strong secret key
export SECRET_KEY=your-very-long-random-secret-key

# Set debug to false
# In settings.py: DEBUG = False

# Run with gunicorn
gunicorn study_assistant.wsgi:application --bind 0.0.0.0:8000
```

---

## Common Issues

**"API key not configured" error**
→ Make sure you ran `export ANTHROPIC_API_KEY=...` in the same terminal session.

**"Module not found" errors**
→ Make sure your virtual environment is activated: `source venv/bin/activate`

**File upload not working**
→ Check file size (max 10MB) and file type matches the selected tab.

**Flashcards not appearing**
→ The AI response may not have followed the expected format. Try again or check your content.
