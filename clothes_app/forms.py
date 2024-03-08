from django import forms

class ContactForm(forms.Form):
    person = forms.CharField(max_length=50,
                              widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی'}),
                              required=True)
    email = forms.EmailField(max_length=100,
                             widget=forms.TextInput(attrs={'placeholder': 'ایمیل'}),
                             required=True)
    text = forms.CharField(max_length=1500,
                            widget=forms.Textarea(attrs={'placeholder': ' پیام...'}),
                            required=True)