from flask import request, redirect, url_for, current_app
from functools import wraps
import jwt

def verificar_cookie():
    token = request.cookies.get("access_token")
    current_user = None

    if token:
        try:
            current_user = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
            print("Token decodificado:", current_user)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            current_user = None
            print("Token inválido ou expirado")

    return current_user

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return redirect(url_for('login.login'))

        try:
            payload = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
            # Passa o payload (informações do usuário) como argumento extra
            return f(*args, **kwargs, current_user=payload)
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login.login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('login.login'))

    return decorated