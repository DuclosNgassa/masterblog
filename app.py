from typing import Literal

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug import Response

import service

app = Flask(__name__)

# Set a secret key for session signing
app.secret_key = "super-secret-key-change-in-production"

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


@app.route('/update/<post_id>', methods=['GET','POST'])
def update(post_id):
    global blog_posts
    print("Heloo")
    if request.method == 'POST':
        # Update the post in the JSON file
        # Redirect back to index

        return do_update(blog_posts, post_id)
    else:
        post = service.fetch_post_by_id(post_id, blog_posts)
        if post is None:
            # Post not found
            print("Post not found")
            return "Post not found", 404
        else:
            # Else, it's a GET request
            # So display the update.html page
            return render_template('update.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    global blog_posts  # Declare global to reassign the list

    new_blog_posts = [p for p in blog_posts if p.get('id') != post_id]

    if len(new_blog_posts) == len(blog_posts):
        flash("Post doesn't exist", "error")
        return redirect(url_for("index"))

    # 1. Update in-memory global list
    blog_posts = new_blog_posts

    # 2. Persist changes to JSON file
    service.write_json('db/posts.json', blog_posts)

    flash("Post deleted successfully!", "success")
    return redirect(url_for("index"))


def do_update(posts: list[dict], post_id) -> tuple[Literal["Post not found"], Literal[404]] | Response:
    title = request.form.get('title')
    content = request.form.get('content')
    author = request.form.get('author')
    post_found = False
    for index_post, _ in enumerate(posts):
        if str(posts[index_post]['id']) == str(post_id):
            posts[index_post]['title'] = title
            posts[index_post]['content'] = content
            posts[index_post]['author'] = author
            post_found = True
        break
    if not post_found:
        return "Post not found", 404
    else:
        # Update the db
        service.write_json('db/posts.json', posts)
        flash("Post updated successfully", "success")
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
