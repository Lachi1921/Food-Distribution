from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone

from .decorators import *
from .models import *
from .forms import *

def home(request):
    menus = MonthlyMenu.objects.all()
    popular_menus = MonthlyMenu.objects.filter(popular=True)[:3]
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)


    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'popular_menus': popular_menus,
    }
    return render(request, 'index.html', context)

def monthly_menus(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
    }
    return render(request, 'monthly-menus.html', context)

def menu(request, slug):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    menu = get_object_or_404(MonthlyMenu, slug=slug)
    context = {
        'menu': menu,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'menus': menus,
    }
    return render(request, 'menu.html', context)

def deals(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    deals = Deal.objects.filter(frozen=False)
    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'deals': deals,
    }
    return render(request, 'daily-menu.html', context)

def deal(request, slug):
    menus = MonthlyMenu.objects.all()
    deal = get_object_or_404(Deal, slug=slug)
    deals = Deal.objects.filter(frozen=False)

    footer_deals = Deal.objects.filter(frozen=False).exclude(id=deal.id)
    footer_fdeals = Deal.objects.filter(frozen=True).exclude(id=deal.id)

    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'deals': deals,

        'deal': deal,
    }
    return render(request, 'deal-details.html', context)

def frozen_food(request):
    menus = MonthlyMenu.objects.all()
    deals = Deal.objects.filter(frozen=True)
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    context = {
        'menus': menus,
        'deals': deals,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
    }
    return render(request, 'frozen-deals.html', context)

