from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Car, Brand, Order, Comment
from .forms import UserRegisterForm, UserUpdateForm, CommentForm

class HomeView(ListView):
    model = Car
    template_name = 'home.html'
    context_object_name = 'cars'

    def get_queryset(self):
        brand_id = self.request.GET.get('brand')
        if brand_id:
            return Car.objects.filter(brand_id=brand_id)
        else:
            return Car.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand_id = self.request.GET.get('brand')
        if brand_id:
            brand = get_object_or_404(Brand, pk=brand_id)
            context['selected_brand'] = brand
            context['car_count'] = brand.car_set.count()  # Count cars for selected brand
        else:
            context['car_count'] = Car.objects.count()  # Total car count
        context['brands'] = Brand.objects.all()
        return context

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'profile.html'
    success_url = '/'

    def get_object(self):
        return self.request.user

@login_required
def buy_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if car.quantity > 0:
        car.quantity -= 1
        car.save()
        Order.objects.create(user=request.user, car=car)
        messages.success(request, f'You have bought {car.title}')
    else:
        messages.error(request, 'This car is out of stock')
    return redirect('car_detail', pk=pk)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def add_comment(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.save()
            messages.success(request, 'Your comment has been added')
    return redirect('car-detail', pk=pk)

class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        # Add search logic here
        return render(request, 'search_results.html', {'query': query})
    
