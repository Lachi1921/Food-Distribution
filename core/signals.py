from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MonthlyMenu, Deal, Item

@receiver(post_save, sender=MonthlyMenu)
def create_item_for_monthly_menu(sender, instance, created, **kwargs):
    if created:
        Item.objects.create(item_type='M', name=instance.name, price=instance.price, monthly_menu=instance)


@receiver(post_save, sender=Deal)
def create_item_for_deal(sender, instance, created, **kwargs):
    if created:
        Item.objects.create(item_type='D', name=instance.name, price=instance.price, deal=instance)
