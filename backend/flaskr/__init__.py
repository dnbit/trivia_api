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
    
    result = {
      'success': True,
      'categories': formatted_categories,
    }

    return jsonify(result)


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

    result = {
      'success': True,
      'questions': processed_questions,
      'total_questions': total_questions,
      'categories': formatted_categories,
      'current_category': None
    }

    return jsonify(result)


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

    new_question = None
    try:
      question = body['question']
      answer = body['answer']
      difficulty = body['difficulty']
      category = body['category']

      new_question = Question(question=question, answer=answer, 
                              difficulty=difficulty, category=category)

      new_question.insert()
    except:
      abort(400)

    result = {
      "success": True,
      "item": new_question.format()
    }

    return jsonify(result)


  @app.route('/questions/search', methods=['POST'])
  def search_question():
    body = json.loads(request.data)
    page = request.args.get('page', 1, type=int)

    search_term = ''
    try:
      search_term = body['search_term']
    except:
      abort(400)
      
    questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    
    total_questions = len(questions)
    processed_questions = process_questions(questions, page)

    if not processed_questions:
      abort(404)

    categories = Category.query.all()
    formatted_categories = format_categories(categories)

    result = {
      'success': True,
      'questions': processed_questions,
      'total_questions': total_questions,
      'categories': formatted_categories,
      'current_category': None
    }

    return jsonify(result)


  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questiosn_by_category(category_id):  
    page = request.args.get('page', 1, type=int)
    
    questions = Question.query.filter_by(category = category_id).all()
    
    total_questions = len(questions)
    processed_questions = process_questions(questions, page)

    if not processed_questions:
      abort(404)

    categories = Category.query.all()
    formatted_categories = format_categories(categories)

    result = {
      'success': True,
      'questions': processed_questions,
      'total_questions': total_questions,
      'categories': formatted_categories,
      'current_category': category_id
    }

    return jsonify(result)


  @app.route('/quizzes', methods=['POST'])
  def play_quizz():
    body = json.loads(request.data)

    next_question = {}
    try:
      previous_questions = body['previous_questions']
      quiz_category = body['quiz_category']['id']

      questions = []
      if quiz_category != 0:
        questions = Question.query.filter_by(category = quiz_category).all()
      else:
        questions = Question.query.all()

      for question in questions:
        if question.id not in previous_questions:
          next_question = question.format()
          break
    except:
      abort(400)
    
    result = {
      'success': True,
      'question': next_question
    }

    return jsonify(result)


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
