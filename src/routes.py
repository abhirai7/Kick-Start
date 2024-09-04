from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from src import app, db
from src.models import Freelancer, Job, User

api = Blueprint("api", __name__)


def create_tables():
    with app.app_context():
        db.create_all()


create_tables()


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        username = current_user.username
        user = load_user(username)
        if user is None:
            error = "Username not found"
            return render_template("profile.html", error=error)
        user.username = request.form["username"]
        user.email = request.form["email"]
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("profile.html")


@app.route("/users", methods=["GET"])
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/freelancers", methods=["GET"])
def get_freelancers():
    freelancers = Freelancer.query.all()
    return jsonify(
        [
            {"id": f.id, "name": f.name, "email": f.email, "skills": f.skills}
            for f in freelancers
        ]
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = load_user(username)  # Call the load_user function we defined earlier
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html")


@api.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return render_template("index")


@api.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if load_user(username) is not None:
            error = "Username already exists"
            return render_template("register.html", error=error)
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        username = request.form["username"]
        user = load_user(username)
        if user is None:
            error = "Username not found"
            return render_template("reset_password.html", error=error)
        password = request.form["password"]
        user.set_password(password)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("reset_password.html")


# We can also add authentication to existing routes...
@api.route("/jobs", methods=["GET"])
@login_required
def get_jobs():
    jobs = Job.query.all()
    return jsonify([{"id": job.id, "title": job.title} for job in jobs])


@api.route("/freelancers", methods=["GET"])
@login_required
def get_freelancers():
    freelancers = Freelancer.query.all()
    return jsonify(
        [{"id": freelancer.id, "name": freelancer.name} for freelancer in freelancers]
    )


@api.route("/jobs", methods=["POST"])
@login_required
def create_job():
    title = request.json["title"]
    description = request.json["description"]
    job = Job(title=title, description=description, posted_by=current_user.id)
    db.session.add(job)
    db.session.commit()
    return jsonify({"message": "Job posted successfully"})


@api.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = Job.query.all()
    output = []
    for job in jobs:
        job_data = {}
        job_data["id"] = job.id
        job_data["title"] = job.title
        job_data["description"] = job.description
        job_data["posted_by"] = job.user.username
        output.append(job_data)
    return jsonify({"jobs": output})


@api.route("/jobs/<id>", methods=["GET"])
def get_job(id):
    job = Job.query.get_or_404(id)
    job_data = {}
    job_data["id"] = job.id
    job_data["title"] = job.title
    job_data["description"] = job.description
    job_data["posted_by"] = job.user.username
    return jsonify({"job": job_data})


@api.route("/jobs/<id>", methods=["PUT"])
@login_required
def update_job(id):
    job = Job.query.get_or_404(id)
    if job.posted_by != current_user.id:
        return jsonify({"message": "You are not authorized to update this job"}), 403
    title = request.json.get("title", job.title)
    description = request.json.get("description", job.description)
    job.title = title
    job.description = description
    db.session.commit()
    return jsonify({"message": "Job updated successfully"})


@api.route("/jobs/<id>", methods=["DELETE"])
@login_required
def delete_job(id):
    job = Job.query.get_or_404(id)
    if job.posted_by != current_user.id:
        return jsonify({"message": "You are not authorized to delete this job"}), 403
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted successfully"})


@app.route("/freelancers/create", methods=["GET", "POST"])
def create_freelancer():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        freelancer = Freelancer(name=name, email=email)
        db.session.add(freelancer)
        db.session.commit()
        return redirect(url_for("get_freelancers"))
    return render_template("create_freelancer.html")


@api.route("/freelancers", methods=["GET"])
def get_freelancers():
    freelancers = Freelancer.query.all()
    return render_template("freelancers.html", freelancers=freelancers)


@api.route("/freelancers/<id>", methods=["GET"])
def get_freelancer(id):
    freelancer = Freelancer.query.get_or_404(id)
    freelancer_data = {}
    freelancer_data["id"] = freelancer.id
    freelancer_data["name"] = freelancer.name
    freelancer_data["description"] = freelancer.description
    freelancer_data["user_id"] = freelancer.user_id
    return jsonify({"freelancer": freelancer_data})


@api.route("/freelancers/<id>", methods=["PUT"])
@login_required
def update_freelancer(id):
    freelancer = Freelancer.query.get_or_404(id)
    if freelancer.user_id != current_user.id:
        return (
            jsonify(
                {"message": "You are not authorized to update this freelancer profile"}
            ),
            403,
        )
    name = request.json.get("name", freelancer.name)
    description = request.json.get("description", freelancer.description)
    freelancer.name = name
    freelancer.description = description
    db.session.commit()
    return jsonify({"message": "Freelancer profile updated successfully"})


@api.route("/freelancers/<id>", methods=["DELETE"])
@login_required
def delete_freelancer(id):
    freelancer = Freelancer.query.get_or_404(id)
    if freelancer.user_id != current_user.id:
        return (
            jsonify(
                {"message": "You are not authorized to delete this freelancer profile"}
            ),
            403,
        )
    db.session.delete(freelancer)
    db.session.commit()
    return jsonify({"message": "Freelancer profile deleted successfully"})


@app.route("/posts", methods=["GET"])
def posts():
    posts = Post.query.filter_by(author=current_user).all()
    return render_template("posts.html", posts=posts)


@app.route("/posts/<int:post_id>", methods=["GET"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!")
        return redirect(url_for("posts"))
    return render_template("new_post.html")


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        flash("Your post has been updated!")
        return redirect(url_for("post", post_id=post_id))
    return render_template("edit_post.html", post=post)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!")
    return redirect(url_for("posts"))


@app.route("/users/<int:user_id>/posts")
def user_posts(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template("user_posts.html", user=user, posts=posts)
