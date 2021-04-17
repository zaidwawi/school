import os
from flask import (Flask, request, abort, jsonify, render_template, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Questions, rollback
from flask_sqlalchemy import sqlalchemy
import random


def create_app(test_config=None):

    # create and configure the app

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    db = SQLAlchemy(app)

    QUESTIONS_PER_PAGE = 4
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)  
        start = (page - 1) * QUESTIONS_PER_PAGE       
        end = start + QUESTIONS_PER_PAGE              

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    @app.route('/')
    def index():
        question = Questions.query.order_by("id").first()

        return render_template('home.html', ss = question)
    
    @app.route('/questions')
    def show_questions():
        question = Questions.query.all()
        current_question = paginate_questions(request, question)
        current_questions = len(question)
        
        return render_template('questions.html', current_ques=current_question, total = current_questions, question=question )

    
    @app.route('/add-question', methods=['GET'])
    def get_question():
        return render_template('add-question.html')

    
    @app.route('/add-question', methods=['POST'])
    def question():
        body = request.get_json()
        school = Questions()
    
        school.title = request.form.get('title', '')
        school.answer = request.form.get('answer', '')
        school.youtube_link = request.form.get('youtube', '')
        school.docs_link = request.form.get('doc', '')
        school.image_link = request.form.get('image', '')
        school.subject = request.form.get('subject', '')
        school.difficulty = request.form.get('difficulty', '')
        school.insert()
    
        return redirect(url_for('index'))


    @app.route('/questions/<int:ques_id>', methods=['GET'])
    def get_question_details(ques_id):
        the_question = Questions.query.get(ques_id)
        ques = Questions.query.all()
        title = the_question.title
        image = the_question.image_link
        docs = the_question.docs_link
        youtube = the_question.youtube_link
        answer = the_question.answer
        subject = the_question.subject
        difficulty = the_question.difficulty


        return render_template('page.html', title=title, image=image, docs=docs, youtube = youtube, answer=answer, subject=subject, difficulty=difficulty, the_ques = ques)

    
    @app.route('/delete/<int:ids>', methods=['POST', "GET"])
    def delete(ids):
        deletes = Questions.query.get(ids).delete()
        db.session.commit()
        return redirect(url_for('index'))

    
    @app.route('/search', methods=['get'])
    def search():
        return render_template('search.html')
        
    @app.route('/search', methods=['POST']) # now we will set a search statement 
    def search_questions():

        # Get search term from request data
        search_term = request.form.get('search', None)

        # Return 422 status code if empty search term is sent
        if search_term == '':
            return render_template('search.html')

        try:
            # get all questions that has the search term substring
            if search_term:
                questions = Questions.query.filter(
                Questions.title.ilike(f'%{search_term}%')).all()

            # if there are no questions for search term return 404
            if len(questions) == 0:
                abort(404)

            # paginate questions
        
        except Exception as e:
            print(e)


        return render_template('search.html', data=questions)
    return app


APP = create_app()

if __name__ == '__main__':
    APP.run()
