from flask import Flask,render_template,session, redirect, url_for,flash,make_response,request
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy #导入flask_sqlalchemy数据库
import os
from flask_script import Shell#在运行shell的时候自动导入相关数控库实例配置
#*********以下用于表单**********************************************
#from flask_wtf import Form
from flask_wtf import Form
#import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import rundoc #导入自动生成的文章程序

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
#******以上用于表单模块*************************************************


app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
#初始化对Flask-Bootstrap 输出的 Bootstrap 类初始化，初始化类的目的就是为了给类分配内存空间
moment = Moment(app)

app.config['SECRET_KEY'] = 'hard to guess string'
#为了实现 CSRF 保护，Flask-WTF 需要程序设置一个密钥。Flask-WTF 使用这个密钥生成加密令牌

#************SQLAlchemy 数据库方面配置***********************************
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
#程序使用的数据库 URL 必须保存到 Flask 配置对象的 SQLALCHEMY_DATABASE_URI 键中
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# SQLALCHEMY_COMMIT_ON_TEARDOWN 键，将其设为 True 时，每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#解释https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
db = SQLAlchemy(app)
#db 对象是 SQLAlchemy 类的实例，表示程序使用的数据库，同时还获得了 Flask-SQLAlchemy提供的所有功能。
#************SQLAlchemy 数据库方面配置*************************************


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
#make_shell_context() 函数注册了程序、数据库实例以及模型，因此这些对象能直接导入 shell


#****************创建数据库表用到*******************************************

class Role(db.Model):

     __tablename__ = 'roles'#__tablename__定义数控库表名
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(64), unique=True)
     def __repr__(self):
#__repr()__ 方法，返回一个具有可读性的字符 串表示模型，可在调试和测试时使用
         return '<Role %r>' % self.name
     users = db.relationship('User', backref='role',lazy='dynamic')
#db.relationship() 的第一个参数表 明这个关系的另一端是哪个模型。如果模型类尚未定义，可使用字符串形式指定。
#db.relationship() 中的 backref 参数向 User 模型中添加一个 role 属性，从而定义反向关系。--不理解
#这一属性可替代 role_id 访问 Role 模型，此时获取的是模型对象，而不是外键的值--不理解
#这个例子中的 user_role.users 查询有个小问题。执行 user_role.users 表达式时，隐含的 查询会调用 all() 返回一个用户列表。query 对象是隐藏的，因此无法指定更精确的查询 过滤器。
#加入了 lazy = 'dynamic' 参数，从而禁止自动执行查询。

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    def __repr__(self):
        return '<User %r>' % self.username
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#****************创建数据库表用到*******************************************

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def indexPost():
    get_update = None
    if request.form['action'] == u'老阳说':
        article = rundoc.ngram_lm(f="yzp_blog.csv", ngram=4, N=200)

    return render_template('index.html',article = article)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/headpg')
def headpage():
    return render_template('headpg.html')

@app.route('/introduce')
def introduce():
    return render_template('introduce.html')

@app.route('/listblog')
def listblog():
    return render_template('listblog.html')

@app.route('/listwechat')
def listwechat():
    return render_template('listwechat.html')

@app.route('/listbook')
def listbook():
    return render_template('listbook.html')

if __name__ == "__main__":
    #manager.run() #manager.run()代替了app.run()，启动后就能解析命令行啦
    app.run(debug = True)
