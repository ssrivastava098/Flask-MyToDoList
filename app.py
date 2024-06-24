from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
# Using SQlite as database here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Defining the schema of our database
class ToDo(db.Model):
    Slno = db.Column(db.Integer, primary_key=True)
    ToDo_Title = db.Column(db.String(200), nullable=False)
    ToDo_Desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # This is where we define what will be printed when we print any object of the ToDo class
    def __repr__(self):
        return f'<ToDo Title -> {self.ToDo_Title} ToDo Serial Number -> {self.Slno}>'

# Side Notes
# After doing all these, python interpreter was opened in the terminal and the following commands were executed
# from app import db
# db.create_all()
# exit()
# This created ToDo.db
# This created our database
# The name and type of database got defined from this line "'sqlite:///ToDo.db'"
# It determines the type of Database i.e. sqlite or mysql and then the name of the database.


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
# this a jinja technique to pass a python variable or object into a html file where it can be rendered as per our liking
# in the above code we have extracted all todos in a python object allToDo of class ToDo 

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
