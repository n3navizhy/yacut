from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL


link = "Ссылка"
Required_field = "Обязательное поле"
Url_error = "пожжалуйста введите URL"
Short_version = 'Ваш короткий вариант'
Submit = "Создать"


class CutForm(FlaskForm):
    original = URLField(
        link,
        validators=[DataRequired(message=Required_field),
                    Length(1, 128), URL(message=Url_error)]
    )
    custom_id = StringField(
        Short_version,
        validators=[Length(0, 16), Optional()]
    )

    submit = SubmitField(Submit)
