from flask import Blueprint,request, jsonify
from app.status_codes import HTTP_200_OK ,HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
import validators
from app.models.user_model import User
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity


# registering blueprints
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# register a user

@auth.route('/register', methods = ['POST'])
def register_user():
    
    data = request.json
    
    userName = data.get(userName)
    email = data.get(email)
    password =data.get(password)
    userType = data.get(userType)
    

    if not userName or not email or not password or not userType:
        return jsonify({
            'error': 'All feilds required'
        }), HTTP_400_BAD_REQUEST
        
    if len(password) <8:
        return({
            'error': 'Short Password length'
        }), HTTP_400_BAD_REQUEST
        
    if not validators.email(email):
        return jsonify({
            'error': 'Invalid email'
        }), HTTP_400_BAD_REQUEST
        
    if userType not in['admin', 'client']:
        return({
            'error': 'User type not identitfied'
        })
        

    try :
        hashed_password = bcrypt.generate_password_hash(password)
        
        # creating a new user
        new_user = User(
            userName =userName, 
            password=hashed_password, 
            email=email)
        
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        db.session.rollback()
        
        # keeping track of user name
        new_user = new_user.user_info()
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
        
        
    
     #user login
@auth.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    try:
        if not password or not email:
            return jsonify({
                'Message': 'Email and Password are required'
            }), HTTP_400_BAD_REQUEST

        user = User.query.filter_by(email=email).first()
        
        if User:
            
            is_correct_password = bcrypt.check_password_hash(user.password,password)
            refresh_token = create_refresh_token(identity=user.id)


            if is_correct_password:
            
                access_token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))

                return jsonify({
                    'user':{
                        'id':user.id,
                        'user_name':user.user_info(),
                        'email':user.email,
                        'access_token':access_token,
                        'refresh_token':refresh_token
                    },
                    'message':'Login successful'
                }),HTTP_200_OK
                
            else:
                 return jsonify({
                    'Message':'Invalid email password'
                }), HTTP_401_UNAUTHORIZED
        
        else:
            return jsonify({
                'Message': 'Invalid email address'
            }), HTTP_401_UNAUTHORIZED
    
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
        
        
        
    # refreshing Token
        
@auth.route("token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = str(get_jwt_identity())  
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token':access_token})
    
    



