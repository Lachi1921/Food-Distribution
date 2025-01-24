from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', home, name="home"),
    path('monthly-menus/', monthly_menus, name="monthly-menus"),
    path('monthly-menu/<slug:slug>/', menu, name="menu"),
    path('deals/', deals, name="deals"),
    path('deals/<slug:slug>/', deal, name="deal-details"),
    path('frozen-menu/', frozen_food, name="frozen-deals"),
    path('place-an-order/<str:unique_id>/', order, name="order"),
    path('order-success/<str:order_number>/', order_success, name="order-success"),
    path('terms-of-service/', TOS, name="TOS"),
    path('privacy-policy/', privacy_policy, name="privacy-policy"),
    
    path('become-a-foodlancer/', foodlancer, name="foodlancer"),
    path('apply-for-foodlancer/', register_foodlancer, name="register-foodlancer"),
    path('contact-us/', contact_us, name="contact-us"),

    # menus
    path('dashboard/manage-menus/', menus_list, name="manage-menus"),
    path('dashboard/manage-menus/duplicate/<slug:slug>/', duplicate_menu, name='duplicate-menu'),
    path('dashboard/create-menu/', create_menu, name="create-menu"),
    path('dashboard/edit-menu/<slug:slug>/', edit_menu, name="edit-menu"),
    path('dashboard/delete-menu/<slug:slug>/', delete_menu, name="delete-menu"),

    # deals
    path('dashboard/manage-deals/', deals_list, name="manage-deals"),
    path('dashboard/manage-deals/duplicate/<slug:slug>/', duplicate_deal, name='duplicate-deal'),
    path('dashboard/create-deal/', create_deal, name="create-deal"),
    path('dashboard/edit-deal/<slug:slug>/', edit_deal, name="edit-deal"),
    path('dashboard/delete-deal/<slug:slug>/', delete_deal, name="delete-deal"),

    #orders
    path('dashboard/manage-orders/', orders_list, name="all-orders"),
    path('dashboard/manage-orders/<str:order_number>/', order_details, name='order-details'),
    path('dashboard/manage-orders/edit/<str:order_number>/', edit_order, name='edit-order'),
    path('dashboard/manage-orders/delete/<str:order_number>/', delete_order, name='delete-order'),

    #invoices
    path('dashboard/invoices/', invoice_list, name='invoice-list'),
    path('dashboard/invoices/edit/<str:inv_num>/', edit_invoice, name='edit-invoice'),
    path('dashboard/invoices/delete/<str:inv_num>/', delete_invoice, name='delete-invoice'),

    #foodlancers
    path('dashboard/foodlancers/', foodlancer_list, name='foodlancers-list'),
    path('dashboard/foodlancers/edit/<int:ID>/', edit_foodlancer, name='edit-foodlancer'),
    path('dashboard/foodlancers/delete/<int:ID>/', delete_foodlancer, name='delete-foodlancer'),

]
