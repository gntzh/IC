from celery import task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


@task
def send_verify_email(info):
    subject = "Shoor's Site 用户%s邮箱验证" % info['username']
    to_email = info['email']
    from_email = settings.DEFAULT_EMAIL_FROM
    text_content = "欢迎访问Shoor's Site，请点击验证链接来验证邮箱%s" % info['verify_url']
    html_content = "<p>欢迎访问Shoor's Site，请点击验证链接来验证邮箱%s </p>" % info['verify_url']
    mail = EmailMultiAlternatives(
        subject, text_content, from_email, [to_email, ])
    mail.attach_alternative(html_content, 'text/html')
    mail_sent = mail.send()
    print(mail_sent, type(mail_sent))
    return mail_sent
