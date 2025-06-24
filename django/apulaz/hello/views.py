from django.http import HttpResponse
 
  
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Post
from .forms import TopicForm, PostForm
from django.contrib.auth.decorators import user_passes_test
from .forms import UserEditForm
from .forms import PasswordResetForm
from django.utils import timezone
from datetime import timedelta


# Все что в решетках это админка
#######################
# Проверка, что пользователь является администратором
def is_admin(user):
    return user.is_superuser

# Получаем всех пользователей
@user_passes_test(is_admin)
def admin_utilites(request):
    
    return render(request, 'accounts/admin_utilites.html')

# Получаем всех пользователей
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all() 
    #Флаги для шаблона и их логика
    for user in users:
        if user.blocked_until and user.blocked_until > timezone.now():
            user.is_blocked = True  
        else:
            user.is_blocked = False 
    return render(request, 'accounts/admin_dashboard.html', {'users': users})

# Смена пароля
@user_passes_test(is_admin)
def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = PasswordResetForm(instance=user)
    
    return render(request, 'accounts/reset_password.html', {'form': form, 'user_obj': user})

# Функция редактирования данных пользователя
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'accounts/edit_user.html', {'form': form, 'user_obj': user})

# выдача админки
@user_passes_test(is_admin)
def grant_admin_rights(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        if user.is_superuser == True & user.is_staff == True: 
            user.is_superuser = False
            user.is_staff = False
            user.save()
            return redirect('admin_dashboard')
        
        elif user.is_superuser == False & user.is_staff == False: 
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return redirect('admin_dashboard')
    
    return render(request, 'accounts/grant_admin_rights.html', {'user_obj': user})

#Удалить аккаунт
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('admin_dashboard')

    return render(request, 'accounts/delete_user.html', {'user_obj': user})

# Логика мута
@user_passes_test(is_admin)
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        if user.is_superuser != True:
            days = int(request.POST.get('days', 0))  # Получаем количество дней блокировки из формы
            user.blocked_until = timezone.now() + timedelta(days=days)
            user.save()
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Админа замутить нельзя.')
    
    return render(request, 'accounts/block_user.html', {'user_obj': user})

# Анмут
@user_passes_test(is_admin)
def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Снимаем блокировку, если она есть
    if user.blocked_until:
        user.blocked_until = None
        user.save()
    
    return redirect('admin_dashboard')
#######################


# Регистрация
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Юзер уже зарегистрирован.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Почта уже зарегистрирован.')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'Вы успешно зарегистрировались.')
            return redirect('login')
    return render(request, 'register.html')

# Авторизация
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('forum') 
        else:
            messages.error(request, 'Неправильный юзер или пароль.')
    return render(request, 'login.html')

# Выход из системы
def logout_view(request):
    logout(request)
    return redirect('login')

# Список всех тем
@login_required(login_url='login')
def forum(request):
    topics = Topic.objects.all().order_by('-created_at')
    return render(request, 'accounts/forum.html', {'topics': topics})

# Просмотр темы и отправки сообщений в ней
@login_required(login_url='login')
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = topic.posts.all()
    #тут мут на пользовательской стороне
    if request.user.blocked_until and request.user.blocked_until > timezone.now():
        messages.error(request, 'Вы не можете отправлять сообщения до: ' + str(request.user.blocked_until))
        return redirect('forum')
    #######################
    elif request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        post_form = PostForm()

    return render(request, 'accounts/topic_detail.html', {
        'topic': topic,
        'posts': posts,
        'post_form': post_form
    })

# Создание новой темы
@login_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('forum')
    else:
        form = TopicForm()
    
    return render(request, 'accounts/create_topic.html', {'form': form})




def index(request):
    return render(request, 'accounts/index.html')
