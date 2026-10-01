from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import (
    current_user,
    login_required
)
from sqlalchemy import or_

from app import db
from app.models import Comment, Post
from app.posts import bp
from app.posts.forms import (
    DeletePostForm,
    PostForm
)
from app.comments.forms import CommentForm


@bp.route("/")
def list_posts():
    search = request.args.get(
        "search",
        ""
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    query = Post.query.filter_by(
        published=True
    )

    if search:
        query = query.filter(
            or_(
                Post.title.ilike(
                    f"%{search}%"
                ),
                Post.content.ilike(
                    f"%{search}%"
                )
            )
        )

    posts = (
        query
        .order_by(
            Post.timestamp.desc()
        )
        .paginate(
            page=page,
            per_page=6,
            error_out=False
        )
    )

    return render_template(
        "posts/list.html",
        title="All Posts",
        posts=posts,
        search=search
    )


@bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():

        post = Post(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            published=form.published.data,
            author=current_user
        )

        db.session.add(post)
        db.session.commit()

        flash(
            "Post published successfully.",
            "success"
        )

        return redirect(
            url_for(
                "posts.detail",
                post_id=post.id
            )
        )

    return render_template(
        "posts/form.html",
        title="Create Post",
        form=form
    )


@bp.route("/<int:post_id>")
def detail(post_id):
    post = db.get_or_404(
        Post,
        post_id
    )

    comment_form = CommentForm()
    delete_form = DeletePostForm()

    comments = (
        Comment.query
        .filter_by(
            post_id=post.id,
            approved=True
        )
        .order_by(
            Comment.timestamp.desc()
        )
        .all()
    )

    return render_template(
        "posts/detail.html",
        title=post.title,
        post=post,
        comments=comments,
        comment_form=comment_form,
        delete_form=delete_form
    )


@bp.route(
    "/<int:post_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(post_id):
    post = db.get_or_404(
        Post,
        post_id
    )

    if post.author != current_user:
        flash(
            "You can edit only your own posts.",
            "danger"
        )

        return redirect(
            url_for(
                "posts.detail",
                post_id=post.id
            )
        )

    form = PostForm(
        obj=post
    )

    if form.validate_on_submit():

        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        post.published = form.published.data

        db.session.commit()

        flash(
            "Post updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "posts.detail",
                post_id=post.id
            )
        )

    return render_template(
        "posts/form.html",
        title="Edit Post",
        form=form
    )


@bp.post(
    "/<int:post_id>/delete"
)
@login_required
def delete(post_id):
    form = DeletePostForm()

    if not form.validate_on_submit():
        flash(
            "Invalid delete request.",
            "danger"
        )

        return redirect(
            url_for(
                "posts.list_posts"
            )
        )

    post = db.get_or_404(
        Post,
        post_id
    )

    if post.author != current_user:
        flash(
            "You can delete only your own posts.",
            "danger"
        )

        return redirect(
            url_for(
                "posts.detail",
                post_id=post.id
            )
        )

    db.session.delete(post)
    db.session.commit()

    flash(
        "Post deleted successfully.",
        "success"
    )

    return redirect(
        url_for("main.index")
    )
    