from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable = False)
    date_create = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"
    
with app.app_context():
    db.create_all()


@app.route('/', methods=["GET","POST"])
def index():
    if request.method =="POST":
        title = request.form['title']
        content = request.form['desc']
        t1 = todo(title=title, content=content)
        db.session.add(t1)
        db.session.commit()
    alltodo = todo.query.all()
    print(alltodo)
    return render_template('index.html',allTodo = alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo = todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if request.method =="POST":
        title = request.form['title']
        content = request.form['desc']
        do = todo.query.filter_by(sno=sno).first()
        do.title=title
        do.content = content
        db.session.add(do)
        db.session.commit()
        return redirect("/")

    allTodo = todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=allTodo)

if __name__ == '__main__':
    app.run(debug=True,port=8000)