from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    filter_by = request.args.get("filter", "all")
    if filter_by == "completed":
        tasks = Task.query.filter_by(completed=True).all()
    elif filter_by == "pending":
        tasks = Task.query.filter_by(completed=False).all()
    else:
        tasks = Task.query.all()
    return render_template('index.html', tasks=tasks, filter_by=filter_by)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    if content:
        task = Task(content=content)
        db.session.add(task)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    task = Task.query.get_or_404(id)
    new_content = request.form[f'edit-{id}']
    task.content = new_content
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
