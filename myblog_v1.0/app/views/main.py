from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.forms import PostsForm
from app.extensions import db
from flask_login import current_user
from app.models import Posts

main = Blueprint('main', __name__)


# 首页
@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        # 判断是否登录
        if current_user.is_authenticated:
            # 获取当前用户
            u = current_user._get_current_object()
            # 创建博客对象
            p = Posts(content=form.content.data, user=u)
            # 保存到数据库
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('用户尚未登录。请登录后发表')
            return redirect(url_for('user.login'))
    # 分页读取数据
    # 获取get参数里的页码，默认为当前页
    page = request.args.get('page', 1, type=int)
    # 获取数据库中博客的数据，按时间排序(pagination是个对象)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=5,
                                                                                        error_out=False)
    # 读取每页数据
    posts = pagination.items
    for post in posts:
        post.count = post.users.count()
    return render_template('main/index.html', form=form, pagination=pagination, posts=posts)
