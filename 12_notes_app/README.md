# Personal Notes App

A simple Flask web application for managing personal notes with HTML templating.

## Features

- Add new notes via a web form
- View all notes in a clean, organized list
- In-memory storage (notes are lost when server restarts)
- Responsive design with basic CSS styling

## Setup & Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python3 app.py
   ```

3. Open your browser and go to: `http://127.0.0.1:5002`

## Usage

- Visit `/` to see all your notes
- Visit `/add` to add a new note
- Submit the form to save your note and return to the main page

## Project Structure

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html      # Base template with CSS styling
│   ├── index.html     # Home page showing all notes
│   └── add.html       # Form page for adding notes
└── README.md          # This file
```

*Implementation assisted by Claude AI*