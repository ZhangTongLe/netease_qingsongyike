from flask import Flask, render_template
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://test:hello@192.168.111.163/data"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Qingsongyike(db.Model):
    __tablename__ = 'qingsongyike'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(32))
    docid = db.Column(db.String(32), unique=True)
    ptime = db.Column(db.String(32))
    cover_img = db.Column(db.String(512))
    url_3g = db.Column(db.String(512))
    body = db.Column(db.Text)

def make_shell_context():
    return dict(app=app, db=db, Qingsongyike=Qingsongyike)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qsyk')
def qsyk():
    qingsongyike=Qingsongyike.query[-1]
    title=qingsongyike.title
    body=qingsongyike.body
    return render_template('qsyk.html',title=title, body=body)


if __name__ == '__main__':
    manager.run()