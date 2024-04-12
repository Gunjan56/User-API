from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.model.model import db, User, Post, Liked_Post
from app.utils.error_response import error_response
from app.utils.success_response import success_response

like_bp = Blueprint('like', __name__)

@like_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    post = Post.query.get(post_id)
    if not current_user or not post:
        error_response(404, 'User or Post not found')

    like = Liked_Post(
        user_id=current_user_id,
        post_id=post.id,
        is_like=True
    )
    db.session.add(like)
    db.session.commit()
    return success_response(200, 'success','post liked')
