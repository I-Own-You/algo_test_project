from django.shortcuts import render, redirect

from products.serializers import CarSerializer
from .forms import UserRegisterForm
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def user_list_api(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def user_detail_api(request, pk):

    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)



def register_user(request):

    if request.user.is_authenticated:
        return redirect('products')
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                first_name=form.cleaned_data['first_name'].lower(
                ).capitalize(),
                last_name=form.cleaned_data['last_name'].lower().capitalize(),
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                return redirect('products')

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def login_user(request):

    if request.user.is_authenticated:
        return redirect('products')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('products')
        else:
            messages.error(request, 'Не верный пароль или e-mail')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

