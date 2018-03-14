from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models import User
from app.extensions import photos
from flask_wtf.file import FileField, FileRequired, FileAllowed


# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名',
                           validators=[DataRequired(message='用户名不能为空'), Length(3, 12, message='用户名只能在3~12个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(3, 20, message='密码只能在3~20个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    email = StringField('邮箱', validators=[Email(message='无效的邮箱格式')])
    submit = SubmitField('立即注册')

    # 自定义用户名验证器
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已注册，请选用其它名称')

    # 自定义邮箱验证器
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册使用，请选用其它邮箱')


# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空')])
    remember = BooleanField('记住我')
    submit = SubmitField('立即登录')


# 修改密码表单
class Change_passwordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired(message='密码不能为空')])
    password = PasswordField('新密码', validators=[DataRequired(message='密码不能为空')])
    confirm = PasswordField('确认新密码', validators=[EqualTo('password', message='两次密码不一致')])
    submit = SubmitField('立即修改')


# 修改邮箱表单
class Change_emailForm(FlaskForm):
    email = StringField('新邮箱', validators=[Email(message='无效的邮箱格式')])
    submit = SubmitField('立即修改')


# 修改头像表单
class Change_iconForm(FlaskForm):
    icon = FileField('头像', validators=[FileAllowed(photos, message='只能上传图片'), FileRequired('请选择文件')])
    submit = SubmitField('点击上传')


# 找回密码表单
class Retrieve_passwordForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空')])
    email = StringField('输入注册邮箱', validators=[Email(message='无效的邮箱格式')])
    password = PasswordField('新密码', validators=[DataRequired(message='密码不能为空')])
    confirm = PasswordField('确认新密码', validators=[EqualTo('password', message='两次密码不一致')])
    submit = SubmitField('发送验证')
