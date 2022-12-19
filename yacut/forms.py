from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp
from settings import LINK_SAMPLE, MAX_LENGTH_CUSTOM, MAX_LENGTH_LINK

LINK = "Ссылка"
REQUIRED_FIELD = "Обязательное поле"
URL_ERROR = "пожжалуйста введите URL"
SHORT_VERSION = 'Ваш короткий вариант'
SUBMIT = "Создать"


class CutForm(FlaskForm):
    original_link = URLField(
        LINK,
        validators=[DataRequired(message=REQUIRED_FIELD),
                    Length(max=MAX_LENGTH_LINK), URL(message=URL_ERROR)]
    )
    custom_id = StringField(
        SHORT_VERSION,
        validators=[Length(max=MAX_LENGTH_CUSTOM), Optional(),
                    Regexp(LINK_SAMPLE)]

    )

    submit = SubmitField(SUBMIT)
