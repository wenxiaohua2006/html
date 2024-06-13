txt = [[{'h1':'第 5 章：数据库¶'},'''大部分程序都需要保存数据，所以不可避免要使用数据库。用来操作数据库的数据库管理系统（DBMS）有很多选择，对于不同类型的程序，不同的使用场景，都会有不同的选择。在这个教程中，我们选择了属于关系型数据库管理系统（RDBMS）的 SQLite，它基于文件，不需要单独启动数据库服务器，适合在开发时使用，或是在数据库操作简单、访问量低的程序中使用。
使用 SQLAlchemy 操作数据库¶
为了简化数据库操作，我们将使用 SQLAlchemy——一个 Python 数据库工具（ORM，即对象关系映射）。借助 SQLAlchemy，你可以通过定义 Python 类来表示数据库里的一张表（类属性表示表中的字段 / 列），通过对这个类进行各种操作来代替写 SQL 语句。这个类我们称之为模型类，类中的属性我们将称之为字段。
Flask 有大量的第三方扩展，这些扩展可以简化和第三方库的集成工作。我们下面将使用一个叫做 Flask-SQLAlchemy 的扩展来集成 SQLAlchemy。
首先安装它：
(env) $ pip install flask-sqlalchemy==2.5.1 sqlalchemy==1.4.47
 Flask-SQLAlchemy 3.x / SQLAlchemy 2.x 版本有一些大的变化，这里分别固定安装 2.5.1 和 1.4.47 版本。后续教程改写后会删除这里的版本限制。

大部分扩展都需要执行一个“初始化”操作。你需要导入扩展类，实例化并传入 Flask 程序实例：'''],[{'h1':'使用 SQLAlchemy 操作数据库¶'},'''为了简化数据库操作，我们将使用 SQLAlchemy——一个 Python 数据库工具（ORM，即对象关系映射）。借助 SQLAlchemy，你可以通过定义 Python 类来表示数据库里的一张表（类属性表示表中的字段 / 列），通过对这个类进行各种操作来代替写 SQL 语句。这个类我们称之为模型类，类中的属性我们将称之为字段。'''],[{'p':'''Flask 有大量的第三方扩展，这些扩展可以简化和第三方库的集成工作。我们下面将使用一个叫做 Flask-SQLAlchemy 的扩展来集成 SQLAlchemy。

首先安装它：'''}],[{'shell':'''(env) $ pip install flask-sqlalchemy==2.5.1 sqlalchemy==1.4.47'''}],[{'samp':''' Flask-SQLAlchemy 3.x / SQLAlchemy 2.x 版本有一些大的变化，这里分别固定安装 2.5.1 和 1.4.47 版本。后续教程改写后会删除这里的版本限制。'''}],[{'p':'''大部分扩展都需要执行一个“初始化”操作。你需要导入扩展类，实例化并传入 Flask 程序实例：'''}],
[{'py':'''from flask_sqlalchemy import SQLAlchemy  # 导入扩展类

app = Flask(__name__)

db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app'''}],[{'h1':'设置数据库 URI¶'},'''为了设置 Flask、扩展或是我们程序本身的一些行为，我们需要设置和定义一些配置变量。Flask 提供了一个统一的接口来写入和获取这些配置变量：Flask.config 字典。配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前。

下面写入了一个 SQLALCHEMY_DATABASE_URI 变量来告诉 SQLAlchemy 数据库连接地址：'''],
[{'py':'''import os

# ...

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')'''}],[{'samp':' 这个配置变量的最后一个单词是 URI，而不是 URL。'}],[{'p':'对于这个变量值，不同的 DBMS 有不同的格式，对于 SQLite 来说，这个值的格式如下：'}],[{'shell':'sqlite:////数据库文件的绝对地址'}],
[{'sheel':'''数据库文件一般放到项目根目录即可，app.root_path 返回程序实例所在模块的路径（目前来说，即项目根目录），我们使用它来构建文件路径。数据库文件的名称和后缀你可以自由定义，一般会使用 .db、.sqlite 和 .sqlite3 作为后缀。

另外，如果你使用 Windows 系统，上面的 URI 前缀部分只需要写入三个斜线（即 sqlite:///）。在本书的示例程序代码里，做了一些兼容性处理，另外还新设置了一个配置变量，实际的代码如下：

app.py：数据库配置'''}],[{'py':'''import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)'''}],[{'p':'如果你固定在某一个操作系统上进行开发，部署时也使用相同的操作系统，那么可以不用这么做，直接根据你的需要写出前缀即可。'}],
[{'samp':' 你可以访问 Flask 文档的配置页面查看 Flask 内置的配置变量；同样的，在 Flask-SQLAlchemy 文档的配置页面可以看到 Flask-SQLAlchemy 提供的配置变量。'}],
[{'h1':'创建数据库模型¶'}],[{'p':'''在 Watchlist 程序里，目前我们有两类数据要保存：用户信息和电影条目信息。下面分别创建了两个模型类来表示这两张表：
app.py：创建数据库模型'''}],[{'py':'''class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份'''}],[{'ul':'模型类的编写有一些限制：'},[['模型类要声明继承 db.Model。'],['每一个类属性（字段）要实例化 db.Column，传入的参数为字段的类型，下面的表格列出了常用的字段类。'],['在 db.Column() 中添加额外的选项（参数）可以对字段进行设置。比如，primary_key 设置当前字段是否为主键。除此之外，常用的选项还有 nullable（布尔值，是否允许为空值）、index（布尔值，是否设置索引）、unique（布尔值，是否允许重复值）、default（设置默认值）等。']]],
[{'p':'常用的字段类型如下表所示：'}],[{'table':['字段类','说明']},[['db.Integer','整型'],['db.String (size)','字符串，size 为最大长度，比如 db.String(20)'],['db.Text','长文本'],['db.DateTime','时间日期，Python datetime 对象'],['db.Float','浮点数'],['db.Boolean','布尔值']]],
[{'h1':'创建数据库表¶'},'''模型类创建后，还不能对数据库进行操作，因为我们还没有创建表和数据库文件。下面在 Python Shell 中创建了它们：'''],[{'shell':'''(env) $ flask shell
>>> from app import db
>>> db.create_all()'''}],[{'p':'打开文件管理器，你会发现项目根目录下出现了新创建的数据库文件 data.db。这个文件不需要提交到 Git 仓库，我们在 .gitignore 文件最后添加一行新规则：'}],[{'shell':'*.db'}],[{'p':'如果你改动了模型类，想重新生成表模式，那么需要先使用 db.drop_all() 删除表，然后重新创建：'}],[{'shell':'''>>> db.drop_all()
>>> db.create_all()'''}],[{'p':'注意这会一并删除所有数据，如果你想在不破坏数据库内的数据的前提下变更表的结构，需要使用数据库迁移工具，比如集成了 Alembic 的 Flask-Migrate 扩展。'}],[{'samp':''' 上面打开 Python Shell 使用的是 flask shell命令，而不是 python。使用这个命令启动的 Python Shell 激活了“程序上下文”，它包含一些特殊变量，这对于某些操作是必须的（比如上面的 db.create_all()调用）。请记住，后续的 Python Shell 都会使用这个命令打开。'''}],
[{'p':'''和 flask shell类似，我们可以编写一个自定义命令来自动执行创建数据库表操作：
  
app.py：自定义命令 initdb'''}],[{'py':'''import click


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息'''}],[{'p':'默认情况下，如果没有指定，函数名称就是命令的名字（注意函数名中的下划线会被转换为连接线），现在执行 flask initdb 命令就可以创建数据库表：'}]]

