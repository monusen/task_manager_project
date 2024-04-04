from django.shortcuts import render, redirect
from django.http import HttpResponse
from openpyxl import Workbook
from .forms import UserForm, TaskForm
from .models import User, Task

def index(request):
    return render(request,'index.html')
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def export_to_excel(request):
    users = User.objects.all()
    tasks = Task.objects.all()

    wb = Workbook()
    ws_users = wb.active
    ws_users.title = "Users"
    ws_tasks = wb.create_sheet(title="Tasks")

    ws_users.append(["Name", "Email", "Mobile"])
    for user in users:
        ws_users.append([user.name, user.email, user.mobile])

    ws_tasks.append(["Detail", "Task Type", "Assigned To"])
    for task in tasks:
        ws_tasks.append([task.detail, task.task_type, task.assigned_to.name])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=task_manager_data.xlsx'
    wb.save(response)

    return response
