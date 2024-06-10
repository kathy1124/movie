
from django import forms
from .models import Movie, Member_data, Session, Ticket


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
    def clean_member_pw(self):
        member_pw = self.cleaned_data.get('member_pw')
        if len(member_pw) < 6:
            raise forms.ValidationError("密碼長度不能少於6個字元")
        elif len(member_pw) >20 :
            raise forms.ValidationError("密碼長度不能超過20個字元")
        return member_pw

class MemberLoginForm(forms.Form):
    member_id = forms.CharField(label='您的帳號', max_length=50)
    member_pw = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)

class MemberForgetForm(forms.Form):
    member_id = forms.CharField(label='您的帳號', max_length=50)
    member_pw = forms.CharField(label='新密碼', widget=forms.PasswordInput)
    member_pwc = forms.CharField(label='確認新密碼', widget=forms.PasswordInput)
    def clean_member_pw(self):
        member_pw = self.cleaned_data.get('member_pw')
        if len(member_pw) < 6:
            raise forms.ValidationError("密碼長度不能少於6個字元")
        elif len(member_pw) >20 :
            raise forms.ValidationError("密碼長度不能超過20個字元")
        return member_pw
    
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
    def clean_manager_pw(self):
        manager_pw = self.cleaned_data.get('manager_pw')
        if len(manager_pw) < 6:
            raise forms.ValidationError("密碼長度不能少於6個字符")
        elif len(manager_pw) >20 :
            raise forms.ValidationError("密碼長度不能超過20個字符")
        return manager_pw
    
class ManagerLoginForm(forms.Form):
    manager_id = forms.CharField(label='您的帳號', max_length=50)
    manager_pw = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)

class ManagerForgetForm(forms.Form):
    manager_id = forms.CharField(label='您的帳號', max_length=50)
    manager_pw = forms.CharField(label='新密碼', widget=forms.PasswordInput)
    manager_pwc = forms.CharField(label='確認新密碼', widget=forms.PasswordInput)
    def clean_manager_pw(self):
        manager_pw = self.cleaned_data.get('manager_pw')
        if len(manager_pw) < 6:
            raise forms.ValidationError("密碼長度不能少於6個字元")
        elif len(manager_pw) >20 :
            raise forms.ValidationError("密碼長度不能超過20個字元")
        return manager_pw
    
class OrderTicketForm(forms.ModelForm):
    movie_name = forms.ModelChoiceField(queryset=Movie.objects.all(), label="電影名稱")
    session = forms.ModelChoiceField(queryset=Session.objects.all(), label="場次")
    ticket_amount = forms.IntegerField(min_value=1, label="票數")
    payment_method = forms.ChoiceField(choices=Ticket.CHOICES, label="付款方式")

    class Meta:
        model = Ticket
        fields = ['movie_name', 'session', 'ticket_amount', 'payment_method']
