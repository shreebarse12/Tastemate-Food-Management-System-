from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import orders
from menu.models import Dish

@login_required
def place_order(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        total_price = dish.price * quantity
        pickup_time = request.POST.get("pickup_time")
        
        # --- NEW: Get payment method from the HTML form ---
        # Defaults to 'cod' (Pay at Counter) if something goes wrong
        payment_method = request.POST.get("payment_method", "cod") 
        # --------------------------------------------------

        if pickup_time:
            # Convert string to datetime object
            try:
                pickup_time = datetime.strptime(pickup_time, "%Y-%m-%dT%H:%M")
            except ValueError:
                pickup_time = None # Handle cases where time might be missing
        
        # Create the order
        orders.objects.create(
            student=request.user,
            dish=dish,
            quantity=quantity,
            total_price=total_price,
            pickup_time=pickup_time,
            
            # --- NEW: Save the payment method to the database ---
            payment_method=payment_method 
            # ----------------------------------------------------
        )
        
        messages.success(request, "Order placed successfully!")
        return redirect("my_orders")

    return render(request, "place_order.html", {"dish": dish})

@login_required
def my_orders(request):
    # Fetch orders for the logged-in student
    order_list = orders.objects.filter(student=request.user).order_by("-ordered_at")
    return render(request, "my_orders.html", {"orders": order_list})

@login_required
def manage_orders(request):
    """For canteen users to accept/reject orders"""
    order_list = orders.objects.filter(dish__canteen=request.user).order_by("-ordered_at")
    return render(request, "orders/manage_orders.html", {"orders": order_list})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(orders, id=order_id, student=request.user)
    
    if request.method == "POST":
        order.delete()
        messages.success(request, "Order deleted successfully!")
        return redirect('my_orders')