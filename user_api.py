from flask import Blueprint, jsonify, make_response, request
from orm import db_session
from orm.users import User

jobs_api = Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@jobs_api.route('/api/user')
def get_jobs():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'jobs': [x.to_dict() for x in users]
        }
    )
