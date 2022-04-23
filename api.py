from flask import Flask, make_response, jsonify
from user_api import user_api
from orm import db_session

app = Flask(__name__)
app.register_blueprint(user_api)

db_session.global_init("db/flea.db")


@app.route('/')
def index():
    return 'Main page'


@user_api.errorhandler(404)
def error_404(error):
    return make_response(jsonify({
        'error': 'Jobs not found!'
    }), 404)


app.run()