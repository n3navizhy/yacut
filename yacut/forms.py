from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


class CutForm(FlaskForm):
    original_link = StringField(
        'Ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    custom_id = StringField(
        'Ваш короткий вариант',
        validators=[Length(1, 10), Optional()]
    )

    submit = SubmitField('Создать')
