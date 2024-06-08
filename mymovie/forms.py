
from django import forms
from .models import Movie, Member_data


class MovieForm(forms.ModelForm):
    CHOICES = (
        ('coming_soon', '即將上映'),
        ('showing', '現正熱映'),
        ('removed','下架電影')
    )
    class Meta:
        model = Movie
        fields = ['date', 'show', 'director', 'actor', 'type', 'length', 'picture', 'movie_name']

class MemberEditForm(forms.ModelForm):
    class Meta:
        model = Member_data
        fields = ['gmail','phone_number']

class MemberSearchForm(forms.Form):
    member_id = forms.CharField(label='會員编號', max_length=100)

class MemberRegisterForm(forms.Form):
    member_id = forms.CharField(label='您的帳號', max_length=50)
    member_pw = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)
    member_pwc = forms.CharField(label='輸入確認密碼', widget=forms.PasswordInput)
    member_mail = forms.EmailField(label='電子信箱')
    member_phone = forms.CharField(label='手機號碼', max_length=15)  

class MemberLoginForm(forms.Form):
    member_id = forms.CharField(label='您的帳號', max_length=50)
    member_pw = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)

class MemberForgetForm(forms.Form):
    member_id = forms.CharField(label='您的帳號', max_length=50)
    member_pw = forms.CharField(label='新密碼', widget=forms.PasswordInput)
    member_pwc = forms.CharField(label='確認新密碼', widget=forms.PasswordInput)

class ManagerRegisterForm(forms.Form):
    CHOICES = (
        ('it', 'IT部門'),
        ('hr', '人事部門')
    )
    manager_id = forms.CharField(label='您的帳號', max_length=50)
    manager_name = forms.CharField(label='您的姓名', max_length=25)
    manager_department = forms.CharField(label='您的帳號', max_length=50)
    manager_pw = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)
    manager_pwc = forms.CharField(label='輸入確認密碼', widget=forms.PasswordInput)

class ManagerLoginForm(forms.Form):
    manager_id = forms.CharField(label='您的帳號', max_length=50)
    manager_pw = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)

class ManagerForgetForm(forms.Form):
    manager_id = forms.CharField(label='您的帳號', max_length=50)
    manager_pw = forms.CharField(label='新密碼', widget=forms.PasswordInput)
    manager_pwc = forms.CharField(label='確認新密碼', widget=forms.PasswordInput)