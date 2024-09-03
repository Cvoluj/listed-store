import pika
from django.conf import settings
from store.smtp_mail.models import SMTPMail
from .message import Message, MessageContext, MessageItem, SMTP

class RMQReceiptProducer:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE)

    def __init__(self, smtp_mail: SMTPMail) -> None:
        self.smtp_mail = smtp_mail

    def send_receipt_message(self, email_reciever, message_items: list[MessageItem]):
        smtp = SMTP(
            name=self.smtp_mail.name,
            smtp_email=self.smtp_mail.smtp_email,
            smtp_password=self.smtp_mail.smtp_password,
            smtp_port=self.smtp_mail.smtp_port,
            smtp_server=self.smtp_mail.smtp_server
        )

        context = MessageContext(
            name=self.smtp_mail.name, 
            items=message_items)
        
        message = Message(
            email=email_reciever, 
            subject=f'Purchasing on {self.smtp_mail.name}',
            context=context,
            smtp=smtp
        )

        self.channel.basic_publish(
            exchange='',
            routing_key=settings.RABBITMQ_QUEUE,
            body=message.json()
        )
