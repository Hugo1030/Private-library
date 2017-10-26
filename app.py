from flask import Flask,render_template,session, redirect, url_for,flash,make_response,request
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy #导入flask_sqlalchemy数据库
import os
from flask_script import Shell#在运行shell的时候自动导入相关数控库实例配置
#*********以下用于表单**********************************************
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import rundoc #导入自动生成的文章程序
import run

import flask_whooshalchemy
from whoosh.fields import *
from whoosh.qparser import QueryParser
from jieba.analyse.analyzer import ChineseAnalyzer
import datetime

import tempfile
import shutil
import flask_whooshalchemyplus #as waa#about  flask_whooshalchemyplus
from flask_whooshalchemyplus import index_all

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
#初始化对Flask-Bootstrap 输出的 Bootstrap 类初始化，初始化类的目的就是为了给类分配内存空间
moment = Moment(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://Woody:123456@localhost/test1'
#程序使用的数据库 URL 必须保存到 Flask 配置对象的 SQLALCHEMY_DATABASE_URI 键中
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#app.config['WHOOSH_DISABLED'] = True #dabout  flask_whooshalchemyplus,disable whoosh indexing .
app.config['WHOOSH_BASE'] = 'whoosh_index'#一定要找到新索引的位置

db = SQLAlchemy(app)
index_all(app)

class BlogingPost(db.Model):
    __tablename__ = 'blogingpost2'
    __searchable__ = ['title', 'content']  # these fields will be indexed by whoosh
    #__analyzer__ = SimpleAnalyzer()        # configure analyzer; defaults to
    __analyzer__ = ChineseAnalyzer()                                  # StemmingAnalyzer if not specified

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))  # Indexed fields are either String,
    content = db.Column(db.String(15000))   # Unicode, or Text
    datime = db.Column(db.String(20))
    url = db.Column(db.String(100))

#flask_whooshalchemyplus.init_app(app)    # initialize
flask_whooshalchemyplus.init_app(app)
flask_whooshalchemyplus.whoosh_index(app,BlogingPost)#about  flask_whooshalchemyplus




@app.route('/',methods=['GET'])
def index():
    posts = BlogingPost.query.all()
    return render_template('index.html')

@app.route('/',methods=['POST'])
def indexPost():
    get_update = None
    if request.form['action'] == u'AI写歌':
        para = rundoc.ngram_lm('test2.txt',5,80)
        lines = para.split(",")
    return render_template('index.html',lines = lines)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/headpg')
def headpage():
    return render_template('headpg.html')

@app.route('/introduce')
def introduce():

    posts = BlogingPost.query.whoosh_search(request.args.get('query')).all()
    return render_template('introduce.html',posts=posts)

@app.route('/listblog')
def listblog():
    return render_template('listblog.html')

@app.route('/listwechat')
def listwechat():
    return render_template('listwechat.html')

@app.route('/listbook')
def listbook():
    return render_template('listbook.html')

@app.route('/search')
def search():
    posts =BlogingPost.query.whoosh_search(request.args.get('query')).all()

    return render_template('searchhello.html',posts=posts)

@app.route('/testa',methods=['GET','POST'])
def testa():
    posts = BlogingPost.query.filter_by(id = request.args.get('id')).all()
    ##获取从列表页（searchhello）传过来的id参数，通过id检索到对应的数据库对应的某一行。
    poststext =BlogingPost.query.whoosh_search(request.args.get('query')).all()
    return render_template('testa.html',posts=posts,poststext=poststext)#,poststext=poststext)


@app.route('/add',methods=['GET','POST'])
def add():
    if request.method =="POST":
        post = BlogingPost(title=request.form['title'],content=request.form['content'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

app.config['WHOOSH_DISABLED'] = True
if __name__ == "__main__":
    #manager.run() #manager.run()代替了app.run()，启动后就能解析命令行啦，可以继续
    app.run(debug = True)
