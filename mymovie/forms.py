
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
        if len(member_pw) < 8:
            raise forms.ValidationError("密碼長度不能少於8個字元")
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
        if len(member_pw) < 8:
            raise forms.ValidationError("密碼長度不能少於8個字元")
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
        if len(manager_pw) < 8:
            raise forms.ValidationError("密碼長度不能少於8個字符")
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
        if len(manager_pw) < 8:
            raise forms.ValidationError("密碼長度不能少於8個字元")
        elif len(manager_pw) >20 :
            raise forms.ValidationError("密碼長度不能超過20個字元")
        return manager_pw
    
class OrderForm(forms.ModelForm):
    movie = forms.ModelChoiceField(queryset=Movie.objects.all(), label="電影名稱", empty_label="請選擇電影")
    session = forms.ModelChoiceField(queryset=Session.objects.none(), label="電影場次", empty_label="請先選擇電影")
    ticket_quantity = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 11)], label="票卷張數")
    PAYMENT_CHOICES = [
        ('money', '現金'),
        ('credit_card', '信用卡')
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, label="付款方式")

    class Meta:
        model = Ticket
        fields = ['session_id', 'ticket_amount', 'payment_method']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['session'].queryset = Session.objects.none()

        if 'movie' in self.data:
            try:
                movie_id = int(self.data.get('movie'))
                self.fields['session'].queryset = Session.objects.filter(movie_id=movie_id).order_by('session')
            except (ValueError, TypeError):
                self.fields['session'].queryset = Session.objects.none()
        elif self.instance and self.instance.pk:
            self.fields['session'].queryset = self.instance.movie.session_set.order_by('session')
