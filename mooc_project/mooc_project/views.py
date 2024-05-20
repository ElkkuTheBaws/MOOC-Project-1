from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Receipt, CreateUserForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import sqlite3

# A01:2021 – Broken Access Control
# Fixed by adding @login_required below
# @login_required(login_url='login/') <- Fix, remove comment
def userView(request, userId):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    # A03:2021 – Injection
    # SQL Injection is possible
    # To fix, enable the userView below
    cursor.execute("SELECT * FROM mooc_project_receipt WHERE owner_id="+str(userId))  
    receipts = map(lambda x: {'id': x[0], 'owner': x[1], 'amount': x[2], 'content': x[3]}, cursor.fetchall())
    return render(request, 'pages/user.html', {'receipts': receipts})

# Fixed userView
# @login_required(login_url='login/')
# def userView(request):
#     receipts = Receipt.objects.filter(owner=request.user)
#     return render(request, 'pages/user.html', {'receipts': receipts})


# A04:2021 – Insecure Design
# Input validation enables empty, but there is no limit.
# Logged in user can add huge amounts of data to content, eventually slowing down the service
@login_required(login_url='login/')
def addReceiptView(request):
    if request.method == 'POST':
        try:
            content: str = request.POST.get('content')
            amount: str = request.POST.get('amount')
            # A04:2021 – Insecure Design FIX
            # Remove comments -->
            #if validate_receipt(request.user, content, amount) == False:
            #     raise
            # <--
            
            # Remove following for the fix -->    
            if content == "" or amount == "" and amount.isnumeric() != True:
                raise ValidationError()
            # <--
            Receipt.objects.create(owner=request.user, content=content, amount=amount)
        except:
            print("Failed")
    return redirect('/')

# Returns true if valid
def validate_receipt(user, content: str, amount: str) -> bool:
    if content == "" or amount == "" and amount.isnumeric() != True:
        return False
    if len(content) > 1000 or len(amount) > 100:
        return False
    # Limit the maximum receipts to 10000
    if len(Receipt.objects.filter(owner=user)) > 10000:
        return False
    return True

@login_required(login_url='login/')
def deleteReceiptView(request):
    if request.method == 'POST':
        try:
            receipt = Receipt.objects.get(pk=request.POST.get('id'), owner=request.user)
            receipt.delete()
        except:
            pass
    return redirect('/')

# A03:2021 – Injection
# SQL Injection is possible
@login_required(login_url='login/')
def landingView(request):
    userId = request.user.id
    return redirect(f'user/{userId}')
    
# FIX 
# @login_required(login_url='login/')
# def landingView(request):
#    return redirect('user/')



def createUserView(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # A07:2021 – Identification and Authentication Failures
            # No weak password check
            # FIX -->
            # try:
            #     validate_password(form.cleaned_data['password'])
            # except ValidationError:
            #     form.add_error('password', 'Weak or incorrect password')
            #     return render(request, 'pages/create.html', {'form': form}) 
            # -->
            if len(User.objects.filter(username=username)) != 0:
                form.add_error('username', 'Username already in use')
                return render(request, 'pages/create.html', {'form': form}) 
            
            User.objects.create_user(username, email, password)
            return redirect('/')
        else:
            return render(request, 'pages/create.html', {'form': form}) 
        
    form = CreateUserForm(None)
    return render(request, 'pages/create.html', {'form': form}) 
