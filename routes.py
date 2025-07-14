from flask import render_template, redirect, url_for, flash, session
from forms import RegisterForm, LoginForm, PostForm, CommentForm, ProfileForm
from ext import app, db
from models import User, Post, Comment
from flask_login import login_user, logout_user, current_user, login_required
import os


def get_liked_posts():
    return session.get('liked_posts', [])

@app.route("/")
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    liked_posts = len(get_liked_posts())
    return render_template("index.html", posts=posts, liked_posts=liked_posts)

@app.route("/liked")
def liked():
    liked_post_ids = get_liked_posts()
    if liked_post_ids:
        posts = Post.query.filter(Post.id.in_(liked_post_ids)).all()
    else:
        posts = []
    return render_template('liked.html', posts=posts, liked_posts=len(liked_post_ids))

@app.route('/add_to_liked/<int:post_id>', methods=['POST'])
def add_to_liked(post_id):
    liked = session.get('liked_posts', [])
    if post_id not in liked:
        liked.append(post_id)
    session['liked_posts'] = liked
    return redirect("/")

@app.route('/remove_from_liked/<int:post_id>')
def remove_from_liked(post_id):
    liked = session.get('liked_posts', [])
    if post_id in liked:
        liked.remove(post_id)
        session['liked_posts'] = liked
    return redirect("/liked")

@app.route("/detailed/<int:post_id>", methods=["GET", "POST"])
def detailed(post_id):
    detailed_post = Post.query.get(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return redirect("/login")
        new_comment = Comment(content=form.content.data, post=detailed_post, user=current_user)

        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('detailed', post_id=post_id))
    comments = Comment.query.filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).all()
    liked = session.get('liked', [])
    liked_posts = len(liked)

    return render_template("detailed.html", post=detailed_post, form=form, comments=comments, liked_posts=liked_posts)

@app.route("/delete_comment/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully.", "success")
    return redirect(url_for("detailed", post_id=comment.post_id))

@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    form = PostForm(title=post.title, description=post.description, content=post.content, category=post.category,
                    location=post.location)
    form.submit.label.text = "Edit"
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.content = form.content.data
        post.category = form.category.data
        post.location = form.location.data

        if form.img.data:
            image = form.img.data
            directory = os.path.join("static", "images", image.filename)
            image.save(directory)
            post.img = image.filename

        db.session.commit()
        flash("Post updated successfully.", "success")
        return redirect("/")

    return render_template("posts.html", form=form)

@app.route("/delete_post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    Comment.query.filter_by(post_id=post.id).delete()

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully.", "success")
    return redirect("/")

@app.route("/posts", methods=["GET", "POST"])
@login_required
def posts():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, description=form.description.data, content=form.content.data,
                        category=form.category.data, location=form.location.data, user_id=current_user.id)
        image = form.img.data
        directory = os.path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        new_post.img = image.filename

        db.session.add(new_post)
        db.session.commit()
        flash("Post published successfully.", "success")
        return redirect("/")

    return render_template("posts.html", form=form, posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_username = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_username:
            flash("Username is already in use.", "danger")
            return redirect("/register")
        if existing_email:
            flash("Email is already in use.", "danger")
            return redirect("/register")
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        image = form.profile_image.data
        if image:
            filename = image.filename
            directory = os.path.join(app.root_path, "static", "images", filename)
            image.save(directory)
            user.img = filename
        else:
            user.img = "default.png"

        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can now log in.", "success")
        return redirect("/login")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash("Username does not exist.", "danger")
        elif not user.check_password(form.password.data):
            flash("Incorrect password.", "danger")
            return redirect("/")
        else:
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect("/")

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.profile_image.data:
            image = form.profile_image.data
            filename = image.filename
            directory = os.path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            current_user.img = filename

        db.session.commit()
        return redirect("/profile")

    form.username.data = current_user.username
    form.email.data = current_user.email

    return render_template("profile.html", form=form)

@app.route('/delete_account', methods=["POST"])
@login_required
def delete_account():
    Post.query.filter_by(user_id=current_user.id).delete()
    Comment.query.filter_by(user_id=current_user.id).delete()
    user = User.query.get(current_user.id)

    db.session.delete(user)
    db.session.commit()
    logout_user()

    flash("Your account and all your data have been deleted.", "success")
    return redirect("/")

@app.route("/admin/users")
@login_required
def admin_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)

@app.route("/user/<int:user_id>")
@login_required
def view_user(user_id):
    user = User.query.get(user_id)
    return render_template("user_profile.html", user=user)

@app.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    Post.query.filter_by(user_id=user.id).delete()
    Comment.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()
    flash("User and all their posts and comments deleted.", "success")
    return redirect(url_for('admin_users'))
