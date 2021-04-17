from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
import os

database_path = os.environ["DATABASE_URL"]
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def rollback():
    db.session.rollback()


class Questions(db.Model):
    __tablename__ = "Questions"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    answer = Column(String, nullable=False)
    youtube_link = Column(String, nullable=False)
    docs_link = Column(String, nullable=False)
    image_link = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "answer": self.answer,
            "youtube_link": self.youtube_link,
            "docs_link": self.docs_link,
            "image_link": self.image_link,
            "subject": self.subject,
            "difficulty": self.difficulty
            }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
