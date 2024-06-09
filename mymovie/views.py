from .filters import MovieFilter, MemberFilter, MovieTypeFilter
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404, redirect, render
from .models import Member_data, Ticket, Movie, Staff_data, Session
from .forms import MovieForm, MemberEditForm, MemberRegisterForm, MemberLoginForm, MemberForgetForm, ManagerRegisterForm, ManagerLoginForm, ManagerForgetForm, OrderForm
from django.contrib.auth import logout
from django.http import JsonResponse

# 首頁


def home(request):
    return redirect('/movieInformation/')

# -------------------------------------------------------------------------------------------------------------
# Manager
# 註冊
def registerManager(request):
    CHOICES = (
        ('it', 'IT部門'),
        ('hr', '人事部門')
    )
    message = ""
    if request.method == 'POST':
        register_form = ManagerRegisterForm(request.POST)
        if register_form.is_valid():
            manager_id = register_form.cleaned_data['manager_id'].strip()
            manager_name = register_form.cleaned_data['manager_name']
            manager_department = register_form.cleaned_data['manager_department']
            manager_pw = register_form.cleaned_data['manager_pw']
            manager_pwc = register_form.cleaned_data['manager_pwc']

            if manager_pw == manager_pwc:
                if not Staff_data.objects.filter(staff_account=manager_id).exists():
                    pw = make_password(manager_pw)
                    manager = Staff_data.create_manager_data(
                        manager_id, pw, manager_department, manager_name)
                    manager.save()
                    message = "註冊成功! 請點選「帳號中心」進行登入"
                    return redirect('/loginManager/')
                else:
                    message = "帳號已經存在"
            else:
                message = "密碼不一致"
        else:
            message = "請檢查輸入的欄位內容"
    else:
        register_form = ManagerRegisterForm()
    return render(request, 'manager_register.html', {'form': register_form, 'message': message, 'CHOICES': CHOICES})

# 登入
def loginManager(request):
    message=""
    if request.method == 'GET':
        form = ManagerLoginForm()
        next_url = request.GET.get('next', '/accountCenter/')
        return render(request, 'manager_login.html', {'form': form, 'next': next_url})

    elif request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        next_url = request.POST.get('next', '/accountCenter/')
        if form.is_valid():
            manager_id = form.cleaned_data['manager_id'].strip()
            manager_pw = form.cleaned_data['manager_pw']
            print(f'manager_id:{manager_id}, password: {manager_pw}')
            try:
                manager = Staff_data.objects.get(staff_account=manager_id)
                if check_password(manager_pw, manager.staff_password):
                    request.session['manager_id'] = manager_id
                    message = '成功登入了'
                    return redirect(next_url)
                else:
                    message = '登入失敗'
            except Staff_data.DoesNotExist:
                message = '沒有此帳號'
        else:
            print(form.errors)
            message = '表單內容有誤: {}'.format(form.errors)
        return render(request, 'manager_login.html', {'form': form, 'message': message, 'next': next_url})
    else:
        message = '錯誤的請求方法'
    return render(request, 'manager_login.html', locals())

# 忘記密碼


def forgetManager(request):
    if request.method == 'POST':
        form = ManagerForgetForm(request.POST)
        if form.is_valid():
            manager_id = form.cleaned_data['manager_id'].strip()
            manager_pw = form.cleaned_data['manager_pw']
            manager_pwc = form.cleaned_data['manager_pwc']
            if manager_pw == manager_pwc:
                try:
                    manager = Staff_data.objects.get(staff_account=manager_id)
                    manager.staff_password = make_password(manager_pw)
                    manager.save()
                    return redirect('/loginManager/')
                    # return redirect('/loginMember/')
                except Staff_data.DoesNotExist:
                    message = "此帳號不存在"
            else:
                message = "新密碼與確認新密碼不一致"
        else:
            message = "表單內容有誤"
        return render(request, 'manager_forget.html', {'form': form, 'message': message})
    else:
        form = ManagerForgetForm()
    return render(request, 'manager_forget.html', locals())

# 登出


def logout_view2(request):
    logout(request)
    return redirect('/loginManager/')

# 帳號中心


def accountCenter(request):
    try:
        manager_id = request.session.get('manager_id')
        if not manager_id:
            return redirect('/loginManager/')

        staff = Staff_data.objects.get(staff_account=manager_id)
        return render(request, 'manager_accountCenter.html', locals())
    except Staff_data.DoesNotExist:
        return redirect('/loginManager/')


