from .models import Deal
from django import forms
from django.forms import inlineformset_factory
from .models import *
from phonenumber_field.formfields import PhoneNumberField


class UnifiedMenuForm(forms.Form):
    name = forms.CharField(max_length=250, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}))
    desc = forms.CharField(
        max_length=300, widget=forms.Textarea(attrs={
        'class': 'form-control shadow-none',
        'rows': 3
    }))
    breif_desc = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}))
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control shadow-none'}))
    persons = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control shadow-none'}))
    days = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control shadow-none'}))
    meals = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control shadow-none'}))
    popular = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))
    nav_link = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))
    slug = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}))

    # week 1
    week1_mon_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week1_tue_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week1_wed_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week1_thu_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week1_fri_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week1_sat_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)

    # week 2
    week2_mon_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week2_tue_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week2_wed_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week2_thu_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week2_fri_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week2_sat_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)

    # week 3
    week3_mon_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week3_tue_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week3_wed_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week3_thu_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week3_fri_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week3_sat_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)

    # week 4
    week4_mon_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week4_tue_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week4_wed_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week4_thu_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week4_fri_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)
    week4_sat_item = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-none'}), required=True)

# class ServingOptionForm(forms.ModelForm):
#     class Meta:
#         model = ServingOption
#         fields = ['persons', 'price']

#     persons = forms.IntegerField(widget=forms.NumberInput(attrs={
#         'class': 'form-control shadow-none',
#         'placeholder': 'Number of persons'
#     }))

#     price = forms.IntegerField(widget=forms.NumberInput(attrs={
#         'class': 'form-control shadow-none',
#         'placeholder': 'Enter price'
#     }))

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['image', 'name', 'desc', 'price',  'frozen', 'free_delivery', 'slug']

    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control shadow-none',
        'placeholder': 'Upload an image'
    }))

    name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={
        'class': 'form-control shadow-none',
        'placeholder': 'Enter deal name'
    }))

    desc = forms.CharField(max_length=300, widget=forms.Textarea(attrs={
        'class': 'form-control shadow-none',
        'rows': 3,
        'placeholder': 'Enter description'
    }))

    price = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control shadow-none',
        'placeholder': 'Enter price for 3 servings'
    }))

    frozen = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input shadow-none'}),
        label='Is it frozen deal?'
    )

    free_delivery = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input shadow-none'}),
        label='Free delivery?'
    )

    slug = forms.SlugField(widget=forms.TextInput(attrs={
        'class': 'form-control shadow-none',
        'placeholder': 'Enter slug'
    }))

class OrderForm(forms.ModelForm):
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-none',
        }),
        error_messages={
            'invalid': 'Enter a valid phone number.',
        },
    )

    class Meta:
        model = Order
        fields = [
            'name', 'email', 'profession', 'persons', 'phone', 'address', 'city', 'timing', 'note', 'item', 'price',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control shadow-none'}),
            'email': forms.EmailInput(attrs={'class': 'form-control shadow-none'}),
            'profession': forms.TextInput(attrs={'class': 'form-control shadow-none'}),
            'persons': forms.NumberInput(attrs={'class': 'form-control shadow-none'}),
            'address': forms.TextInput(attrs={'class': 'form-control shadow-none'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'timing': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control shadow-none', 'style': 'height: 116px;'}),
        }

    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item', None)
        super().__init__(*args, **kwargs)

        if item.item_type == 'D':
            self.fields['persons'] = forms.IntegerField(
                min_value=3,
                widget=forms.NumberInput(attrs={'class': 'form-control shadow-none'}),
                required=True
            )

class FoodlancerForm(forms.Form):
    name = forms.CharField(
        max_length=250, 
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none'}), 
        label="Your name"
    )
    kitchen = forms.CharField(
        max_length=250, 
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none'}), 
        label="Kitchen name"
    )
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-none',
        }),
        error_messages={
            'invalid': 'Enter a valid phone number.',
        },
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control shadow-none'}),
        label="Email address"
    )
    street_address = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none'}),
        label="Street address"
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none'}),
        label="City"
    )
    postal_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none'}),
        label="Postal code"
    )

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control shadow-none'}), label="Your Name")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control shadow-none'}), label="Email")
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-none',
        }),
        error_messages={
            'invalid': 'Enter a valid phone number.',
        },
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control shadow-none'}), label="Message")

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'order', 'recurring', 'pre_paid', 'paid', 'inv_date', 'due_date', 'notes', 'send_email'
        ]
        widgets = {
            'order': forms.Select(attrs={'class': 'form-select shadow-none'}),
            'recurring': forms.Select(choices=Invoice.RECURRINGS, attrs={'class': 'form-select shadow-none'}),
            'pre_paid': forms.CheckboxInput(attrs={'class': 'form-check-input shadow-none'}),
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input shadow-none'}),
            'inv_date': forms.DateInput(attrs={'class': 'form-control shadow-none', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control shadow-none', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control shadow-none', 'style': 'height: 116px;'}),
            'send_email': forms.CheckboxInput(attrs={'class': 'form-check-input shadow-none'})
        }