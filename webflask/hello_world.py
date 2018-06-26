# coding=utf-8
from flask import Flask
# 引入Flask类，Flask类实现了一个WSGI应用。

# app是Flask的实例，它接收包或者模块的名字作为参数，但一般都是传递__name__。
# 让flask.helpers.get_root_path函数通过传入这个名字确定程序的根目录。
# 以便获得静态文件和模板文件的目录。
app = Flask(__name__)


# 配置管理
# 复杂的项目需要配置各种环境。如果设置项很少，可以直接硬编码进来，如下。
app.config['DEBUG'] = True
# app.config 是flask.config.Config类的实例，继承自Python内置数据结构的dict,所以可以使用update方法：
app.config.update(
    DEBUG=True,
    SECRET_KEY='123456'
)
# app.config内置的全部配置变量可以参看Builtin Configuration Values(http://bit.ly/28UUgW3)(翻墙？)
# 如果设置选项很多，想要集中管理设置项，应该将他们存放到一个文件里面。如已存在：settings.py配置文件。
# 方式一：通过配置文件加载。app.config.from_object('settings') # 通过字符串的模块名字
#         或者引用之后直接传入模块对象   import settings    app.config.from_object(settings)
# 方式二：通过文件名字加载。直接传入文件名字，但是不限于只使用.py后缀的文件名。
#         app.config.from_pyfile('settings.py',silent=True) #默认当配置文件不存在时会抛出异常，使用silent=True的时候只是返回False，但不会抛出异常。a
# 方式三：通过环境变量加载。这种方式依然支持silent参数，获得路径后其实哈哈死使用from_pyfile的方式加载。
#         > export YOURAPPLICATION_SETTINGS='settings.py' 
#         app.config.from_envvar('YOURAPPLICATION_SETTINGS') 


# 调试模式
# 虽然app.run这样的方式适用于启动本地的开发服务器，但是每次修改代码后都要手动重启的话，既不方便也不够优雅。如果启用了调试模式，服务器会在代码修改后
# 自动重新载入，并在发生错误时提供一个能获得错误上下文及可执行代码的调试页面。启用方式：
# 方式一： 直接在应用对象上设置  app.debug = True   app.run()
# 方式二： 作为run的参数传入     app.run(debug=True) 
# 需要注意，开启调试模式会成为一个巨大的安全隐患，因此它绝对不能用于生产环境中。
# Werkzeug 从0.11版本开始默认启用了PIN(Personal Identification Number)码的身份验证，旨在调试环境下的攻击者更难利用调试器。
# 当程序有异常而进入错误堆栈模式，第一次点击某个堆栈想要查看对应变量值的时候，浏览器会弹出一个要求你输入这个PIN值的输入框。
# Werkzeug会把这个PIN作为cookie的一部分存起来（失效时间默认8小时），失效之前不需要重复输入。
# 当然，也可以使用指定PIN码的值：
# export WERKZEUG_DEBUG_PIN=123


# app.route装饰器会将URL和执行的视图函数的关系保存到app.url_map属性上。
# 处理URL和视图函数的关系的程序就是路由，这里的视图函数就是hello_world。
@app.route('/')
def hello_world():
    return "Hello World!"


# 默认监听5000，启动后会调用werkzeug.serving.run_simple进入轮询，默认使用单进程单线程的werkzeug.serving.BaseWSGIServer处理请求，
# 实际上还是使用的标准库BaseHTTPServer.HTTPServer，通过select.select做0.5秒的‘while True’的事件轮询。
# app.run 只适合调试，生产环境应该使用 Gunicorn或者uWSGI.
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)
