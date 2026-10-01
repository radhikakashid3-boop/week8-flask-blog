from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length
)


class CommentForm(FlaskForm):
    content = TextAreaField(
        "Comment",
        validators=[
            DataRequired(),
            Length(min=2, max=1000)
        ]
    )

    submit = SubmitField(
        "Add Comment"
    )


class DeleteCommentForm(FlaskForm):
    submit = SubmitField(
        "Delete Comment"
    )
    