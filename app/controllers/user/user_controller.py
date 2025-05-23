from flask import Flask, Blueprint, request,jsonify
from app.status_codes import HTTP_200_OK,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_202_ACCEPTED,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT
import validators
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user_model import User

users = Blueprint('users', __name__, url_prefix='api/vi/users')

# getting all the users
@users.get('/all')
# @jwt_required()
def get_all_users():
    
    try:
        all_users = User.query.all()
        
        user_data =[]
        
        for user in all_users:
            user_info ={
                'id':user.id,
                'email': user.email,
                # 'password':user.password,
                'userType': user.userType
            }
            user_data.append(user_info)
        
        return jsonify({
            'message':'All users successfully retrive',
            'total_users':len(user_data),
            'user':user_data
        }),HTTP_200_OK
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
        
        
# get a user by id
@users.get('users/<int:id>')
def get_users(id):
    
    try:
        user = User.query.filter_by(id=id).first()
        
        if not user:
            return jsonify({
                'error':'User not found'
            }), HTTP_400_BAD_REQUEST
        
       
        user_info ={
                'id':user.id,
                'userName': user.userName,
                'email': user.email,
                # 'password':user.password,
                'userType': user.userType
            }
        
        return jsonify(user_info)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
        
# updating user details

@users.route('/edit/<int:id>', methods =['PUT', 'PATCH'])
def update_user(id):
    
    try:
        
        users = User.query.filter_by(id=id).first()
        
        if not users:
            return jsonify({
                'error': 'User not found'
            }), HTTP_409_CONFLICT
            
        else:
            new_userName = request.get_json('userName', users.userName)
            new_email = request.get_json('email', users.email)
            new_userType = request.get_json('userType', users.userType)
            
        if new_userName != users.userName and User.query.filter_by(userName = new_userName).filter_by():
            return jsonify({
                'error': 'user already in use'
            }), HTTP_409_CONFLICT
        
        
        if new_email != users.email and User.query.filter_by(email = new_email).filter_by():
            return jsonify({
                'error': 'email already in use'
            }), HTTP_409_CONFLICT
            
        # updating user details
        users.userName = new_userName
        users.email = new_email
        users.userType = new_userType
        
        db.session.commit()
        
        return jsonify({
            'meassage': 'Update successful',
            
            'user':{
                'id': users.id,
                'userName': users.userName,
                'email': users.email
            }
        })
    except Exception as e:
        return jsonify ({
            'error':str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR


# deleting a user
@users.route('/delete/<int:id>', methods =['DELETE'])
def delete_usert(id):
    
    try:
        
        # get student by id
        user = User.query.filter_by(id=id).first()
        
        if not user:
            return jsonify({
                'error':'user not found'
            }), HTTP_400_BAD_REQUEST
                   
            
        db.session.delete(user)
        db.session.commit()
        
        
                
        return jsonify({
            'message': 'user deleted ',
            
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error':str(e)
        }), HTTP_400_BAD_REQUEST