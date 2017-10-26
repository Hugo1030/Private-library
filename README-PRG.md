#### 如何运行程序：
直接运行python app.py即可
#### 文件说明：
static 文件夹flask 静态的文件和bootstrap的CSS和JS的样式包
templates 文件夹 flask的静态页面
whoosh_index文件夹 flask-whooshalchemyplus框架的索引库
app.py 运行的主程序
run.py 和rundoc.py 实现Ai写歌功能（txt文件的都是写歌用的语料）
importfile.py 导入数据库的脚本，单独使用（使用csv文件）。

#### 异常情况
##### 无法检索到数控已有的数据
以下情况可能没有和数据库建立索引，特征就是数据库有数据，但就是检索不到  
情况1、可能直接给数据库插入数据，没有经过创建索引的形式  
解决方式：1、删除数控的内容，重新创建索引
手动删除数据库的内容
```javascript
>>> from app import * #app运行文件
>>> for post in BlogingPost.query.all():
...     db.session.delete(post)
...
>>> db.session.commit()
```
情况2、之前创建索引了，但是索引库迁移了（包括变更索引库和索引库的位置发生变化）  
解决方式：1、找到新的索引库的位置。实在不清楚索引库位置，自己再创建一个。
创建的方式就是：
```javascript
>>> from app import * #app运行文件
>>> db.create_all()
```
3、出现stop词的情况，这应该是analyze的选择问题（猜想）
解决方式：变更app 里面“__analyzer__ = ”的值

#### 其他操作说明
手动添加到数据库的语法：
```javascript
>>> from app import *
>>> sqltest=BlogingPost(title ='live is good',content='Lives are better,so I want to enjoy lives')
>>> db.session.add(sqltest)
>>> db.session.commit()
```
