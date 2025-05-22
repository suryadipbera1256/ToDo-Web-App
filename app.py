from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ToDo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ToDo(db.Model):
    No = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Todo({self.No},{self.title},{self.desc},{self.date_created})"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    try:
        if request.method == 'POST':
            title = request.form.get('title')
            desc = request.form.get('desc')
            if not title or not desc:
                logger.warning("Title or description missing in form data")
            else:
                todo = ToDo(title=title, desc=desc)
                db.session.add(todo)
                db.session.commit()
        alltodo = ToDo.query.all()
        return render_template('index.html', alltodo=alltodo)
    except Exception as e:
        logger.error(f"Error in hello_world route: {e}")
        return "An error occurred", 500


@app.route('/delete/<int:No>')
def delete(No):
    try:
        todo = ToDo.query.filter_by(No=No).first()
        if todo:
            db.session.delete(todo)
            db.session.commit()
        else:
            logger.warning(f"Delete requested for non-existent ToDo No: {No}")
        return redirect('/')
    except Exception as e:
        logger.error(f"Error in delete route: {e}")
        return "An error occurred", 500


@app.route('/update/<int:No>', methods=['GET', 'POST'])
def update(No):
    try:
        todo = ToDo.query.filter_by(No=No).first()
        if not todo:
            logger.warning(f"Update requested for non-existent ToDo No: {No}")
            return redirect('/')
        if request.method == 'POST':
            title = request.form.get('title')
            desc = request.form.get('desc')
            if not title or not desc:
                logger.warning("Title or description missing in update form data")
            else:
                todo.title = title
                todo.desc = desc
                db.session.add(todo)
                db.session.commit()
                return redirect('/')
        return render_template('update.html', todo=todo)
    except Exception as e:
        logger.error(f"Error in update route: {e}")
        return "An error occurred", 500


if __name__ == "__main__":
    app.run(debug=False, port=8000)
