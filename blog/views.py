from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, UserProfile
from .forms import UserProfileForm, PostForm, CommentForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'profile': profile, 'form': form})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def home_view(request):
    posts = Post.objects.all().order_by('-created_at')[:50]
    return render(request, 'home.html', {'posts': posts})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_profile.user.post_set.all().delete()  # Удаляем все посты автора
    user_profile.delete()
    messages.success(request, 'Профиль успешно удален!')
    return redirect('home')

# Новый код для комментариев

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # Привязываем комментарий к текущему пользователю
            comment.post = post  # Привязываем комментарий к посту
            comment.save()
            messages.success(request, 'комментарий добавлен успешно')
            return redirect('home')  # Перенаправляем на главную страницу или на страницу поста
    else:
        form = CommentForm()
    return render(request, 'create_comment.html', {'form': form, 'post': post})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')  # Получаем комментарии к посту
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Храним пароль в зашифрованном виде
            user.save()
            messages.success(request, 'Регистрация прошла успешно! Вы можете войти в систему.')
            return redirect('home')  # Перенаправление на страницу после успешной регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы вошли в систему успешно!')
            return redirect('home')  # Перенаправление на главную страницу после входа
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль.')
    return render(request, 'login.html')  # Отображение формы входа

def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('home')