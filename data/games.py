import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from flask_wtf import *
from wtforms import *
from wtforms.validators import *


class Games(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    log = sqlalchemy.Column(sqlalchemy.Text, default='''########################################
#                                      #
#                                      #
#                                      #
#                                      #
#                                      #
#                                      #
#                                      #
#                                      #
#                                      #
#              XXX                     #
#                                      #
#                                      #
#                                      #
#                                      #
#                             a        #
#                                      #
#                                      #
#                                      #
########################################
''')
    log2 = sqlalchemy.Column(sqlalchemy.Text, default='''snake_body = [
	(5, FIELD_HEIGHT // 2),
	(4, FIELD_HEIGHT // 2),
	(3, FIELD_HEIGHT // 2)]
DIRECTIONS = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
direction = DIRECTIONS['right']
eaten = False
apple_pos = place_apple()''')
    input = sqlalchemy.Column(sqlalchemy.Text, default='''d
''')
    user = orm.relationship('User')




class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
