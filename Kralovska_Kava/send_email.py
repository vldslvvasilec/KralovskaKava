import os
import sys
import django
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils.translation import gettext as _
from django.utils.translation import activate

# Установка пути к проекту и добавление в sys.path
current_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(current_path, os.pardir))
sys.path.append(project_path)

# Установка переменной окружения и настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kralovska_Kava.settings')
django.setup()

def send_reservation_email(user_email, user_name, restaurant_name, reservation_date, reservation_time, user_language):
    # Установите язык пользователя
    activate(user_language)

    # Настройки email сервера
    smtp_server = os.getenv('SMPT_SERVER')
    smtp_port = os.getenv('SMPT_PORT')
    smtp_user = os.getenv('SMPT_USER')
    smtp_password = os.getenv('SMPT_PASSWORD')

    print(user_language)
    print(user_name)
    print(user_email)
    print(restaurant_name)
    print(reservation_date)
    print(reservation_date)

    # Создание email сообщения
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = user_email
    msg['Subject'] = _('Successful Reservation')

    body = _(
        "Dear {user_name},\n\n"
        "Your reservation at Kralovska Kava {restaurant_name} has been successfully made.\n"
        "Date: {reservation_date}\n"
        "Time: {reservation_time}\n\n"
        "Thank you for choosing our restaurant!\n\n"
        "Best regards,\n"
        "The Kralovska Kava {restaurant_name} Team"
    ).format(
        user_name=user_name,
        restaurant_name=restaurant_name,
        reservation_date=reservation_date,
        reservation_time=reservation_time
    )

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)
    server.quit()

