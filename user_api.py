from flask import Blueprint, jsonify
from orm import db_session
from orm.users import User

user_api = Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@user_api.route('/api/user')
def get_jobs():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users': [x.to_dict() for x in users]
        }
    )
