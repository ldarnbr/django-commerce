from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Item, ShoppingBasket, BasketItem, Order, OrderItem
import json
# Lecture 6 on Django
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth

# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Check the customers credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Credentials matched so set up their login session.
            auth(request, user)
            return JsonResponse({
                'message': f'{username} Logged in successfully.'
            })
        else:
            return JsonResponse({
                'error': 'Invalid Username or Password.'
            }, status=400)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Web form will make these required fields but just incase as a security measure i'll check here too.
        if not username:
            return JsonResponse({
                'error': 'Username required'
            }, status=400)

        if not password:
            return JsonResponse({
                'error': 'Password required'
            }, status=400)

        # Check username doesn't exist already
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'error': 'Username taken.'
            }, status=400)

        user = User.objects.create_user(username=username, password=password)

        # Create a shopping basket for the new user by default.
        ShoppingBasket.objects.create(customer=user)

        # Also log the user in immediately.
        auth(request, user)
        
        return JsonResponse({'message': f'Account created, welcome to the platform {username}!'})

def item(request, item_id):
    if request.method == 'GET':

        item = Item.objects.get(id=item_id)

        item_details = {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'stock_count': item.stock_count,
            'price': str(item.price),
            'sale_discount': str(item.sale_discount)
        }

        return JsonResponse(item_details)

# Search functionality is bundled in this endpoint.
def shopping(request):
    if request.method == 'GET':

        item_data = []

        # https://learndjango.com/tutorials/django-search-tutorial
        # Checks for search terms in the URL itself and then filters based on this.
        # Limited to only search for exact terms in the order they appear.
        if 'search' in request.GET:
            # Reads the value of search variable in the dictionary from Django.
            term = request.GET['search']
            # Filtering based on method in learndjango source above.
            items = Item.objects.filter(name__icontains=term)
        else:
            items = Item.objects.all()

        for item in items:
            item_data.append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'stock_count': item.stock_count,
                # Django's Decimals aren't suitable for JSON, so it's converted to string.
                'price': str(item.price),
                'sale_discount': str(item.sale_discount)
            })

        # https://www.stanza.dev/courses/django-rest-api/api-fundamentals/django-rest-api-json-responses
        # Returning non-dict value so safe=False bypasses JSON protections.
        return JsonResponse(item_data, safe=False)

def sale(request):
    if request.method == 'GET':

        # Filter all items and return those with a discount only.
        sale_items = Item.objects.filter(sale_discount__gt=0)

        item_data = []
        for item in sale_items:
            item_data.append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'stock_count': item.stock_count,
                'price': str(item.price),
                'sale_discount': str(item.sale_discount)
            })
        return JsonResponse(item_data, safe=False)

# https://stackoverflow.com/questions/36147597/adding-items-to-shopping-cart-django-python
# Idea to require login before adding to cart adapted from the above source.
# After clicking add to basket, need to either make a new cart or add it to existing one pertaining
# to the logged in user.
@csrf_exempt
def shopping_basket(request):

    # Need to login before seeing basket.
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Please login to view or add items to basket.'}, status=401)

    # Get the basket for the logged in user.
    basket, basket_created = ShoppingBasket.objects.get_or_create(customer=request.user)
    
    if request.method == 'GET':
        # Grab all items pertaining to the current basket.
        basket_items = BasketItem.objects.filter(basket=basket)

        basket_data = []

        for basket_item in basket_items:
            basket_data.append({
                'item_id': basket_item.item.id,
                'name': basket_item.item.name,
                'quantity': basket_item.quantity,
                'price': str(basket_item.item.price),
                'sale_discount': str(basket_item.item.sale_discount)
            })

        return JsonResponse(basket_data, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']

        # Check if the item is available in the database, if not return 404.
        item_request = get_object_or_404(Item, id=item_id)

        # Create the basket item if its not already in the users basket.
        basket_item, basket_item_created = BasketItem.objects.get_or_create(
            basket=basket,
            item=item_request,
            defaults={'quantity': 0}
        )

        # Must check existing basket items against stock to check order can be fulfilled.
        if basket_item.quantity + 1 > item_request.stock_count:
            return JsonResponse({
                'error': f'Maximum quantity reached.'
            }, status=400)

        # Increment the quantity in the database and save it.
        basket_item.quantity += 1
        basket_item.save()

        return JsonResponse({
            'message': f'Added {item_request.name} to the basket.',
            'quantity': basket_item.quantity
        })

    if request.method == 'DELETE':
        data = json.loads(request.body)
        item_id = data['item_id']

        # Find the item in the basket (if it exists).
        basket_item = BasketItem.objects.filter(basket=basket, item_id=item_id).first()

        if not basket_item:
            return JsonResponse({'error': 'Item not found to delete.'}, status=404)

        # Handles quantity reduction instead of entire removal from basket.
        # Would benefit from being a separate action so customer can completely
        # get rid of an item in the basket rather than one at a time.
        if basket_item.quantity > 1:
            basket_item.quantity -= 1
            basket_item.save()
            return JsonResponse({
                'message': 'Quantity Reduced.'
            })
        else:
            basket_item.delete()
            return JsonResponse({
                'message': 'Item removed from basket.'
            })

@csrf_exempt
def checkout(request):
    if request.method == 'POST':

        # Need to make sure user is logged in first.
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'You must login to checkout.'}, status=401)

        # Check basket exists for customer.
        basket = ShoppingBasket.objects.filter(customer=request.user).first()

        # Throw error when basket doesn't exist but user tries to check out.
        if not basket:
            return JsonResponse({
                'error': 'No basket created. Please add items to basket before checking out.'
            }, status=400)

        basket_items = BasketItem.objects.filter(basket=basket)

        # Check items are present in the created basket.
        if not basket_items:
            return JsonResponse({'error': 'Basket is empty'}, status=400)

        # Need to check theres enough stock to fulfil the order.
        # Prompts the customer with a message depending on if item is out of stock or not enough stock.
        for basket_item in basket_items:
            if basket_item.item.stock_count < basket_item.quantity:
                if basket_item.item.stock_count <= 0:
                    return JsonResponse({
                        'error': f'{basket_item.item.name} is no longer in stock.'
                    }, status=400)
                else:
                    return JsonResponse({
                        'error': f'Only {basket_item.item.stock_count} x {basket_item.item.name} remaining in stock, please update quantity.'
                    }, status=400)


        order = Order.objects.create(customer=request.user)

        # Save the order information to access in order history for this customer.
        for basket_item in basket_items:
            OrderItem.objects.create(
                order=order,
                item=basket_item.item,
                quantity=basket_item.quantity,
                price=basket_item.item.price
            )

            basket_item.item.stock_count -= basket_item.quantity
            basket_item.item.save()

        # Empty the basket in the db.
        basket_items.delete()

        return JsonResponse({'message': f'Your order #{order.id} has been received.'})
