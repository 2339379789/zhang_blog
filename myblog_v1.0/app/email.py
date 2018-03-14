from flask import current_app, render_template
from app.extensions import mail
from flask_mail import Message
from threading import Thread


# 异步发送邮件
def async_send_mail(app, msg):
    # 必须在程序上下文中才能发送邮件，新建的线程没有，因此需要手动创建
    with app.app_context():
        # 发送邮件
        mail.send(msg)


# 封装函数发送邮件
def send_mail(to, subject, template, **kwargs):
    # 获取原始的app实例
    app = current_app._get_current_object()
    # 创建邮件对象
    msg = Message(subject, recipients=[to], sender=app.config['MAIL_USERNAME'])
    # 浏览器接收显示内容
    msg.html = render_template('email/' + template + '.html', **kwargs)
    # 终端接收显示内容
    msg.body = render_template('email/' + template + '.txt', **kwargs)
    # 创建线程，在新的线程中发送邮件
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr
