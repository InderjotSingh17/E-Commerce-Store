from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, TemplateView, View
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from .models import Product, CartItem, OrderItem, Order
stripe.api_key = settings.STRIPE_SECRET_KEY
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    paginate_by = 12
    ordering = ['-id']
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    print(CartItem.objects.filter(user=request.user)) 
    return redirect('cart')
def decrease_quantity(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item = CartItem.objects.filter(user=request.user, product=product).first()
    if item:
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    return redirect('cart')
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item = CartItem.objects.filter(user=request.user, product=product).first()
    if item:
        item.delete()
    return redirect('cart')
class CartView(TemplateView):
    template_name = 'cart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = CartItem.objects.filter(user=self.request.user)
        total = sum(item.get_total_price() for item in items)
        context['items'] = items
        context['total'] = total
        return context
def checkout_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    if not cart_items.exists():
        return redirect('cart')
    order = Order.objects.filter(user=user, ordered=False).first()
    if not order:
        order = Order.objects.create(user=user)
    order.items.clear()
    for cart_item in cart_items:
        order_item = OrderItem.objects.create(
            product=cart_item.product,
            quantity=cart_item.quantity
        )
        order.items.add(order_item)
    order.save()
    cart_items.delete()  
    return redirect('order-summary', order.id)
class OrderSummaryView(DetailView):
    model = Order
    template_name = 'order_summary.html'
    context_object_name = 'order'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        items = order.items.all()
        total = sum(item.get_total_price() for item in items)
        context['items'] = items
        context['total'] = total
        context['stripe_public_key'] = settings.STRIPE_PUBLISHABLE_KEY 
        return context
class CreateCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        order = Order.objects.filter(user=user, ordered=False).first()
        if not order or not order.items.exists():
            return JsonResponse({'error': 'No active order'}, status=400)
        YOUR_DOMAIN = 'http://localhost:8000'
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item.product.price * 100),
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                } for item in order.items.all()
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
            metadata={'order_id': str(order.id)}
        )

        return JsonResponse({'id': session.id})
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            order.ordered = True
            order.save()
        except Order.DoesNotExist:
            pass
    return HttpResponse(status=200)