# 新增電影
def addMovie(request):
    CHOICES = [
        ('coming_soon', '即將上映'),
        ('showing', '現正熱映'),
    ]
    if 'manager_id' not in request.session:
        return redirect(f'/loginManager/?next={request.path}')

    if request.method == 'POST':
        movie_no = request.POST.get('movie_no')
        movie_name = request.POST.get('movie_name')
        date = request.POST.get('date')
        show = request.POST.get('show')
        director = request.POST.get('director')
        actor = request.POST.get('actor')
        type = request.POST.get('type')
        length = request.POST.get('length')
        picture = request.POST.get('picture')
        staff_data_instance = Staff_data.objects.get(staff_no=1)
        movie = Movie.objects.create(
            movie_no=movie_no,
            movie_name=movie_name,
            date=date,
            show=show,
            director=director,
            actor=actor,
            type=type,
            length=length,
            picture=picture,
            change_staff=staff_data_instance
        )
        return redirect('addSession')
    else:
        return render(request, 'manager_addMovie.html', {'CHOICES': CHOICES})



# 新增場次


def addSession(request):
    if 'manager_id' not in request.session:
        return redirect(f'/loginManager/?next={request.path}')
    if request.method == 'POST':
        movie_id = request.POST['movie']
        session_desc = request.POST['session']
        movie = get_object_or_404(Movie, pk=movie_id)
        session = Session(movie=movie, session=session_desc)
        session.save()
        return redirect('showMovie', movie_no=movie.pk)
    else:
        movies = Movie.objects.all()
        return render(request, 'manager_addSession.html', {'movies': movies})


# 刪除電影


def deleteMovie(request, movie_no):
    if 'manager_id' not in request.session:
        return redirect(f'/loginManager/?next={request.path}')
    if movie_no:
        try:
            movie = Movie.objects.get(movie_no=movie_no)
            movie.delete()
        except:
            pass
    return redirect('searchMovie')
# 編輯電影


def editMovie(request, movie_no):
    if 'manager_id' not in request.session:
        return redirect(f'/loginManager/?next={request.path}')
    movie_instance = get_object_or_404(Movie, movie_no=movie_no)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie_instance)
        if form.is_valid():
            form.save()
            return redirect('showMovie', movie_no=movie_instance.movie_no)
    else:
        form = MovieForm(instance=movie_instance)
    context = {
        'form': form,
        'movie_instance': movie_instance,
    }
    return render(request, 'manager_editMovie.html', context)


# 搜尋電影


def searchMovie(request):
    if 'manager_id' not in request.session:
        return redirect(f'/loginManager/?next={request.path}')
    movies = Movie.objects.all()
    movieFilter = MovieFilter(request.GET, queryset=movies)
    context = {
        'movieFilter': movieFilter
    }
    return render(request, 'manager_searchMovie.html', context)

# 顯示電影


def showMovie(request, movie_no):
    if 'manager_id' not in request.session:
        return redirect(f'/loginManager/?next={request.path}')
    movie = Movie.objects.get(movie_no=movie_no)
    ses = Session.objects.filter(movie=movie_no)
    return render(request, 'manager_showMovie.html', locals())

# 會員購票紀錄


def search_member_info(member_no):
    try:
        member = Member_data.objects.get(member_no=member_no)
        tickets = Ticket.objects.filter(ticket_member=member)
        result = {
            'member_account': member.member_account,
            'gmail': member.gmail,
            'phone_number': member.phone_number,
            'tickets': [],
        }
        payment_method_display = {
            'money': '現金',
            'credit_card': '信用卡'
        }
        for ticket in tickets:
            session = Session.objects.get(pk=ticket.session_id_id)
            movie = session.movie
            result['tickets'].append({
                'session': session.session,
                'movie_name': movie.movie_name,
                'ticket_amount': ticket.ticket_amount,
                'payment_method': payment_method_display.get(ticket.payment_method, ticket.payment_method)
            })
        return result
    except Member_data.DoesNotExist:
        return None


def searchTicket(request):
    if 'manager_id' not in request.session:
        return redirect(f'/loginManager/?next={request.path}')
    member_info = None
    if request.method == 'POST':
        member_no = request.POST.get('member_no')
        if member_no:
            member_info = search_member_info(member_no)
    return render(request, 'manager_searchTicket.html', {'member_info': member_info})

# 會員資料


def searchMember(request):
    member_info = None
    if request.method == 'POST':
        member_no = request.POST.get('member_no')
        if member_no:
            member_info = search_member_info(member_no)
    return render(request, 'manager_searchMember.html', locals())

# ---------------------------------------------------------------------------------------------------------------
# User
# 註冊
def registerMember(request):
    message=""
    if request.method == 'POST':
        register_form = MemberRegisterForm(request.POST)
        if register_form.is_valid():
            member_id = register_form.cleaned_data['member_id'].strip()
            member_pw = register_form.cleaned_data['member_pw']
            member_pwc = register_form.cleaned_data['member_pwc']
            member_mail = register_form.cleaned_data['member_mail']
            member_phone = register_form.cleaned_data['member_phone']

            if member_pw == member_pwc:
                if not Member_data.objects.filter(member_account=member_id).exists():
                    pw = make_password(member_pw)
                    member = Member_data.create_member_data(member_id, pw, member_mail, member_phone)
                    member.save()
                    return redirect('/loginMember/')
                else:
                    message = "帳號已經存在"
            else:
                message = "密碼不一致"
        else:
            message = "請檢查輸入的欄位內容"
    else:
        register_form = MemberRegisterForm()
    return render(request, 'user_register.html', {'form': register_form, 'message': message})

