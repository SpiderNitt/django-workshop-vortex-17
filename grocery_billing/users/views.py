from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import Employee
from django.contrib.auth.models import User
# Create your views here.

def register(request):
    success = -1
    auth = -1
    if request.method == 'POST':
        uname = request.POST.get('username','default')
        name = request.POST.get('name','default')
        pwd = request.POST.get('password','default')
        pwdcnf = request.POST.get('pwdcnf','default')
        optradio = request.POST.get('option_hidden','none')
        if pwd != pwdcnf:
            success = 0
        else:
            try:
                u = User.objects.get(username=uname)
                if u is not None:
                    success = 2
            except User.DoesNotExist:    
                success = 1
                u = User()
                u.username = uname
                u.set_password(pwd)
                u.save()
                e = Employee()
                e.user = u
                e.name = name
                e.pos = optradio
                e.save()
    return render(request,"index.html",{'auth' : auth, 'success' : success}) 
    
def login_view(request):
    auth = -1
    success = -1
    if request.method == 'POST':
        uname = request.POST.get('login_username','default')
        upwd = request.POST.get('login_password','default')
        user = authenticate(username=uname, password=upwd)
        if user is not None:
            login(request,user)
            return redirect('/users/dashboard')
        else:
            auth = -2
    return render(request,"index.html", {'auth' : auth, 'success' : success })
    
def dashboard(request):
    if request.user.is_authenticated():
        try:
            e = Employee.objects.get(user=request.user)
            if e.pos == 'C':
                return render(request,"cashier_dashboard.html",{'emp' : e, 'range' : range(1,3) })
            else:
                return render(request,"search.html",{'emp' : e })
        except Employee.DoesNotExist:
            print request.user.username
            return redirect('/users/logout')
    else:
        return HttpResponse('Please provide your credentials')

def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('/users/login')
    else:
        return HttpResponse('Please provide your credentials')
        
