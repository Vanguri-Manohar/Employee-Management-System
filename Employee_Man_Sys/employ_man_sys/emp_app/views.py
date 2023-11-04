from django.shortcuts import render,HttpResponse,redirect
from .models import Employee,Role,Department
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'index.html')

def all_emp(request):
    emps=Employee.objects.all()
    context={
        'emps':emps
    }
    return render(request,'all_emp.html',context=context)

def add_emp(request):
    if request.method == 'POST':
         first_name=request.POST['first_name']
         last_name =request.POST['last_name']
         dept = int(request.POST['dept'])
         salary =int(request.POST['salary'])
         bonus = int(request.POST['bonus'])
         role =int(request.POST['role'])
         phone =int(request.POST['phone'])
         new_emp=Employee(first_name=first_name,last_name =last_name,dept_id=dept,salary=salary,bonus=bonus,role_id=role,phone=phone,hire_date=datetime.now())
         new_emp.save()
         messages.success(request,"Employee Added Successfully")
         return HttpResponse("EMPLOYEE ADDED")
         
    elif request.method=='GET':
        return render(request,'add_emp.html')
    else:
        return HttpResponse('fail')
    
 
def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed=Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            messages.success(request,"Employee removed successfully")
        except:
            return HttpResponse("enter valid id")
    emps=Employee.objects.all()
    context={'emps':emps}
    return render(request,'remove_emp.html',context)

        
def filter_emp(request):
    if request.method=='POST':
        name=request.POST['name']
        dept=request.POST['dept']
        role=request.POST['role']
        emps=Employee.objects.all()
        if name:
            emps=emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps=emps.filter(dept__name__icontains=dept)
        if role:
            emps=emps.filter(role__name__icontains=role)
        context={
            'emps':emps
        }
        return render(request,'all_emp.html',context)
    elif request.method=='GET':
        return render(request,'filter_emp.html')
    else:
        return HttpResponse("Exception occured")
# def LoginUser(request):
    # if request.method=='POST':
    #     username=request.POST.get('username')
    #     password=request.POST.get('password')

    #     user=authenticate(username=username,password=password)
        
    #     if user is not None:
    #         login(request,user)
    #         return redirect("/")
    #     else:
    #         return render(request,'login.html')
    # # return render(request,'login.html')
    #  else:
    #     # Check if the user is already authenticated
    #     if request.user.is_authenticated:
    #         return redirect('logout')  # Redirect to the logout page if already authenticated

    # return render(request, 'login.html')
    
def LoginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html')
    else:
        # Check if the user is already authenticated
        if request.user.is_authenticated:
            return redirect('logout')  # Redirect to the logout page if already authenticated

    return render(request, 'login.html')
def LogoutUser(request):
    logout(request)
    return redirect("/login")

def about(request):
    return render(request,'about.html')

