from email.policy import default
from typing import Any

from flask import Flask, render_template, request, redirect, url_for

import service

app = Flask(__name__)

blog_posts:list[dict] = service.read_json('db/posts.json')

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET','POST'])
def add():
    if request.method=='POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        post_id = max((post.get("id", 0) for post in blog_posts), default=0) + 1
        blog_posts.append({'id': post_id,'title':title,'content':content,'author':author})

        service.write_json('db/posts.json', blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
