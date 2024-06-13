from flask import Flask, render_template,request,url_for,jsonify,make_response
from flask_mysqldb import MySQL
from flask_login import login_required, current_user
from flask import request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import click
import re
import ast 
from markupsafe import escape

def txtp():
    with open('1.txt','r',encoding='utf-8') as t:
        txtnew = t.read()
    # 使用ast.literal_eval()转换字符串为列表  
    list_from_literal_eval = ast.literal_eval(txtnew)  
    # print(list_from_literal_eval)  # 输出: ['第一行', '第二行', '第三行']
    # for i in list_from_literal_eval:
    #     print(i)
    return list_from_literal_eval

app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'username'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'database'
# mysql = MySQL(app)
log = False
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)
#用户数据表
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    usename = db.Column(db.String(20))
    view = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    works = db.Column(db.String)
    time = db.Column(db.String)
    # def __repr__(self):  
    #     return f'<User {self.username}>'
#用户账号表
class Userall(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    usename = db.Column(db.String(20))
    password = db.Column(db.String(30))
    mylike = db.Column(db.String)
login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = 'log'
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = Userall.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象
#表创建指令注册
@app.cli.command()
def create():
    db.drop_all()
    db.create_all()
    click.echo('Initialized database.')
#注册查询指令
@app.cli.command()
def query():
    use = User.query.all()
    useall = f"|ID     |usename     |view     |likes     |works     |time         |\n"
    for u in use:
        all = f"|{u.id}      |{u.usename}         |{u.view}       |{u.likes}       |{u.works}    |{u.time}     |"
        useall = useall + all + '\n'
    click.echo(useall)
#注册查询指令
@app.cli.command()
def get():
    click.echo(User.query.get(1))
#注册插入指令
@app.cli.command()
def createuser():
    new_user = User(usename='wen', view=1,likes=1,works='数据库',time='2024-6-4')
    # new_user = Userall(usename='root',password='12345')
    db.session.add(new_user)
    db.session.commit()
    click.echo("usename='wen', view=1,likes=1,works='数据库',time='2024-6-4'")
#注册查询指令
@app.cli.command()
def createusers():
    new_user = Userall(usename='root',password='12345')
    db.session.add(new_user)
    db.session.commit()
    click.echo("usename='root',password='12345'")
#注册删除指令
@app.cli.command()
def drop():
    num = int(input('删除对象:'))
    uses = User.query.get(num)
    db.session.delete(uses)
    db.session.commit()
#注册删除指令
@app.cli.command()
def drops():
    num = int(input('删除对象:'))
    uses = Userall.query.get(num)
    db.session.delete(uses)
    db.session.commit()
#注册查询指令
@app.cli.command()
def all():
    click.echo(User.query.all())
#注册查询指令
@app.cli.command()
def queryuuser():
    num = int(input('查询对象:'))
    use = User.query.get(num)
    cent = {'id':use.id,'usename':use.usename,'view':use.view,'likes':use.likes,'works':use.works,'time':use.time}
    click.echo(cent)
#注册查询指令
@app.cli.command()
def alls():
    click.echo(Userall.query.all())
@app.cli.command()
def queryuse():
    uses = User.query.all()
    for use in uses:
        cent = {'id':use.id,'usename':use.usename,'view':use.view,'likes':use.likes,'works':use.works,'time':use.time}
        click.echo(cent)
    return cent
@app.cli.command()
def queryuses():
    uses = Userall.query.all()
    for use in uses:
        cent = {'name':use.usename,'password':use.password,'mylike':use.mylike}
        click.echo(cent)
    return cent
@app.cli.command()
def queryname(): 
    target_name = "wxh"  
    target_index = None  
    users = Userall.query.all()
    for user in users:
        if target_name == user.usename:
            target_index = user.id
    if target_index is not None:  
        click.echo(f"用户 {target_name} 在列表中的位置是: {target_index}")
    else:  
        click.echo(f"未找到名为 {target_name} 的用户")
def usefrom(usename):
    target_name = usename
    target_index = None  
    users = Userall.query.all()
    for user in users:
        if target_name == user.usename:
            target_index = user.id
    return target_index
def uselikeif(usename):
    id = usefrom(usename)
    like = Userall.query.get(id).mylike
    return like
def queryusec():
    use = User.query.get(2)
    # cent = {'name':use.usename,'password':use.password}
    cent = {'id':use.id,'usename':use.usename,'view':use.view,'likes':use.likes,'works':use.works,'time':use.time}
    return cent
@app.route('/',methods=['GET', 'POST'])
# @login_required
def hello():
    likeif = None
    text = txtp()
    if not current_user.is_authenticated:  # 如果当前用户未认证
        return redirect(url_for('log'))  # 重定向到主页
    cent = queryusec()
    uselike = uselikeif(current_user.usename)
    #初始化点赞判断
    if uselike == cent['works']:
        init = '取消点赞'
    elif uselike != cent['works']:
        init = '为我点赞'
    username = request.cookies.get('lognum') 
    #判断用户点赞行为
    if request.method == 'POST':
        json_data = request.get_json()  # 从请求中获取JSON数据  
            # 你可以在这里处理接收到的数据，例如保存到数据库或进行其他操作
        likes = json_data['like']
        if uselike == cent['works']:
            new_user_like = User.query.get(2)
            new_user_like.likes = new_user_like.likes-1
            current = Userall.query.get(usefrom(current_user.usename))
            current.mylike = None
            db.session.commit()
            likeif = False
        elif uselike != cent['works']:
            # if likes == 'increase':
            new_user_like = User.query.get(2)
            new_user_like.likes = new_user_like.likes+1
            current = Userall.query.get(usefrom(current_user.usename))
            current.mylike = cent['works']
            db.session.commit()
            likeif = True
            # 返回一个响应给客户端
        return jsonify({'message':User.query.get(2).likes,'likeif':likeif})
    else:
        username = request.cookies.get('lognum')
        new_user = User.query.get(2)
        if username:
            username = int(username)+1
            new_user.view = new_user.view+1
            db.session.commit()
        else:
            username = '1'
    textid = cent['id']
    # with open(f'txt/{textid}.txt','r+',encoding='utf-8') as f:
    #     txt = f.read()
    home = ['简介','封面','前言','第 1 章：准备工作','第 2 章：Hello, Flask!','第 3 章：模板','第 4 章：静态文件','第 5 章：数据库','第 6 章：模板优化','第 7 章：表单','第 8 章：用户认证','第 9 章：测试','第 10 章：组织你的代码','第 11 章：部署上线',]
    hoem_name = 'Python Web!'
    teile = '第 2 章：Hello, Flask!'
    home_div = ['安装编辑器和浏览器','使用命令行','使用 Git,将程序托管到 GitHub（可选）','设置 SSH 密钥','创建远程仓库','创建虚拟环境'',激活虚拟环境','安装 Flask,本章小结','进阶提示']
    # text = txt.split('\n')
    onout=['#','#']
    resp = make_response(render_template('index.html',init=init,home=home,hoem_name=hoem_name,teile=teile,text=text,home_div=home_div,cent=cent,onout=onout))  # 或者只是返回一个字符串 'Hello, World!'  
    resp.set_cookie('lognum',str(username))
    new_user.view = new_user.view-1
    db.session.commit()
    return resp
@app.route('/<name>',methods=['GET', 'POST'])
def user_page(name):
    likeif = None
    text = txtp()
    if not current_user.is_authenticated:  # 如果当前用户未认证
        return redirect(url_for('log'))  # 重定向到主页
    cent = queryusec()
    uselike = uselikeif(current_user.usename)
    #初始化点赞判断
    if uselike == cent['works']:
        init = '取消点赞'
    elif uselike != cent['works']:
        init = '为我点赞'
    #判断用户点赞行为
    if request.method == 'POST':
        json_data = request.get_json()  # 从请求中获取JSON数据  
            # 你可以在这里处理接收到的数据，例如保存到数据库或进行其他操作
        likes = json_data['like']
        if uselike == cent['works']:
            new_user_like = User.query.get(2)
            new_user_like.likes = new_user_like.likes-1
            current = Userall.query.get(usefrom(current_user.usename))
            current.mylike = None
            db.session.commit()
            likeif = False
        elif uselike != cent['works']:
            # if likes == 'increase':
            new_user_like = User.query.get(2)
            new_user_like.likes = new_user_like.likes+1
            current = Userall.query.get(usefrom(current_user.usename))
            current.mylike = cent['works']
            db.session.commit()
            likeif = True
            # 返回一个响应给客户端
        return jsonify({'message':User.query.get(2).likes,'likeif':likeif})
    else:
        username = request.cookies.get('lognum')
        new_user = User.query.get(2)
        if username:
            username = int(username)+1
            new_user.view = new_user.view+1
            db.session.commit()
        else:
            username = '1'
    textid = cent['id']
    # with open(f'txt/{textid}.txt','r+',encoding='utf-8') as f:
    #     txt = f.read()
    home = ['简介','封面','前言','第 1 章：准备工作','第 2 章：Hello, Flask!','第 3 章：模板','第 4 章：静态文件','第 5 章：数据库','第 6 章：模板优化','第 7 章：表单','第 8 章：用户认证','第 9 章：测试','第 10 章：组织你的代码','第 11 章：部署上线',]
    teile = None
    onout=[]
    for homename in range(len(home)):
        if home[homename] == escape(name):
            teile = home[homename]
            if homename > 0:onout.append(home[homename-1])
            else:onout.append('#')
            if homename < len(home)-2:onout.append(home[homename+1])
            else:onout.append('#')
    if teile == None:
        return render_template('404.html')
    hoem_name = 'Python Web!'
    home_div = ['安装编辑器和浏览器','使用命令行','使用 Git,将程序托管到 GitHub（可选）','设置 SSH 密钥','创建远程仓库','创建虚拟环境'',激活虚拟环境','安装 Flask,本章小结','进阶提示']
    # text = txt.split('\n') 
    resp = make_response(render_template('index.html',init=init,home=home,hoem_name=hoem_name,teile=teile,text=text,home_div=home_div,cent=cent,onout=onout))  # 或者只是返回一个字符串 'Hello, World!'  
    resp.set_cookie('lognum',str(username))
    new_user.view = new_user.view-1
    db.session.commit()
    return resp
@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        users = Userall.query.all()
        username = request.form['username']
        password = request.form['password']
        action = request.form['action']
        flash(username)
        flash(password)
        if not username or not password:
                flash('请输入你的用户名与密码!')
                return redirect(url_for('log'))
        if action == 'login':
            for user in users:
                if username == user.usename and password == user.password:
                    login_user(user)
                    return redirect(url_for('hello'))
                elif username == user.usename and password != user.password:
                    flash('密码错误!')
                    return redirect(url_for('log'))
            flash(f'{username}用户未注册')
            return redirect(url_for('log'))
        elif action == 'create':
            for user in users:
                if username == user.usename:
                    flash(f'{username}用户已经注册过了,选择其他用户名,若忘记密码可找回,')
                    return redirect(url_for('log'))
            new_user = Userall(usename=username,password=password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'{username}用户已注册成功,请重新登录')
            return redirect(url_for('log'))
    else:
        username = ''
        password = ''
    return render_template('log.html')
@app.route('/logout')
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('log'))  # 重定向回首页
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/c', methods=['GET','POST'])  
def receive_json_data():
    if request.method == 'POST':
        json_data = request.get_json()  # 从请求中获取JSON数据  
        name = json_data['name']
        age = json_data['age']  
        city = json_data['city']  
        # 你可以在这里处理接收到的数据，例如保存到数据库或进行其他操作  
        # 返回一个响应给客户端  
        return jsonify({'message': 'Data received successfully!'})
    return render_template('create.html')
if __name__ == '__main__':  
    app.run(debug=True, host='0.0.0.0', port=5000)