# 登入會員
def loginMember(request):
    message=""
    if request.method == 'GET':
        form = MemberLoginForm()
        return render(request, 'user_login.html', {'form': form})

    elif request.method == 'POST':
        form = MemberLoginForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data['member_id'].strip()
            member_pw = form.cleaned_data['member_pw']
            try:
                member = Member_data.objects.get(member_account=member_id)
                if check_password(member_pw, member.member_password):
                    request.session['member_id'] = member_id
                    message = '成功登入了'
                    return redirect('/lookMember/')
                else:
                    message = '登入失敗'
            except Member_data.DoesNotExist:
                message = '沒有此帳號'
        else:
            message = '表單內容有誤'
        return render(request, 'user_login.html', {'form': form, 'message': message})
    else:
        message = '錯誤的請求方法'
    return render(request, 'user_login.html', {'form': form, 'message': message})

# 忘記密碼


def forgetMember(request):
    if request.method == 'POST':
        form = MemberForgetForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data['member_id'].strip()
            member_pw = form.cleaned_data['member_pw']
            member_pwc = form.cleaned_data['member_pwc']
            if member_pw == member_pwc:
                try:
                    member = Member_data.objects.get(member_account=member_id)
                    member.member_password = make_password(member_pw)
                    member.save()
                    return redirect('/loginMember/')
                except Member_data.DoesNotExist:
                    message = "帳號不存在"
            else:
                message = "新密碼與確認新密碼不一致"
        else:
            message = "表單內容有誤"
        return render(request, 'user_forget.html', {'form': form, 'message': message})
    else:
        form = MemberForgetForm()
    return render(request, 'user_forget.html', {'form': form})

# 登出


def logout_view(request):
    logout(request)
    return redirect('/loginMember/')

# 電影資訊
def movieInformation(request):
    movies = Movie.objects.all()
    movieTypeFilter = MovieTypeFilter(request.GET, queryset=movies)

    if movieTypeFilter.qs:
        movies = movieTypeFilter.qs

    coming_soon_movies = movies.filter(show='coming_soon')
    showing_movies = movies.filter(show='showing')
    removed_movies = movies.filter(show='removed')

    context = {
        'movieTypeFilter': movieTypeFilter,
        'coming_soon_movies': coming_soon_movies,
        'showing_movies': showing_movies,
        'removed_movies': removed_movies,
    }
    return render(request, 'user_movieInformation.html', context)


def movieInformationDetails(request, movie_id):
    movies = Movie.objects.get(movie_no=movie_id)
    sessions = Session.objects.filter(movie=movie_id)
    context = {
        'movies': movies,
        'sessions': sessions,
    }
    return render(request, 'user_movieInformationDetails.html', context)

def orderTicket(request):
    if 'member_id' not in request.session:
        return redirect(f'/loginMember/?next={request.path}')
    member_info = None
    if request.method == 'POST':
        member_no = request.POST.get('member_no')
        if member_no:
            member_info = search_member_info(member_no)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            # Assuming you have a way to get the current member
            ticket.ticket_member = request.user.member_data
            ticket.ticket_amount = form.cleaned_data['ticket_quantity']
            ticket.save()
            return redirect('orderTicketRecord')
    else:
        form = OrderForm()
    return render(request, 'user_orderTicket.html', {'form': form})

def orderTicketRecord(request):
    return render(request, 'user_orderTicketRecord.html')

def get_sessions(request):
    movie_id = request.GET.get('movie_id')
    sessions = Session.objects.filter(movie_id=movie_id).order_by('session')
    session_options = '<option value="">請選擇電影場次</option>'
    for session in sessions:
        session_options += f'<option value="{session.pk}">{session.session}</option>'
    return JsonResponse(session_options, safe=False)


# def orderTicketConfirm(request):
#     return render(request, 'user_orderTicketConfirm.html', locals())


# def orderTicketRecord(request):
#     return render(request, 'user_orderTicketRecord.html', locals())

# 查看會員資訊


def lookMember(request):
    try:
        member_id = request.session.get('member_id')
        if not member_id:
            return redirect('/loginMember/')

        member = Member_data.objects.get(member_account=member_id)
        return render(request, 'user_lookMember.html', {'member': member})
    except Member_data.DoesNotExist:
        return redirect('/loginMember/')

# 編輯會員


def editMember(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('/loginMember/')

    try:
        member = Member_data.objects.get(member_account=member_id)
    except Member_data.DoesNotExist:
        return redirect('/loginMember/')

    if request.method == 'POST':
        form = MemberEditForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/lookMember/')
    else:
        form = MemberEditForm(instance=member)
    return render(request, 'user_editMember.html', {'form': form})

# 聯絡我們
def contact(request):
    return render(request, "user_contactUs.html", locals())
