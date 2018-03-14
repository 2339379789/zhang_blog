from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length


# 发表博客表单
class PostsForm(FlaskForm):
    # 若想设置input的指定属性，可以通过render_kw
    content = TextAreaField('', render_kw={'placeholder': '这一刻的想法...'},
                            validators=[Length(3, 200, message='发表长度(3~200)')])
    submit = SubmitField('发表博客')


# 发表博客表单
class PostsToForm(FlaskForm):
    content = TextAreaField('', render_kw={'placeholder': '我还有一些想说的...'},
                            validators=[Length(3, 200, message='发表长度(3~200)')])
    submit = SubmitField('继续发表')


# 发表评论表单
class CommentForm(FlaskForm):
    content = TextAreaField('', render_kw={'placeholder': '我想说点什么。。。(不得超过100字)'},
                            validators=[Length(1, 100, message='不得超过100字')])
    submit = SubmitField('发表评论')


# 发表留言表单
class CommentToForm(FlaskForm):
    content = TextAreaField('', render_kw={'placeholder': '我要怼她/他。。。(不得超过100字)'},
                            validators=[Length(1, 100, message='不得超过100字')])
    submit = SubmitField('留言')
