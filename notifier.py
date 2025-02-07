import smtplib
from email.mime.text import MIMEText
import os

def send_notification(subject, message):
    """
    環境変数 SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_PASSWORD が設定されていることが前提です。
    例：Gmail を使用する場合
    """
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.environ.get("SENDER_EMAIL")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")

    if not sender_email or not receiver_email or not password:
        print("メール通知の設定が不十分です。環境変数を確認してください。")
        return

    msg = MIMEText(message, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        server.quit()
        print("通知メールを送信しました。")
    except Exception as e:
        print("通知メール送信中にエラーが発生しました:", e)