filetxt = []
for a in txt:
    key = len(a)
    if key == 1:
        txts = a[0]
        for name,cent in txts.items():
            filetxt.append([[f'<{name}>'],cent])
    elif key == 2 and type(a[1]) != list:
        txtc = a[0]
        for namec,centc in txtc.items():
            filetxt.append([[f'<{namec}>'],centc])
        filetxt.append([[f'<p>'],a[1]])
    elif type(a[1]) == list:
        txtc = a[0]
        for namec,centc in txtc.items():
            filetxt.append([[f'<{namec}>'],centc,[a[1]]])
print(filetxt)
with open('1.txt','w',encoding='utf-8') as f:
    f.write(str(filetxt))

with open('1.txt','r',encoding='utf-8') as t:
    txtnew = t.read()
import ast  
# 使用ast.literal_eval()转换字符串为列表  
list_from_literal_eval = ast.literal_eval(txtnew)  
# print(list_from_literal_eval)  # 输出: ['第一行', '第二行', '第三行']
for i in list_from_literal_eval:
    print(i)
d = [['<table>'], ['字段类', '说明'], [['<txtcent>'], [['db.Integer', '整型'], ['db.String (size)', '字符串，size 为最大长度，比如 db.String(20)'], ['db.Text', '长文本'], ['db.DateTime', '时间日期，Python datetime 对象'], ['db.Float', '浮点数'], ['db.Boolean', '布尔值']]]]