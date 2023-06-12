from flask import Flask,render_template
from flask_admin import Admin
from dotenv import load_dotenv
import os
from models import db
from models import Lector,Group,Message
from auth_part import auth_module,login_manager
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_CONNECTION"]
app.config['FLASK_ADMIN_SWATCH'] = os.environ["ADMIN_THEME"]
app.secret_key = os.environ["SECRET_KEY"]

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(auth_module)
login_manager.init_app(app)

admin = Admin(app, name='АДМИН ЧАСТЬ САЙТА', template_mode='bootstrap3')

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin.add_view(AdminView(Lector, db.session))
admin.add_view(AdminView(Group, db.session))
admin.add_view(AdminView(Message, db.session))

app.run()
