import functools
from flask import session, jsonify, request
def login_required(func):
    @functools.wraps(func)  # 設置函數的元信息
    def inner(*args, **kwargs):
        user = session.get('username')
        if user:
            return func(*args, **kwargs)
        else:
            if request.environ.get('HTTP_ORIGIN') == 'http://localhost:4200' and ("118.163.69.181" in request.environ.get('HTTP_X_FORWARDED_FOR','') or "118.163.69.181" in request.environ.get('HTTP_X_REAL_IP','')):
                return func(*args, **kwargs)
            return jsonify(msg='Please login',code="fail"), 401
    return inner