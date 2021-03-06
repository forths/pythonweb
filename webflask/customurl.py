# -*- coding:utf-8 -*-
import urllib
from flask import Flask
from werkzeug.routing import BaseConverter

# 自定义URL转换器
# 自定义转换器需要继承BaseConverter，要设置to_python和to_url两个方法。
# to_python:把路径转换成一个Python对象
# to_url:把参数转换成为符合URL的形式。

app = Flask(__name__)

class ListConverter(BaseConverter):

    def __init__(self,url_map,separator='+'):
        super(ListConverter,self).__init__(url_map)
        self.separator = urllib.parse.unquote(separator)

    def to_python(self,value):
        return value.split(self.separator)

    def to_url(self,values):
        return self.separator.join(BaseConverter.to_url(value) for value in values)

app.url_map.converters['list'] = ListConverter


@app.route('/list1/<list:page_names>/')
def list1(page_names):
    return "Separator: {} {}".format('+',page_names)

@app.route('/list2/<list(separator=u"|"):page_names>/')
def list2(page_names):
    return "Sepatator: {} {}".format('|',page_names)

if __name__ == "__main__":
    app.run(debug=True)