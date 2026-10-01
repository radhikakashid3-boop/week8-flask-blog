from flask import (
    flash,
    redirect,
    url_for
)

from flask_login import (
    current_user,
    login_required
)

from app import db
from app.comments import bp
from app.comments.forms import (
    CommentForm,
    DeleteCommentForm
)
from app.models import Comment, Post


@bp.post("/add/<int:post_id>")
@login_required
def add(post_id):
    post = db.get_or_404(
        Post,
        post_id
    )

    form = CommentForm()

    if not form.validate_on_submit():
        flash(
            "Please enter a valid comment.",
            "danger"
        )

        return redirect(
            url_for(
                "posts.detail",
                post_id=post.id
            )
        )

    comment = Comment(
        content=form.content.data.strip(),
        author=current_user,
        post=post,
        approved=True
    )

    db.session.add(comment)
    db.session.commit()

    flash(
        "Comment added successfully.",
        "success"
    )

    return redirect(
        url_for(
            "posts.detail",
            post_id=post.id
        )
    )


@bp.post("/delete/<int:comment_id>")
@login_required
def delete(comment_id):
    form = DeleteCommentForm()

    if not form.validate_on_submit():
        flash(
            "Invalid delete request.",
            "danger"
        )

        return redirect(
            url_for("main.index")
        )

    comment = db.get_or_404(
        Comment,
        comment_id
    )

    if comment.author != current_user:
        flash(
            "You can delete only your own comments.",
            "danger"
        )

        return redirect(
            url_for(
                "posts.detail",
                post_id=comment.post_id
            )
        )

    post_id = comment.post_id

    db.session.delete(comment)
    db.session.commit()

    flash(
        "Comment deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "posts.detail",
            post_id=post_id
        )
    )
    