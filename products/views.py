from math import prod
from django.http import HttpResponse
from django.shortcuts import render, redirect

from products.serializers import CarSerializer, ImagesSerializer
from .models import Car, Images
from .forms import AddEditProductForm,  CarImageFormSet
from users.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'products': reverse('car-list', request=request, format=format),
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def products_list(request):
    if request.method == 'GET':
        products = Car.objects.all()
        serializer = CarSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_detail(request, pk):
    try:
        product = Car.objects.get(id=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method in 'PUT DELETE' and request.user.email != product.owner.email:
        raise PermissionDenied('Error - This item doesn\'t belong to you')

    elif request.method == 'GET':
        serializer = CarSerializer(product, context={'request': request})
        return Response(serializer.data)


    elif request.method == 'PUT':
        serializer = CarSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def images_detail(request,pk):
    imgs = Images.objects.get(id=pk)
    if request.method == 'GET':
        serializer = ImagesSerializer(imgs, context={'request': request})
        return Response(serializer.data)


@login_required(login_url='login')
def products(request):
    cars = Car.objects.all()

    if request.method == 'GET' and request.GET.get('search'):
        search_txt = request.GET.get('search')
        match search_txt:
            case 'Искать по алфавиту':
                cars = Car.objects.order_by('name')

            case 'От минимлаьной цены вверх':
                cars = Car.objects.order_by('price')

            case 'От максимальной цены вниз':
                cars = Car.objects.order_by('-price')

            case _:
                cars = Car.objects.filter(name__contains=search_txt)

    paginator = Paginator(cars, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        # 'cars': cars
        'page_obj': page_obj,
    }

    return render(request, 'products.html', context)


@login_required(login_url='login')
def single_product(request, id):

    car = Car.objects.get(id=id)
    images = Images.objects.filter(owner=car)
    context = {
        'car': car,
        'images': images,
    }
    return render(request, 'single_product.html', context)


@login_required(login_url='login')
def add_product(request):
    form = AddEditProductForm()
    form_images = CarImageFormSet()
    if request.method == 'POST':
        form = AddEditProductForm(request.POST)
        if form.is_valid():
            car_obj = Car.objects.create(
                owner=User.objects.get(email=request.user),
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
            )
            if request.FILES:
                for key in request.FILES:
                    img_files = request.FILES.getlist(key)
                    for file in img_files:
                        Images.objects.create(owner=Car.objects.get(id=car_obj.id), images=file)
            else:
                Images.objects.create(owner=Car.objects.get(id=car_obj.id))

            return redirect('products')
    context = {
        'form': form,
        'form_images': form_images,
    }
    return render(request, 'add_product.html', context)


@login_required(login_url='login')
def edit_product(request, id):


    car = Car.objects.get(id=id)
    if request.user != car.owner:
        return redirect('products')

    data = {
        'name': car.name,
        'description': car.description,
        'price': car.price,
    }
    form_images = CarImageFormSet()
    form = AddEditProductForm(data)
    if request.method == 'POST':
        form = AddEditProductForm(request.POST, request.FILES)
        if form.is_valid():
            car.name = form.cleaned_data.get('name')
            car.description = form.cleaned_data.get('description')
            car.price = form.cleaned_data.get('price')
            car.save()

            for key in request.FILES:
                img_files = request.FILES.getlist(key)
                for file in img_files:
                    Images.objects.create(owner=Car.objects.get(id=car.id), images=file)


            return redirect('products')

    context = {
        'form': form,
        'car': car,
        'form_images': form_images,
    }

    return render(request, 'edit_product.html', context)


@login_required(login_url='login')
def remove_product(request, id):
    car = Car.objects.get(id=id)

    if request.method == 'GET':
        car.delete()
        return redirect('products')

    context = {
        'car': car
    }

    return render(request, 'remove_product.html', context)
