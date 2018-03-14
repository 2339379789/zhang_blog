from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for, g
from flask_login import current_user, login_required
from app.models import Posts, User
from app.forms import PostsForm, CommentForm, PostsToForm, CommentToForm
from app.extensions import db

posts = Blueprint('posts', __name__)


@posts.route('/collect/<int:pid>')
def collect(pid):
    # 判断是否收藏
    if current_user.is_favorite(pid):
        current_user.del_favorite(pid)
    else:
        current_user.add_favorite(pid)
    favorite_count = Posts.query.get(pid).users.count()
    return jsonify({'result': 'ok', 'data': favorite_count, 'pid': pid})


# 发表博客
@posts.route('/blogs/', methods=['GET', 'POST'])
@login_required
def blogs():
    form = PostsForm()
    if form.validate_on_submit():
        u = current_user._get_current_object()
        p = Posts(content=form.content.data, user=u)
        db.session.add(p)
        flash('你的博客已经发表成功，点击继续发表可继续发表，点击返回可返回首页')
        return redirect(url_for('posts.blogs_continue'))
    # 读取分页数据 'page':当前页码，默认第一页
    page = request.args.get('page', 1, type=int)
    # 只保留我发表的博客，然后按照时间倒序排列
    pagination = Posts.query.filter_by(rid=0).filter_by(uid=current_user.id).order_by(Posts.timestamp.desc()).paginate(
        page, per_page=5, error_out=False)
    # 获取当前分页所有数据
    posts = pagination.items
    for p in posts:
        p.count = Posts.query.filter_by(rid=p.id).count()
    return render_template('posts/blogs.html', form=form, posts=posts, pagination=pagination)


# 继续发表博客
@posts.route('/blogs_continue/', methods=['GET', 'POST'])
@login_required
def blogs_continue():
    form = PostsToForm()
    if form.validate_on_submit():
        u = current_user._get_current_object()
        p = Posts(content=form.content.data, user=u)
        db.session.add(p)
        flash('你的博客已经发表成功，点击继续发表可继续发表，点击返回可返回首页')
        return redirect(url_for('posts.blogs_continue'))
    # 读取分页数据 'page':当前页码，默认第一页
    page = request.args.get('page', 1, type=int)
    # 只保留我发表的博客，然后按照时间倒序排列
    pagination = Posts.query.filter_by(rid=0).filter_by(uid=current_user.id).order_by(Posts.timestamp.desc()).paginate(
        page, per_page=5, error_out=False)
    # 获取当前分页所有数据
    posts = pagination.items
    for p in posts:
        p.count = Posts.query.filter_by(rid=p.id).count()
    return render_template('posts/blogs_continue.html', form=form, posts=posts, pagination=pagination)


# 我发表的
@posts.route('/my_blogs/')
@login_required
def my_blogs():
    page = request.args.get('page', 1, type=int)
    # 只保留我发表的博客，然后按照时间倒序排列
    pagination = Posts.query.filter_by(uid=current_user.id).filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(
        page, per_page=5, error_out=False)
    # 获取当前分页所有数据
    posts = pagination.items
    return render_template('posts/my_blogs.html', posts=posts, pagination=pagination)


# 我收藏的
@posts.route('/my_favoriate/')
@login_required
def my_favoriate():
    page = request.args.get('page', 1, type=int)
    u = current_user._get_current_object()
    pagination = User.query.get(u.id).favorites.order_by(Posts.timestamp.desc()).paginate(page, per_page=5,
                                                                                          error_out=False)
    posts = pagination.items
    return render_template('posts/my_favoriate.html', posts=posts, pagination=pagination)


# 发表评论
@posts.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    post = Posts.query.filter_by(id=id)
    if form.validate_on_submit():
        u = current_user._get_current_object()
        p = Posts(content=form.content.data, rid=id, user=u)
        db.session.add(p)
        flash('您的评论已发表')
        return redirect(url_for('posts.comment', id=id))
    # 读取分页数据 'page':当前页码，默认第一页
    page = request.args.get('page', 1, type=int)
    # 只保留评论，然后按照时间倒序排列
    pagination = Posts.query.filter_by(rid=id).order_by(Posts.timestamp.desc()).paginate(page, per_page=5,
                                                                                         error_out=False)
    count = Posts.query.filter_by(rid=id).count()
    # 获取当前分页所有数据
    posts = pagination.items
    return render_template('posts/comment.html', form=form, post=post, pagination=pagination, posts=posts, count=count)


# 发表评论的评论（留言）
@posts.route('/comment_to_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment_to_comment(id):
    form = CommentToForm()
    # 获取当前评论
    post = Posts.query.filter_by(id=id)
    if form.validate_on_submit():
        u = current_user._get_current_object()
        p = Posts(content=form.content.data, rid=id, user=u)
        db.session.add(p)
        flash('留言成功')
        return redirect(url_for('posts.comment_to_comment', id=id))
    # 读取分页数据 'page':当前页码，默认第一页
    page = request.args.get('page', 1, type=int)
    # 只保留评论，然后按照时间倒序排列
    pagination = Posts.query.filter_by(rid=id).order_by(Posts.timestamp.desc()).paginate(page, per_page=5,
                                                                                         error_out=False)
    count = Posts.query.filter_by(rid=id).count()
    # 获取当前分页所有数据
    posts = pagination.items
    return render_template('posts/comment_to_comment.html', form=form, post=post, pagination=pagination, posts=posts,
                           count=count)
