from flask import Blueprint
from flask import request, session,redirect
from api.utils import responses as resp
from api.utils.responses import response_with
from api.utils.login_require import login_required
from flask_cors import CORS
from api.models.users import User, UserSchema

user_routes = Blueprint("user_routes", __name__)

#建立帳號(需登入才能建)
@user_routes.route('/create_user', methods=['POST'])
@login_required
def create_user():
    data = request.get_json()
    if User.find_by_username(data['username']) is not None:
        return response_with({ **resp.INVALID_INPUT_422,'code':'fail'},value={'msg':"User already exists"})
    data['password'] = User.generate_hash(data['password'])
    user_schmea = UserSchema()
    user = user_schmea.load(data)
    result = user_schmea.dump(user.create())
    return response_with(resp.SUCCESS_201)

#帳號登入
@user_routes.route('/login', methods=['POST'])
def authenticate_user():
    session.permanent = True
    data = request.get_json()
    current_user = None
    if data.get('email'):
        current_user = User.find_by_email(data['email'])
    elif data.get('username'):
        current_user = User.find_by_username(data['username'])
    if not current_user:
        return response_with({ **resp.UNAUTHORIZED_401,'code':'fail'}, value={'msg': 'This user does not exists'})
    # 資料表中使用者是被確認的才能往下執行
    if User.verify_hash(data['password'], current_user.password):
        session['username'] = current_user.username
        return response_with(resp.SUCCESS_200)
    else:
        return response_with({ **resp.UNAUTHORIZED_401,'code':'fail'}, value={'msg': 'Wrong password'})

#取得使用者資訊
@user_routes.route('/get_session', methods=['POST'])
@login_required
def get_session():
    if 'username' in session:
        data = {'username':session['username']}
    else:
        data = {'username':''}
    return response_with(resp.SUCCESS_200, value=data)

#帳號登出
@user_routes.route('/logout', methods=['POST'])
def logout():
    for key in list(session.keys()):
        session.pop(key)
    data = {"code":"success"}
    return response_with(resp.SUCCESS_200, value={"msg": "ok"})