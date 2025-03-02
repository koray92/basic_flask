from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

def load_data(data):
    """ Load movie data from the JSON file """
    with open(data, "r") as file:
        return json.load(file)


def save_data(data):
    """ Save movie data to the JSON file """
    with open("blogs.json", "w") as file:
        json.dump(data, file, indent=4)


def generate_unique_id(blog_posts):
    """ Generate a unique ID for new blog posts """
    if not blog_posts:
        return 1  # If there are no posts, start from ID 1
    else:
        max_id = max(post['id'] for post in blog_posts)
        return max_id + 1


def validate_post_data(author, title, content):
    """ Validate the data for the blog post """
    if not author or author.strip() == "":
        return "Author cannot be empty or whitespace."
    if not title or title.strip() == "":
        return "Title cannot be empty or whitespace."
    if not content or content.strip() == "":
        return "Content cannot be empty or whitespace."
    return None


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

        # Validate input data
        validation_error = validate_post_data(author, title, content)
        if validation_error:
            flash(validation_error, 'error')
            return redirect(url_for('add'))

        blog_posts = load_data("blogs.json")

        new_post = {
            "id": generate_unique_id(blog_posts),  # Generate a unique ID
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
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Validate input data
        validation_error = validate_post_data(author, title, content)
        if validation_error:
            flash(validation_error, 'error')
            return redirect(url_for('update', post_id=post_id))  # Redirect back to the update page

        post['author'] = author
        post['title'] = title
        post['content'] = content

        save_data(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
