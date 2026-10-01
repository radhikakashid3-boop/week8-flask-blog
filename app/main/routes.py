from flask import render_template, request
from sqlalchemy import or_

from app.main import bp
from app.models import Post


@bp.route("/")
@bp.route("/index")
def index():
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
        "main/index.html",
        title="Home",
        posts=posts,
        search=search
    )


@bp.route("/about")
def about():
    return render_template(
        "main/about.html",
        title="About"
    )
    