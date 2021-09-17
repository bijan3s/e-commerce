from django import forms
from .models import Order


class CartForm(forms.Form):
    تعداد = forms.IntegerField(initial='1')
    product_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CartForm, self).__init__(*args, **kwargs)


class CheckoutForm(forms.Form):
    
    نام = forms.CharField(max_length=191)
    ایمیل = forms.EmailField()
    کد_پستی = forms.IntegerField()
    آدرس = forms.CharField(max_length=191,widget=forms.Textarea(attrs={'row': 5, 'col': 8}))
    widgets = {
            'address': forms.Textarea(attrs={'row': 5, 'col': 8}),
        }