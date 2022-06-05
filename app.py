from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_api import FlaskAPI, status
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os, jwt
from functools import wraps


POSTGRES = {
    "user": os.environ.get("USER"),
    "pw": os.environ.get("PASSWORD"),
    "db": os.environ.get("DATABASE"),
    "host": os.environ.get("HOST"),
    "port": os.environ.get("PORT")
}


db = SQLAlchemy()
migrate = Migrate()

# Define user model
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    gender = db.Column(db.String(10))
    email = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    address = db.Column(db.String())
    password_hash = db.Column(db.String(), nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.utcnow())
    last_modified_date = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return "<User ID: {}>".format(self.id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "email": self.email,
            "username": self.username,
            "address": self.address,
            "created_date": self.created_date
        }


def create_app():
    app = FlaskAPI(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SECRET_KEY"] = os.environ.get("SECERT_KEY")
    db.init_app(app)
    migrate.init_app(app, db)
    return app


app = create_app()

#Validate token user JWT
def token_required(f):
    @wraps(f)
    def validate_token(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        
        if not token:
            return jsonify(
                message="Không tìm thấy token",
                status=status.HTTP_401_UNAUTHORIZED
            )
  
        try:
            data = jwt.decode(token, app.config.get("SECRET_KEY"), algorithms="HS256")
            current_user = User.query\
                .filter_by(id=data["user_id"])\
                .first()
        except Exception as e:
            return jsonify(
                message="User chưa đăng nhập",
                status=status.HTTP_401_UNAUTHORIZED
            )
        return  f(current_user, *args, **kwargs)
  
    return validate_token


@app.route("/")
def home_page():
    return jsonify(
        message="Welcome to HomeTest",
        status=status.HTTP_200_OK
    )


@app.route("/user/sign_up", methods = ["POST"])
def sign_up():
    if request.method == "POST":
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        gender = request.data.get("gender")
        address = request.data.get("address")
        username = email.split("@")[0]
        password = request.data.get("password")

        if User.query.filter_by(email=email).first():
            return jsonify(
                message="Email đã tồn tại",
                status=status.HTTP_409_CONFLICT
            )

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            address=address,
            username=username
        )
        user.set_password(password)

        db.session.add(user)
        db.session.flush()
        db.session.commit()

        return jsonify(
            message="Thêm user thành công",
            status=status.HTTP_200_OK,
            data=user.to_json()
        )


@app.route("/user/<int:user_id>", methods = ["GET", "POST", "DELETE"])
@token_required
def get_user(current_user, user_id: int) -> jsonify:
    if request.method == "GET":
        user = User.query.get(user_id)
        if user:
            return jsonify(
                message="Lấy thông tin user thành công",
                status=status.HTTP_200_OK,
                data=user.to_json()
            )
        
        return jsonify(
            message="User không tồn tại",
            status=status.HTTP_401_UNAUTHORIZED
        )
    elif request.method == "POST":
        user = User.query.get(user_id)
        if user:
            user.first_name = request.data.get("first_name")
            user.last_name = request.data.get("last_name")
            user.gender = request.data.get("gender")
            user.address = request.data.get("address")
            user.last_modified_date = datetime.utcnow()
            db.session.flush()
            db.session.commit()

            return jsonify(
                message="Cập nhật user thành công",
                status=status.HTTP_200_OK,
                data=user.to_json()
            )
        
        return jsonify(
            message="User không tồn tại",
            status=status.HTTP_401_UNAUTHORIZED
        )
    elif request.method == "DELETE":
        user = User.query.filter_by(id=user_id)
        if user:
            user.delete()
            db.session.flush()
            db.session.commit()
            return jsonify(
                message="Xóa user thành công",
                status=status.HTTP_200_OK,
            )
        
        return jsonify(
            message="User không tồn tại",
            status=status.HTTP_401_UNAUTHORIZED
        )


@app.route("/user/get_all_user", methods = ["GET"])
@token_required
def get_all_user(current_user) -> jsonify:
    if request.method == "GET":
        users = User.query.all()
        
        return jsonify(
            message="Lấy danh sách user thành công",
            data=[user.to_json() for user in users]
        )


@app.route("/user/login", methods =["POST"])
def login():
    auth = request.data
  
    if not auth or not auth.get("email") or not auth.get("password"):
        return jsonify(
            message="Chưa nhập email hoặc password",
            status=status.HTTP_401_UNAUTHORIZED
        )
  
    user = User.query\
        .filter_by(email = auth.get("email"))\
        .first()
  
    if not user:
        return jsonify(
            message="User không tồn tại",
            status=status.HTTP_401_UNAUTHORIZED
        )
  
    if user.check_password(auth.get("password")):
        token = jwt.encode({
            "user_id": user.id,
            "exp" : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config["SECRET_KEY"])
  
        return jsonify(
            token=token,
            status=status.HTTP_201_CREATED
        )
    
    return jsonify(
        message="Password không chính xác",
        status=status.HTTP_403_FORBIDDEN
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)