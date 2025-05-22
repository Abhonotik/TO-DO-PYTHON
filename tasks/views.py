from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def todo_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        completed = request.POST.get('completed') == 'on'
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority', 0)
        
    
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            completed=completed,
            due_date=due_date or None,
            priority=int(priority)
        )
        return redirect('todo')

    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/todo.html', {'tasks': tasks})


def update_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        task.completed = request.POST.get('completed') == 'on'
        task.due_date = request.POST.get('due_date')
        task.priority = int(request.POST.get('priority', 0))
        task.save()
        return redirect('todo')
    return render(request, 'tasks/update_task.html', {'task': task})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('todo')
    return render(request, 'tasks/delete_task.html', {'task': task})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            # Form invalid - show errors
            return render(request, 'tasks/signup.html', {'form': form})
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todo')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'tasks/login.html', {
                'error': 'Invalid username or password',
                'username': username
            })
        login(request, user)
        return redirect('todo')
    return render(request, 'tasks/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'tasks/home.html')
