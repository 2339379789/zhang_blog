from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from app.forms import RegisterForm, LoginForm, Change_passwordForm, Change_emailForm, Change_iconForm, \
    Retrieve_passwordForm
from app.models import User
from app.extensions import db, photos
from app.email import send_mail
from flask_login import login_user, logout_user, login_required, current_user
import os
from PIL import Image

# 创建用户视图蓝本
user = Blueprint('user', __name__)


# 用户注册
@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 根据表单数据创建用户对象
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        # 将用户对象保存到数据库
        db.session.add(u)
        # 下面生成token需要用户id，此时还没有id，需要手动提交
        db.session.commit()
        # 提示用户前往邮箱激活
        flash('用户已注册，只需前往您的邮箱激活即可使用')
        # 生成激活邮件的token
        token = u.generate_activate_token()
        # 发送激活的邮件
        send_mail(u.email, '账号激活', 'activate', user=u, token=token)
        # 跳转到主页
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


# 账号激活
@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('恭喜您激活成功，现在可以正常使用了')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))


# 账号登录
@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 根据输入的用户名查找数据库中对应的用户
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash('该用户不存在')
        elif not u.confirmed:
            flash('用户尚未激活，请激活后再登录')
        elif u.verify_password(form.password.data):
            login_user(u, remember=form.remember.data)
            flash('登录成功！')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('密码不正确，请重新登录')
    return render_template('user/login.html', form=form)


# 退出登录
@user.route('/logout/')
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


# 显示个人信息
@user.route('/profile/')
@login_required
def profile():
    img_url = photos.url(current_user.icon)
    return render_template('user/profile.html', img_url=img_url)


# 修改密码
@user.route('/change_password/', methods=['GET', 'POST'])
@login_required
def change_password():
    form = Change_passwordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('你的密码已经修改成功')
            return redirect(url_for('user.login'))
        else:
            flash('您输入的旧密码不正确，请重新输入')
    return render_template('user/change_password.html', form=form)


# 修改邮箱
@user.route('/change_email/', methods=['GET', 'POST'])
@login_required
def change_email():
    form = Change_emailForm()
    if form.validate_on_submit():
        global u
        u = form.email.data
        # 生成token
        token = current_user.generate_activate_token()
        # 发送用户账户的激活邮件
        send_mail(form.email.data, '修改邮箱', 'change_email_activate', user=current_user, token=token)
        # 弹出flash消息提示用户
        flash('邮箱修改的验证已发送到新邮箱,点击邮件完成确认修改')
        return redirect(url_for('user.change_email'))
    return render_template('user/change_email.html', form=form)


# 账号修改邮箱激活
@user.route('/change_email_activate/<token>')
def change_email_activate(token):
    if User.check_activate_token(token):
        current_user.email = u
        db.session.add(current_user)
        flash('邮箱已修改')
        return redirect(url_for('user.profile'))
    else:
        flash('邮箱修改失败')
        return redirect(url_for('user/change_email.html'))


# 修改头像
@user.route('/change_icon/', methods=['GET', 'POST'])
@login_required
def change_icon():
    form = Change_iconForm()
    if form.validate_on_submit():
        # 获取文件后缀
        suffix = os.path.splitext(form.icon.data.filename)[1]
        # 生成文件名
        filename = random_string() + suffix
        # 保存图片
        photos.save(form.icon.data, name=filename)
        # 文件保存路径
        filepath = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        # 生成缩略图
        img = Image.open(filepath)
        img.thumbnail((200, 200))
        img.save(filepath)
        # 删除原来的图片
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
        # 保存修改至数据库
        current_user.icon = filename
        db.session.add(current_user)
        flash('头像已保存')
        return redirect(url_for('user.change_icon'))
    img_url = photos.url(current_user.icon)
    return render_template('user/change_icon.html', form=form, img_url=img_url)


# 随机生成字符串
def random_string(length=32):
    import random
    base_string = '1234567890qwertyuiopasdfghjklmnbvcxz'
    return ''.join(random.choice(base_string) for i in range(length))


# 找回密码
@user.route('/retrieve_password/', methods=['GET', 'POST'])
def retrieve_password():
    form = Retrieve_passwordForm()
    if form.validate_on_submit():
        global password1
        password1 = form.confirm.data
        # 发送验证的邮件
        send_mail(form.email.data, '找回密码', 'retrieve_password', username=form.username.data)
        # 弹出flash消息提示用户
        flash('邮件已发送，请前往邮箱点击确认才可完成修改')
        return redirect(url_for('user.retrieve_password'))
    return render_template('user/retrieve_password.html', form=form)


# 找回密码验证邮箱
@user.route('/retrieve_password_activate/<username>')
def retrieve_password_activate(username):
    u = User.query.filter_by(username=username).first()
    if u:
        u.password = password1
        db.session.add(u)
        flash('密码已修改')
        return redirect(url_for('user.login'))
    else:
        flash('用户不存在')
        return redirect(url_for('user/retrieve_password.html'))
