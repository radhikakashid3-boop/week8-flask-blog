from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired,
    Length
)


class PostForm(FlaskForm):
    title = StringField(
        "Post Title",
        validators=[
            DataRequired(),
            Length(min=3, max=200)
        ]
    )

    content = TextAreaField(
        "Content",
        validators=[
            DataRequired(),
            Length(min=10)
        ]
    )

    published = BooleanField(
        "Publish",
        default=True
    )

    submit = SubmitField(
        "Save Post"
    )


class DeletePostForm(FlaskForm):
    submit = SubmitField(
        "Delete Post"
    )
    