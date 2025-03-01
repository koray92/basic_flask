from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_data(data):
    """ Load movie data from the JSON file """
    with open(data, "r") as file:
        return json.load(file)


def save_data(data):
    """ Save movie data to the JSON file """
    with open("blogs.json", "w") as file:
        json.dump(data, file, indent=4)


@app.route('/')
def index():
    blog_posts = load_data("blogs.json")
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = load_data("blogs.json")

        new_post = {
            "id": len(blog_posts) + 1,
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)
        save_data(blog_posts)

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=["GET"])
def delete(post_id):
    blog_posts = load_data("blogs.json")
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_data(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    blog_posts = load_data("blogs.json")
    post = next((p for p in blog_posts if p['id'] == post_id), None)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        save_data(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)