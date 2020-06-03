from flask import Flask,request,render_template
import pandas as pd
from flask_paginate import Pagination, get_page_args
from process import Process

app = Flask(__name__)

@app.route('/')
def home() :
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    proc = Process()
    arrays = proc.get_data()
    total = len(arrays)
    pagination_users = arrays[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('index.html',users=pagination_users,page=page,per_page=per_page,pagination=pagination)


@app.route('/show/<id>')
def route(id) :
    print(id)
    page, per_page, offset = get_page_args(page_parameter='page',
                                            per_page_parameter='per_page')
    proc = Process()
    g = proc.get_encoded()
    recommend = proc.calculate(id)
    if recommend :
        total = len(recommend)
        pagination_users = recommend[offset: offset + per_page]
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                    css_framework='bootstrap4')
        return render_template('show.html',users=pagination_users,page=page,per_page=per_page,pagination=pagination)
    else :
        return "<h1>No Recommendation available </h1>"


if __name__ == '__main__' :
    app.run()