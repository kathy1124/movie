from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# ⭐ 修改 models.py 要在 cmd 輸入 python manage.py makemigrations 、 python manage.py migrate ⭐
#----------------------------------------------------------------------------------------------------------------------
# 會員個人資料
class Member_data(models.Model):
    member_no = models.AutoField(primary_key=True)
    member_account = models.CharField(max_length=25, unique=True)
    member_password = models.CharField(max_length=25)
    gmail = models.EmailField()
    phone_number = models.CharField(max_length=15)
    
    @classmethod
    def create_member_data(cls, member_account, member_password, gmail, phone_number):
        member = cls(
            member_account=member_account,
            member_password=member_password,
            gmail=gmail,
            phone_number=phone_number,
        )
        return member
    
    def __str__(self):
        return self.member_account
# 在 Django 管理介面中查看Member_data時，以 member_account 的值作為 Member_data 的字串表示形式，而不是預設的模型名稱和物件ID。
#----------------------------------------------------------------------------------------------------------------------
# 場次
class Session(models.Model):
    session_no = models.AutoField(primary_key=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    session = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.movie.movie_name} - {self.session}"
#----------------------------------------------------------------------------------------------------------------------
# 訂票紀錄
class Ticket(models.Model):
    CHOICES = (
        ('money', '現金'),
        ('credit_card', '信用卡')
    )
    ticket_no = models.AutoField(primary_key=True)
    ticket_member = models.ForeignKey('Member_data',on_delete=models.CASCADE )   # 删除了一个 Member_data 的資料，所有和 member 有關的紀錄也會删除
    session_id = models.ForeignKey('Session',on_delete=models.CASCADE)
    ticket_amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=100, choices=CHOICES)
#----------------------------------------------------------------------------------------------------------------------
# 電影資訊
class Movie(models.Model):
    CHOICES = (
        ('coming_soon', '即將上映'),
        ('showing', '現正熱映'),
        ('removed','下架電影')
    )
    movie_no = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=200)
    date = models.DateField()
    show = models.CharField(max_length=20, choices=CHOICES)
    director = models.CharField(max_length=20)
    actor = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    length = models.CharField(max_length=100)
    picture = models.CharField(max_length=500)
    change_staff = models.ForeignKey('Staff_data', on_delete=models.CASCADE)
    def __str__(self):
        return self.movie_name
#----------------------------------------------------------------------------------------------------------------------
# 員工資料
class Staff_data(models.Model):
    CHOICES = (
        ('it', 'IT部門'),
        ('hr', '人事部門')
    )
    staff_no = models.AutoField(primary_key=True)
    staff_account = models.CharField(max_length=25 , unique=True)
    staff_password = models.CharField(max_length=200)
    staff_name = models.CharField(max_length=25)
    staff_department = models.CharField(max_length=200, choices=CHOICES)

    @classmethod
    def create_manager_data(cls, staff_account, staff_password, staff_department, staff_name):
        member = cls(
            staff_account=staff_account,
            staff_password=staff_password,
            staff_department=staff_department,
            staff_name=staff_name,

        )
        return member
    
    def __str__(self):
        return self.staff_name
