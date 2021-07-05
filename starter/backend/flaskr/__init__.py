import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # CORS(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: DONE
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
      try:
          cat_dict = {}
          categories = Category.query.order_by(Category.id).all()
          for category in categories:
            cat_dict[category.id] = category.type
      except: 
          print(sys.exc_info())
          abort(422)

      return jsonify({
            'success': True,
            'categories': cat_dict
        })
  '''
  @TODO: DONE 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
      try:
        # pagenate Questions
          page = request.args.get('page', 1, type=int)
          questions = Question.query.paginate(page, per_page=QUESTIONS_PER_PAGE)
          formatted_questions = [question.format() for question in questions.items]
        # Category
          cat_dict = {}
          categories = Category.query.order_by(Category.id).all()
          for category in categories:
            cat_dict[category.id] = category.type
      except: 
          print(sys.exc_info())
          abort(404)
      return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions':questions.total,
            'categories':cat_dict ,
            'currentCategory': cat_dict
        })
  '''
  @TODO: DONE
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        
        try: 
            question.delete()
        except:
            print(sys.exc_info())
            abort(500)

        return jsonify({
            'success': True,
            'deleted': question_id,
        })
  '''
  @TODO: DONE
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
      questionData = request.get_json()
      try:
          question = Question(
              question=questionData['question'],
              answer=questionData['answer'],
              category = questionData['category'],
              difficulty = questionData['difficulty']
          )
          question.insert()
      except:
          print(sys.exc_info())
          abort(422)
      return jsonify({
            'success': True
        })
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search_query', methods=['POST'])
  def search_questions():
      try:
          body = request.get_json()
          search_term = body.get('searchTerm')
          questions = Question.query.filter(Question.question.ilike("%"+search_term+"%")).all()
          formatted_questions = [question.format() for question in questions]
      except: 
          print(sys.exc_info())
      return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions':len(formatted_questions)
        })
  '''
  @TODO: DONE
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
      try:
          questions = Question.query.filter(Question.category == category_id)
          formatted_questions = [question.format() for question in questions]
        # Category
          cat_dict = {}
          categories = Category.query.filter(Category.id == category_id).one_or_none()
      except: 
          print(sys.exc_info())
      return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions':len(formatted_questions),
            'currentCategory': categories.type
        })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
      try:
          # quesz_question = {}
          body = request.get_json()
          
          previous_questions = body.get('previous_questions')
          
          quiz_category = body.get('quiz_category')
          quiz_category = quiz_category['id']

          questions = Question.query
          # when user select all category
          if quiz_category != 0:  
              questions = questions.filter(Question.category == quiz_category)
          
          questions = questions.filter(Question.id.notin_(previous_questions)).all()  
          
          formatted_questions = [question.format() for question in questions]
          quesz_question = random.choice(formatted_questions)
      except: 
          print(sys.exc_info())
      return jsonify({
            'success': True,
            'questions': quesz_question
        })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
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

    