def order(request, unique_id):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    
    item = get_object_or_404(Item, unique_id=unique_id)
    form = OrderForm(request.POST or None, item=item)
    if request.method == 'POST':
        if form.is_valid():
            order = form.save(commit=False)
            order.item = item
            persons = form.cleaned_data.get('persons')

            if item.item_type == 'D':
                base_price = item.deal.price / 3
                order.price = base_price * persons
            else:
                order.price = item.price * persons
            order.save()


            recurring = "None"
            if item.item_type == "M":
                if hasattr(item, 'monthly_menu'):
                    recurring = f"{item.monthly_menu.days}"

            invoice = Invoice.objects.create(
                order=order,
                recurring=recurring,
                pre_paid=False,
                inv_date=timezone.now().date(),
                paid=False,
                due_date=None,
            )

            send_mail(
                subject="Your Order Confirmation",
                message=(
                    f"Thank you for your order!\n\n"
                    f"Order Number: {order.order_number}\n"
                    f"Order Details:\n"
                    f"Item: {order.item.name}\n"
                    f"Persons: {order.persons}\n"
                    f"Total Price: {item.price}\n"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.email],
                fail_silently=False,
            )

            send_mail(
                subject=f"New Order Placed ({order.order_number})",
                message=(
                    f"A new order has been placed:\n\n"
                    f"Order Number: {order.order_number}\n"
                    f"Item: {item.name}\n"
                    f"Customer Email: {order.email}\n"
                    f"Profession: {order.profession}\n"
                    f"Customer phone: {order.phone}\n"
                    f"Address: {order.address}\n"
                    f"City: {order.get_city_display()}\n"
                    f"Order Details:\n"
                    f"Item: {item.name}\n"
                    f"Persons: {order.persons}\n"
                    f"Timing: {order.get_timing_display()}\n"
                    f"Order Note: {order.note}\n"
                    f"Total Price: {item.price}\n"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            return redirect("core:order-success", order_number=order.order_number)
    context = {
        'form': form,
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'item': item,
    }
    return render(request, 'order.html', context)

def order_success(request, order_number):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    order = Order.objects.get(order_number=order_number)
    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'order': order,
    }
    return render(request, 'order-success.html', context)

def foodlancer(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
    }
    return render(request, 'register-as-foodlancer.html', context)

def register_foodlancer(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    form = FoodlancerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            kitchen = form.cleaned_data['kitchen']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            street_address = form.cleaned_data['street_address']
            city = form.cleaned_data['city']
            postal_code = form.cleaned_data['postal_code']

            address = Address.objects.create(
                street=street_address,
                city=city,
                postal_code=postal_code
            )

            foodlancer = Foodlancer.objects.create(
                name=name,
                kitchen_name=kitchen,
                phone=phone,
                email=email,
                address=address
            )

            send_mail(
                    'Kitchen Registration Confirmation',
                    f'Hello {foodlancer.name},\n\n'
                    f'Your kitchen "{foodlancer.kitchen}" has been successfully registered!\n\n'
                    'Please WhatsApp us at +923335189005 for approval and more details.\n\n'
                    'Thank you!',
                    settings.EMAIL_HOST_USER,
                    [foodlancer.email],
                    fail_silently=False,
                )

            send_mail(
                'New Kitchen Registration',
                f'A new kitchen has been registered:\n\nName: {foodlancer.name}\nKitchen: {foodlancer.kitchen}\nPhone: {foodlancer.phone}\nEmail: {foodlancer.email}',
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Your kitchen has been registered!")
            return redirect('core:register-foodlancer')

        
    context = {
        'form': form,
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
    }
    return render(request, 'register-foodlancer.html', context)

def contact_us(request):
    form = ContactUsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            send_mail(
                'New Contact Us Message',
                f'Name: {name}\nEmail: {email}\nPhone/WhatsApp: {phone}\nMessage: {message}',
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            send_mail(
                'Contact Us - Message Received',
                f'Hello {name},\n\nThank you for reaching out! We have received your message and will get back to you shortly.\n\nYour message: {message}\n\nBest regards,\nLunch.pk',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully!")
            return redirect('core:contact-us')


    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    context = {
        'menus': menus,
        'form': form,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
    }
    return render(request, 'contact.html', context)

def TOS(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
    }
    return render(request, 'TOS.html', context)

def privacy_policy(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
    }
    return render(request, 'privacy-policy.html', context)


@superuser_required
def menus_list(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
    }
    return render(request, 'manage-menus.html', context)

@superuser_required
def create_menu(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    form = UnifiedMenuForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            monthly_menu = MonthlyMenu(
                name=request.POST['name'],
                desc=request.POST['desc'],
                breif_desc=request.POST.get('breif_desc', ''),
                persons=request.POST['persons'],
                days=request.POST['days'],
                meals=request.POST['meals'],
                price=request.POST['price'],
                popular = True if 'popular' in request.POST else False,
                nav_link = True if 'nav_link' in request.POST else False,
                slug=slugify(request.POST['slug']),
            )
            monthly_menu.save()

            weekly_schedule = WeeklySchedule(
                menu=monthly_menu,
                week1_mon_item=request.POST['week1_mon_item'],
                week1_tue_item=request.POST['week1_tue_item'],
                week1_wed_item=request.POST['week1_wed_item'],
                week1_thu_item=request.POST['week1_thu_item'],
                week1_fri_item=request.POST['week1_fri_item'],
                week1_sat_item=request.POST['week1_sat_item'],
                week2_mon_item=request.POST['week2_mon_item'],
                week2_tue_item=request.POST['week2_tue_item'],
                week2_wed_item=request.POST['week2_wed_item'],
                week2_thu_item=request.POST['week2_thu_item'],
                week2_fri_item=request.POST['week2_fri_item'],
                week2_sat_item=request.POST['week2_sat_item'],
                week3_mon_item=request.POST['week3_mon_item'],
                week3_tue_item=request.POST['week3_tue_item'],
                week3_wed_item=request.POST['week3_wed_item'],
                week3_thu_item=request.POST['week3_thu_item'],
                week3_fri_item=request.POST['week3_fri_item'],
                week3_sat_item=request.POST['week3_sat_item'],
                week4_mon_item=request.POST['week4_mon_item'],
                week4_tue_item=request.POST['week4_tue_item'],
                week4_wed_item=request.POST['week4_wed_item'],
                week4_thu_item=request.POST['week4_thu_item'],
                week4_fri_item=request.POST['week4_fri_item'],
                week4_sat_item=request.POST['week4_sat_item'],
            )
            weekly_schedule.save()
            return redirect('core:menu', slug=monthly_menu.slug)

    
    context = {
        'menus': menus,
        'form': form,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
    }
    return render(request, 'create-menu.html', context)

@superuser_required
def edit_menu(request, slug):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    menu = get_object_or_404(MonthlyMenu, slug=slug)
    weekly_schedule = get_object_or_404(WeeklySchedule, menu=menu)

    form = UnifiedMenuForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            menu.name = request.POST['name']
            menu.desc = request.POST['desc']
            menu.breif_desc = request.POST.get('breif_desc', '')
            menu.price = request.POST['price']
            menu.popular = 'popular' in request.POST
            menu.nav_link = 'nav_link' in request.POST
            menu.slug = slugify(request.POST['slug'])
            menu.save()

            weekly_schedule.week1_mon_item = request.POST['week1_mon_item']
            weekly_schedule.week1_tue_item = request.POST['week1_tue_item']
            weekly_schedule.week1_wed_item = request.POST['week1_wed_item']
            weekly_schedule.week1_thu_item = request.POST['week1_thu_item']
            weekly_schedule.week1_fri_item = request.POST['week1_fri_item']
            weekly_schedule.week1_sat_item = request.POST['week1_sat_item']
            weekly_schedule.week2_mon_item = request.POST['week2_mon_item']
            weekly_schedule.week2_tue_item = request.POST['week2_tue_item']
            weekly_schedule.week2_wed_item = request.POST['week2_wed_item']
            weekly_schedule.week2_thu_item = request.POST['week2_thu_item']
            weekly_schedule.week2_fri_item = request.POST['week2_fri_item']
            weekly_schedule.week2_sat_item = request.POST['week2_sat_item']
            weekly_schedule.week3_mon_item = request.POST['week3_mon_item']
            weekly_schedule.week3_tue_item = request.POST['week3_tue_item']
            weekly_schedule.week3_wed_item = request.POST['week3_wed_item']
            weekly_schedule.week3_thu_item = request.POST['week3_thu_item']
            weekly_schedule.week3_fri_item = request.POST['week3_fri_item']
            weekly_schedule.week3_sat_item = request.POST['week3_sat_item']
            weekly_schedule.week4_mon_item = request.POST['week4_mon_item']
            weekly_schedule.week4_tue_item = request.POST['week4_tue_item']
            weekly_schedule.week4_wed_item = request.POST['week4_wed_item']
            weekly_schedule.week4_thu_item = request.POST['week4_thu_item']
            weekly_schedule.week4_fri_item = request.POST['week4_fri_item']
            weekly_schedule.week4_sat_item = request.POST['week4_sat_item']
            weekly_schedule.save()

            return redirect('core:menu', slug=menu.slug)
        
    
    context = {
        'menus': menus,
        'form': form,
        'menu': menu,
        'weekly_schedule': weekly_schedule,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
    }
    return render(request, 'edit-menu.html', context)

@superuser_required
def delete_menu(request, slug):
    menu = get_object_or_404(MonthlyMenu, slug=slug)
    menu.delete()
    return redirect("core:manage-menus")      

@superuser_required
def duplicate_menu(request, slug):
    menu = get_object_or_404(MonthlyMenu, slug=slug)

    menu.pk = None
    menu.slug = slugify(f"{menu.slug}-copy")
    menu._state.adding = True
    menu.save()

    return redirect('core:manage-menus')

@superuser_required
def create_deal(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    form = DealForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form = form.save()

            return redirect('core:deals')

    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'form': form,
    }
    return render(request, 'create-deal.html', context)

@superuser_required
def edit_deal(request, slug):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    deal = get_object_or_404(Deal, slug=slug)

    form = DealForm(request.POST or None, request.FILES or None, instance=deal)

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return redirect('core:deals')

    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'form': form,
    }
    return render(request, 'edit-deal.html', context)

@superuser_required
def deals_list(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    deals = Deal.objects.all()
    context = {
        'deals': deals,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'menus': menus,
    }
    return render(request, 'manage-deals.html', context)

@superuser_required
def delete_deal(request, slug):
    deal = get_object_or_404(Deal, slug=slug)
    deal.delete()
    
    return redirect("core:manage-deals")

@superuser_required
def duplicate_deal(request, slug):
    deal = get_object_or_404(Deal, slug=slug)

    deal.pk = None
    deal.slug = slugify(f"{deal.slug}-copy")

    deal._state.adding = True
    deal.save()

    return redirect('core:manage-deals')

@superuser_required
def orders_list(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    orders = Order.objects.all()

    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'orders': orders,
    }
    return render(request, 'orders-list.html', context)

@superuser_required
def order_details(request, order_number):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    order = get_object_or_404(Order, order_number=order_number)

    return render(request, 'order-details.html', {'order': order, 'menus': menus, 'footer_deals': footer_deals, 'footer_fdeals': footer_fdeals})

@superuser_required
def edit_order(request, order_number):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    order = get_object_or_404(Order, order_number=order_number)
    form = OrderForm(request.POST or None, instance=order)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('core:order-details', order_number=order.order_number)

    return render(request, 'edit-order.html', {'form': form, 'order': order, 'menus': menus, 'footer_deals': footer_deals, 'footer_fdeals': footer_fdeals})

@superuser_required
def delete_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    order.delete()
    messages.success(request, f"Order {order_number} has been deleted.")
    return redirect('core:home')

@superuser_required
def invoice_list(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    invoices = Invoice.objects.all()
    return render(request, 'invoices.html', {'invoices': invoices, 'menus': menus, 'footer_deals': footer_deals, 'footer_fdeals': footer_fdeals})

@superuser_required
def edit_invoice(request, inv_num):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    invoice = get_object_or_404(Invoice, inv_num=inv_num)
    form = InvoiceForm(request.POST or None, instance=invoice)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('core:invoice-list')

    return render(request, 'edit-invoice.html', {'form': form, 'invoice': invoice, 'menus': menus, 'footer_deals': footer_deals, 'footer_fdeals': footer_fdeals})

@superuser_required
def delete_invoice(request, inv_num):
    invoice = get_object_or_404(Invoice, inv_num=inv_num)
    invoice.delete()
    return redirect('core:invoice-list')

@superuser_required
def foodlancer_list(request):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)

    foodlancers = Foodlancer.objects.all()
    return render(request, 'foodlancers.html', {'foodlancers': foodlancers, 'menus': menus, 'footer_deals': footer_deals, 'footer_fdeals': footer_fdeals})

@superuser_required
def edit_foodlancer(request, ID):
    menus = MonthlyMenu.objects.all()
    footer_deals = Deal.objects.filter(frozen=False)
    footer_fdeals = Deal.objects.filter(frozen=True)
    foodlancer = get_object_or_404(Foodlancer, id=ID)
    form = FoodlancerForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            kitchen = form.cleaned_data['kitchen']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            street_address = form.cleaned_data['street_address']
            city = form.cleaned_data['city']
            postal_code = form.cleaned_data['postal_code']

            foodlancer.address.street = street_address
            foodlancer.address.city = city
            foodlancer.address.postal_code = postal_code
            foodlancer.address.save()
            foodlancer.name = name
            foodlancer.kitchen_name = kitchen
            foodlancer.phone = phone
            foodlancer.email = email
            foodlancer.save()

            return redirect('core:foodlancers-list')
        else:
            print(form.errors)

    context = {
        'menus': menus,
        'footer_deals': footer_deals,
        'footer_fdeals': footer_fdeals,
        'form': form,
        'foodlancer': foodlancer,
    }
    return render(request, 'edit-foodlancer.html', context)

@superuser_required
def delete_foodlancer(request, ID):
    foodlancer = get_object_or_404(foodlancer, id=ID)
    foodlancer.delete()
    return redirect('core:foodlancer-list')



def page_not_found_404(request, exception):
    print(exception)
    return render(request, '404.html', status=404)