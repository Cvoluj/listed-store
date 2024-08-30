import pika
from django.conf import settings
from store.smtp_mail.models import SMTPMail
from .message import Message, MessageContext, MessageItem

class RMQReceiptProducer:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE)

    def __init__(self, smtp_mail: SMTPMail) -> None:
        self.smtp_mail = smtp_mail

    def send_receipt_message(self, email_reciever, message_items: list[MessageItem]):
        context = MessageContext(
            name=self.smtp_mail.name, 
            items=message_items)
        
        message = Message(
            email=email_reciever, 
            subject=f'Purchasing on {self.smtp_mail.name}',
            context=context
        )

        self.channel.basic_publish(
            exchange='',
            routing_key=settings.RABBITMQ_QUEUE,
            body=message.json()
        )
