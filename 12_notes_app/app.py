from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

notes = []

@app.route('/')
def index():
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        note_content = request.form.get('content')
        if note_content and note_content.strip():
            notes.append(note_content.strip())
        return redirect(url_for('index'))
    
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True, port=5002)