from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from robots.models import Robot
from orders.models import Order
from orders.lexicon import EMAIL


@receiver(post_save, sender=Robot)
def notify_for_available_robots(sender, instance, created, **kwargs):
    '''When a new robot is released, all customers who've been placed orders
    for that series of robot will be notified for availability'''
    if created:
        robot_orders = Order.objects.filter(robot_serial=instance.serial)
        if robot_orders:
            for order in robot_orders:
                model, version = order.robot_serial.split('-')
                send_mail(subject=EMAIL['subject'],
                          message=EMAIL['text'].format(model=model,
                                                       version=version),
                          from_email=EMAIL['from_whom'],
                          recipient_list=[order.customer.email])
