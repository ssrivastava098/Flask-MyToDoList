from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    Slno = db.Column(db.Integer, primary_key=True)
    ToDo_Title = db.Column(db.String(200), nullable=False)
    ToDo_Desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<ToDo Title -> {self.ToDo_Title} ToDo Serial Number -> {self.Slno}>'

@app.route('/',  methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:
            todo = ToDo(ToDo_Title=title, ToDo_Desc=desc)
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for('hello'))
    allToDo = ToDo.query.all()
    # print(allToDo)
    return render_template('index.html', allToDo = allToDo)

@app.route('/update/<int:ToDoSlno>')
def update(ToDoSlno):
    updateToDo = ToDo.query.filter_by(Slno=ToDoSlno).first()
    return render_template('update.html', updateToDo = updateToDo)

    
@app.route('/doneUpdate/<int:ToDoSlno>', methods=['GET', 'POST'])
def fun(ToDoSlno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:
            updateToDo = ToDo.query.filter_by(Slno=ToDoSlno).first()
            updateToDo.ToDo_Title = title
            updateToDo.ToDo_Desc = desc
            db.session.commit()
    return redirect('/')


@app.route('/delete/<int:ToDoSlno>')
def delete(ToDoSlno):
    delToDo = ToDo.query.filter_by(Slno=ToDoSlno).first()
    if delToDo:
        db.session.delete(delToDo)
        db.session.commit()
    return redirect(url_for('hello'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
