from flask import Flask, render_template

import service

app = Flask(__name__)

blog_posts = service.read_json('db/posts.json')

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
