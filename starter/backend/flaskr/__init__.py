import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from sqlalchemy.sql.elements import Null
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        try:
            cat_dict = {}
            categories = Category.query.order_by(Category.id).all()
            for category in categories:
                cat_dict[category.id] = category.type
        except BaseException:
            print(sys.exc_info())
            abort(422)

        return jsonify({
            'success': True,
            'categories': cat_dict
        })

    @app.route('/questions')
    def get_questions():
        try:
            page = request.args.get('page', 1, type=int)
            questions = Question.query.paginate(
                page, per_page=QUESTIONS_PER_PAGE)
            formatted_questions = [question.format()
                                   for question in questions.items]
            cat_dict = {}
            categories = Category.query.order_by(Category.id).all()
            for category in categories:
                cat_dict[category.id] = category.type
        except BaseException:
            print(sys.exc_info())
            abort(404)
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions': questions.total,
            'categories': cat_dict,
            'currentCategory': cat_dict
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)

        try:
            question.delete()
        except BaseException:
            print(sys.exc_info())
            abort(500)

        return jsonify({
            'success': True,
            'deleted': question_id,
        })

    @app.route('/questions', methods=['POST'])
    def create_question():
        questionData = request.get_json()
        try:
            question = Question(
                question=questionData['question'],
                answer=questionData['answer'],
                category=questionData['category'],
                difficulty=questionData['difficulty']
            )
            question.insert()
        except BaseException:
            print(sys.exc_info())
            abort(422)
        return jsonify({
            'success': True
        })

    @app.route('/questions/search_query', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()
            search_term = body.get('searchTerm')
            questions = Question.query.filter(
                Question.question.ilike(
                    "%" + search_term + "%")).all()
            formatted_questions = [question.format() for question in questions]
        except BaseException:
            print(sys.exc_info())
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions': len(formatted_questions)
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        # categories_type = ''
        try:
            questions = Question.query.filter(Question.category == category_id)
            formatted_questions = [question.format() for question in questions]
        # Category
            cat_dict = {}
            categories = Category.query.filter(
                Category.id == category_id).one_or_none()
            categories_type = categories.type
        except BaseException:
            print(sys.exc_info())
            abort(500)
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions': len(formatted_questions),
            'currentCategory': categories_type
        })

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            quesz_question = {}
            body = request.get_json()

            previous_questions = body.get('previous_questions')

            quiz_category = body.get('quiz_category')
            quiz_category = quiz_category['id']

            questions = Question.query
            # when user select all category
            if quiz_category != 0:
                questions = questions.filter(
                    Question.category == quiz_category)

            questions = questions.filter(
                Question.id.notin_(previous_questions)).all()

            formatted_questions = [question.format() for question in questions]
            quesz_question = random.choice(formatted_questions)
        except BaseException:
            print(sys.exc_info())
        return jsonify({
            'success': True,
            'question': quesz_question
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
