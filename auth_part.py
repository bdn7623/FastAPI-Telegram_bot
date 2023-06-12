from flask import Blueprint,render_template,request,redirect
from flask_login import LoginManager,login_user
from flask_login import UserMixin
from models import db
from wtforms_alchemy import ModelForm


auth_module = Blueprint('auth_module',
                        __name__,
                        template_folder='templates')

login_manager = LoginManager()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

class UserForm(ModelForm):
    class Meta:
        model = User

class UserManager:
    def __init__(self,user_class):
        self.user_class = user_class
        
    def get_user_by_credentials(self,username,password):
        user = self.user_class.query \
               .filter(self.user_class.username==username) \
               .filter(self.user_class.password==password).first()
        return user

user_manager = UserManager(User)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return "Вы должны войти для работы с сайтом"


"""
@app.route('/')
@login_required
def index():
    return f"Hello {current_user.username}"
"""

@auth_module.route('/login',methods=["GET","POST"])
def login():
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.form).data
        user = user_manager.get_user_by_credentials(form['username'],
                                                    form['password'])
        if user:
            login_user(user)
        return redirect('/admin')
    return render_template('login.html',form=form)


