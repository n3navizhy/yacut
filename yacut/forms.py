from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


class CutForm(FlaskForm):
    original_link = StringField(
        'Введите название фильма',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    custom_id = TextAreaField(
        'Напишите мнение',
        validators=[Length(1, 256), Optional()]
    )

    submit = SubmitField('Создать')
