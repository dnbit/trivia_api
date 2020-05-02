import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE')
    return response


  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    
    if not categories:
      abort(404)

    formatted_categories = format_categories(categories)
    
    data = {
      'success': True,
      'categories': formatted_categories,
    }

    return jsonify(data)


  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    
    questions = Question.query.all()
    
    total_questions = len(questions)
    processed_questions = process_questions(questions, page)

    if not processed_questions:
      abort(404)

    categories = Category.query.all()
    formatted_categories = format_categories(categories)

    data = {
      'success': True,
      'questions': processed_questions,
      'total_questions': total_questions,
      'categories': formatted_categories,
      'current_category': None
    }

    return jsonify(data)

  def process_questions(questions, page):
    sliced_questions = slice_questions(questions, page)
    return format_questions(sliced_questions)

  def slice_questions(questions, page):
    end = page * QUESTIONS_PER_PAGE
    start = end - QUESTIONS_PER_PAGE
    return questions[start:end]
  

  def format_questions(questions):
    formatted_questions = []
    for question in questions:
      formatted_questions.append(question.format())
    
    return formatted_questions

  def format_categories(categories):
    formatted_categories = {}
    for category in categories:
      formatted_categories[category.id] = category.type
    
    return formatted_categories


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.get(question_id)

    if not question:
      abort(404)

    try:
      question.delete()
    except:
      abort(422)
    
    result = {
      "success": True,
      "deleted": question_id
    }

    return jsonify(result)


  @app.route('/questions', methods=['POST'])
  def create_new_question():
    body = json.loads(request.data)

    if not body:
      abort(400)

    question = body['question']
    answer = body['answer']
    difficulty = body['difficulty']
    category = body['category']

    new_question = Question(question=question, answer=answer, 
                            difficulty=difficulty, category=category)

    new_question.insert()

    result = {
      "success": True,
      "item": new_question.format()
    }

    return jsonify(result)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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


  @app.errorhandler(400)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Not found'
    }), 404

  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable Entity'
    }), 422
  

  return app
