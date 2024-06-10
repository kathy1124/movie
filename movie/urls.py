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
    # 登出


    # -----------------------------------------------------------
    # Manager
    # 電影處理
    path('addMovie/', mv.addMovie, name='addMovie'),
    path('addSession/', mv.addSession, name='addSession'),
    path('editMovie/<int:movie_no>/', mv.editMovie, name='editMovie'),
    path('deleteMovie/<int:movie_no>/', mv.deleteMovie, name='deleteMovie'),
    path('searchMovie/', mv.searchMovie, name='searchMovie'),
    path('searchMovie/<int:movie_no>/', mv.showMovie, name='showMovie'),

    # 會員購票紀錄
    path('searchTicket/', mv.searchTicket, name='searchTicket'),

    # 搜尋會員資料
    path('searchMember/', mv.searchMember, name='searchMember'),

    # 員工登入註冊忘記密碼登出
    path('registerManager/', mv.registerManager, name='registerManager'),
    path('loginManager/', mv.loginManager, name='loginManager'),
    path('forgetManager/', mv.forgetManager, name='forgetManager'),
    path('logout2/', mv.logout_view2, name='logout2'),

    # 員工帳號中心
    path('accountCenter/', mv.accountCenter, name='accountCenter'),
    # -----------------------------------------------------------
    # User
    # 電影資訊
    path('movieInformation/', mv.movieInformation, name='movieInformation'),
    path('movieInformation/<int:movie_id>',
         mv.movieInformationDetails, name='movieInformationDetails'),

    #聯絡我們 聯絡資訊
    path('contactUs',mv.contact,name='contactUs'),
    path('contactInfo',mv.contact,name='contactInfo'),

    # 登入註冊忘記密碼登出
    path('registerMember/', mv.registerMember, name='registerMember'),
    path('loginMember/', mv.loginMember, name='loginMember'),
    path('forgetMember/', mv.forgetMember, name='forgetMember'),
    path('logout/', mv.logout_view, name='logout'),

    # 快速購票
    path('orderTicket/', mv.orderTicket, name='orderTicket'),
    # path('orderTicketConfirm/', mv.orderTicketConfirm, name='orderTicketConfirm'),
    path('orderTicketRecord/', mv.orderTicketRecord, name='orderTicketRecord'),
	path('get_sessions/', mv.get_sessions, name='get_sessions'),

    # 會員中心
    path('lookMember/', mv.lookMember, name='lookMember'),
    path('editMember/', mv.editMember, name='editMember'),

]
