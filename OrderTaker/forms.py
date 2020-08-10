from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Name', 'pattern': '.{3,}',
                                      'required title': '3 Characters minimum'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter password'}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your 10 digit mobile number',
                                      'pattern': '[1-9]{1}[0-9]{9}',
                                      'required title': 'Enter a valid mobile number'}),
        required=False)
