from django.shortcuts import render

def index(request):
    return render(request, "index.html") 

def admin_menu(request):
    return render(request, "admin.html")