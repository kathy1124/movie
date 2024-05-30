"""
URL configuration for movie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mymovie import views as mv


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mv.home, name='home'),
    # 註冊、登入、忘記密碼
    path('registerMember/',mv.registerMember, name='registerMember'),
    path('loginMember/',mv.loginMember, name='loginMember'),
    path('forgetMember/',mv.forgetMember, name='forgetMember'),
    path('logout/',mv.logout_view, name='logout'),
    path('lookMember/',mv.lookMember, name='lookMember'),

    #-----------------------------------------------------------
    # Manager
    # 電影處理
    path('addMovie/',mv.addMovie , name='addMovie'),
    path('addSession/', mv.addSession, name='addSession'),
    path('editMovie/<int:movie_no>/', mv.editMovie, name='editMovie'),
    path('deleteMovie/<int:movie_no>/',mv.deleteMovie , name='deleteMovie'),
    path('searchMovie/',mv.searchMovie , name='searchMovie'),
    path('searchMovie/<int:movie_no>/',mv.showMovie , name='showMovie'),

    # 會員購票紀錄
    path('searchTicket/',mv.searchTicket , name='searchTicket'),

    # 會員資料
    path('searchMember/',mv.searchMember, name='searchMember'),
    path('searchMemberDetails/',mv.searchMemberDetails, name='searchMemberDetails'),
    
    #登入註冊忘記密碼
    path('registerMember/',mv.registerMember, name='registerMember'),
    path('loginMember/',mv.loginMember, name='loginMember'),
    path('forgetMember/',mv.forgetMember, name='forgetMember'),



    #-----------------------------------------------------------
    # User
    # 電影資訊
	# path('movieInformation/',mv.movieInformation, name='movieInformation'),

    

    # 快速購票
    # path('orderTicket/',mv.orderTicket, name='orderTicket'),
    # path('orderTicketConfirm/',mv.orderTicketConfirm, name='orderTicketConfirm'),
    # path('orderTicketRecord/',mv.orderTicketRecord, name='orderTicketRecord'),

    # 會員中心
    path('lookMember/', mv.lookMember, name='lookMember'),
    path('editMember/', mv.editMember, name='editMember'),
    # path('/',mv. , name=''),
]
