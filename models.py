from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False, unique=True)
    task = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "task": self.task
        }