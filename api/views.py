from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    if request.method == 'POST':
        return HttpResponse('login')

def register(request):
    if request.method == 'POST':
        return HttpResponse('register')

def item(request, item_id):
    if request.method == 'GET':
        return HttpResponse(f'item details: {item_id}')

def shopping(request):
    if request.method == 'GET':
        return HttpResponse('all items')

def sale(request):
    if request.method == 'GET':
        return HttpResponse('sale items')

def shopping_basket(request):
    if request.method == 'GET':
        return HttpResponse('look at basket')

    if request.method == 'POST':
        return HttpResponse('basket add')

    if request.method == 'DELETE':
        return HttpResponse('basket delete')

def checkout(request):
    if request.method == 'POST':
        return HttpResponse('checkout')
