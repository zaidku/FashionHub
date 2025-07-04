"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Product
from django.utils.translation import gettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [  # Only the fields that actually exist on Product
            'name',
            'slug',
            'description',
            'price',
            'cost_price',
            'shipping_cost',
            'quantity',
            'size',
            'color',
            'is_active',
            'reorder_level',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
}