from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
# from auditlog.registry import auditlog

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# auditlog.register(Order)


fromaddr = 'demenkovakatarina@mail.ru'
mypass = "93XqCqhdZgaTje3KUut0"


def send(msg: MIMEMultipart, toaddr: str):
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


STATUS_CHOICES = [
    {'id': 'processing', 'name': 'В обработке'},
    {'id': 'ready', 'name': 'Готов к выдаче'},
    {'id': 'completed', 'name': 'Завершен'},
    {'id': 'cancelled', 'name': 'Отменен'},
]


@receiver(post_save, sender=Order)
def send_email_on_field_change(sender, instance, created, **kwargs):

    if not created:
        # print(Order.objects.get(pk=instance.pk).status)

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = instance.email
        msg['Subject'] = f"Обновление статуса заказа №{instance.pk}"


        status = ''
        for st in STATUS_CHOICES:
            if st['id'] == instance.status:
                status = st['name']
        if instance.status == 'ready':
            sum = 0
            for item in Order.objects.get(pk=instance.pk).orderitem_set.all():
                print(Order.objects.get(pk=instance.pk).orderitem_set.all())
                sum += item.price

            body = f"<h4>Статус заказа: {status}.</h4><h5>К оплате: <strong>{sum}</strong></h5><h5>Адрес: ул. Улица Октябрьской Революции, 23, город Смоленск</h5>"
        else:
            body = f"<h4>Статус заказа: {status}.</h4>"
        msg.attach(MIMEText(body, 'html'))

        send(msg, instance.email)


