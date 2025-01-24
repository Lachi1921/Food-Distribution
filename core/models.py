from django.db import models
from django.core.exceptions import ValidationError
import random, string
from uuid import uuid4
from django.core.mail import send_mail
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
def generate_short_id(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class MonthlyMenu(models.Model):
    name = models.CharField(max_length=250)
    desc = models.CharField(max_length=300)
    breif_desc = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField()
    persons = models.IntegerField()
    days = models.IntegerField()
    meals = models.IntegerField()
    popular = models.BooleanField()
    nav_link = models.BooleanField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.popular:
            popular_count = MonthlyMenu.objects.filter(popular=True).exclude(id=self.id).count()
            if popular_count >= 3:
                raise ValidationError("Only 3 menus can be marked as popular.")
        super().save(*args, **kwargs)

class WeeklySchedule(models.Model):
    menu = models.ForeignKey(MonthlyMenu, on_delete=models.CASCADE, related_name='weekly_schedules')
    
    # week 1
    week1_mon_item = models.CharField(max_length=255)
    week1_tue_item = models.CharField(max_length=255)
    week1_wed_item = models.CharField(max_length=255)
    week1_thu_item = models.CharField(max_length=255)
    week1_fri_item = models.CharField(max_length=255)
    week1_sat_item = models.CharField(max_length=255)
    # week 2
    week2_mon_item = models.CharField(max_length=255)
    week2_tue_item = models.CharField(max_length=255)
    week2_wed_item = models.CharField(max_length=255)
    week2_thu_item = models.CharField(max_length=255)
    week2_fri_item = models.CharField(max_length=255)
    week2_sat_item = models.CharField(max_length=255)
    # week 3
    week3_mon_item = models.CharField(max_length=255)
    week3_tue_item = models.CharField(max_length=255)
    week3_wed_item = models.CharField(max_length=255)
    week3_thu_item = models.CharField(max_length=255)
    week3_fri_item = models.CharField(max_length=255)
    week3_sat_item = models.CharField(max_length=255)
    # week 4
    week4_mon_item = models.CharField(max_length=255)
    week4_tue_item = models.CharField(max_length=255)
    week4_wed_item = models.CharField(max_length=255)
    week4_thu_item = models.CharField(max_length=255)
    week4_fri_item = models.CharField(max_length=255)
    week4_sat_item = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Weekly Schedule for {self.menu.name}"

class Deal(models.Model):
    image = models.ImageField(upload_to='deals/')
    name = models.CharField(max_length=250)
    desc = models.CharField(max_length=300)
    price = models.IntegerField()
    frozen = models.BooleanField()
    free_delivery = models.BooleanField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    TYPES = (
        ('M', 'Monthly Menu'),
        ('D', 'Daily Deal'),
    )
    unique_id = models.CharField(max_length=36, unique=True, editable=False, default=uuid4)
    name = models.CharField(max_length=300)
    item_type = models.CharField(choices=TYPES, max_length=1)
    monthly_menu = models.ForeignKey("MonthlyMenu", on_delete=models.CASCADE, null=True, blank=True, related_name="monthly_item")
    deal = models.ForeignKey("Deal", on_delete=models.CASCADE, null=True, blank=True, related_name="deal_item")
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = str(uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_item_type_display()} - {self.unique_id}'

class Order(models.Model):
    CITIES = (
        ('I', 'Islamabad'),
        ('K', 'Karachi'),
        ('L', 'Lahore'),
        ('R', 'Rawalpindi'),
        ('O', 'Other'),
    )

    TIMINGS = (
        ('L', 'Lunch'),
        ('D', 'Dinner'),
        ('O', 'Other'),
    )

    order_number = models.CharField(max_length=10, unique=True, editable=False, default=generate_short_id)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    profession = models.CharField(max_length=100, blank=True)
    persons = models.PositiveIntegerField()
    phone = PhoneNumberField(unique=True, region='PK')
    address = models.CharField(max_length=300)
    city = models.CharField(choices=CITIES, max_length=1)
    timing = models.CharField(choices=TIMINGS, max_length=1)
    note = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    item = models.ForeignKey("Item", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.name}"    

class Foodlancer(models.Model):
    name = models.CharField(max_length=255)
    kitchen_name = models.CharField(max_length=255)
    phone = PhoneNumberField(unique=True, region='PK')
    email = models.EmailField()
    address = models.OneToOneField("Address", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foodlancer: {self.kitchen_name}"

class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Pakistan")

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

    class Meta:
        verbose_name_plural = "Addresses"

def inv_id():
    number = 'INV-'+str(uuid4()).split('-')[1]
    return number

class Invoice(models.Model):
    RECURRINGS = (
        ("None", "None"),
        ("1mo", "Every 1 Month"),
        ("2mo", "Every 2 Month"),
        ("3mo", "Every 3 Month"),
        ("4mo", "Every 4 Month"),
        ("5mo", "Every 5 Month"),
        ("6mo", "Every 6 Month"),
        ("7mo", "Every 7 Month"),
        ("9mo", "Every 9 Month"),
        ("10mo", "Every 10 Month"),
        ("11mo", "Every 11 Month"),
        ("12mo", "Every 12 Month")
    )

    
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    inv_num = models.CharField(default=inv_id, max_length=15, unique=True)
    recurring = models.CharField(choices=RECURRINGS, max_length=18)
    pre_paid = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    inv_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    send_email = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.inv_num} for Order #{self.order.order_number}"

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            self.send_invoice_emails()

        if self.send_email:
            self.send_customer_email()

    def send_invoice_emails(self):
        try:
            self.send_customer_email()
            self.send_admin_notification()
        except Exception as e:
            print(f"Failed to send invoice emails: {e}")

    def send_customer_email(self):
        subject = f"Your Invoice #{self.inv_num} - {self.order.name}"
        pre_paid_text = f"Pre paid: {self.pre_paid}\n" if self.pre_paid else ""
        message = (
            f"Dear {self.order.name},\n\n"
            f"Your invoice has been generated. Here are the details:\n\n"
            f"Invoice Number: {self.inv_num}\n"
            f"Order Number: {self.order.order_number}\n"
            f"Invoice Date: {self.inv_date}\n"
            f"Due Date: {self.due_date}\n"
            f"Status: {self.status}\n"
            f"{pre_paid_text}"
            f"Total Amount: {self.order.price} {self.currency}\n\n"
            f"Notes: {self.notes or 'N/A'}\n\n"
            f"Thank you for choosing Lunch.pk.\n"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.order.email],
            fail_silently=False,
        )

    def send_admin_notification(self):
        subject = f"New Invoice Generated: #{self.inv_num}"
        message = (
            f"A new invoice has been created:\n\n"
            f"Invoice Number: {self.inv_num}\n"
            f"Order Number: {self.order.order_number}\n"
            f"Customer Name: {self.order.name}\n"
            f"Customer Email: {self.order.email}\n"
            f"Total Amount: {self.order.price}\n"
            f"Invoice Date: {self.inv_date}\n"
            f"Due Date: {self.due_date}\n"
            f"Notes: {self.notes or 'N/A'}\n"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )

