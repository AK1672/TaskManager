from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    due = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method == "POST":
        title=request.form['title']
        desc=request.form['desc']
        due=request.form['due']
        todo = Todo(title = title, desc = desc, due=due)
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo.query.all()
    return render_template('index.html', alltodo = alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    dl = Todo.query.filter_by(sno=sno).first()
    db.session.delete(dl)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title=request.form['title']
        desc=request.form['desc']
        due=request.form['due']
        up = Todo.query.filter_by(sno=sno).first()
        up.title = title
        up.desc = desc
        up.due = due
        db.session.add(up)
        db.session.commit()
        return redirect("/")

    up = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = up)




if __name__=="__main__":
    app.run(debug=False)