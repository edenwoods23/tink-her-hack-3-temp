from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import SkinProfile, Product, Order
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'skin/register.html', {'form': form})

@login_required
def dashboard(request):
    try:
        profile = request.user.skinprofile
        current_season_type = profile.get_current_season_skin_type()
        recommended_products = Product.objects.filter(suitable_for__icontains=current_season_type)
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        
        context = {
            'profile': profile,
            'current_season_type': current_season_type,
            'recommended_products': recommended_products[:4],
            'recent_orders': orders[:5]
        }
    except SkinProfile.DoesNotExist:
        context = {
            'needs_profile': True
        }
    
    return render(request, 'skin/dashboard.html', context)

@login_required
def create_skin_profile(request):
    try:
        profile = request.user.skinprofile
        return redirect('update_skin_profile')
    except SkinProfile.DoesNotExist:
        if request.method == 'POST':
            SkinProfile.objects.create(
                user=request.user,
                summer_skin_type=request.POST.get('summer_skin_type'),
                winter_skin_type=request.POST.get('winter_skin_type'),
                monsoon_skin_type=request.POST.get('monsoon_skin_type'),
                spring_skin_type=request.POST.get('spring_skin_type'),
                concerns=request.POST.get('concerns'),
                goals=request.POST.get('goals'),
                allergies=request.POST.get('allergies')
            )
            messages.success(request, 'Skin profile created successfully!')
            return redirect('product_list')
    return render(request, 'skin/create_profile.html', {'skin_type_choices': SkinProfile.SKIN_TYPE_CHOICES})

@login_required
def update_skin_profile(request):
    profile = request.user.skinprofile
    if request.method == 'POST':
        profile.summer_skin_type = request.POST.get('summer_skin_type')
        profile.winter_skin_type = request.POST.get('winter_skin_type')
        profile.monsoon_skin_type = request.POST.get('monsoon_skin_type')
        profile.spring_skin_type = request.POST.get('spring_skin_type')
        profile.concerns = request.POST.get('concerns')
        profile.goals = request.POST.get('goals')
        profile.allergies = request.POST.get('allergies')
        profile.save()
        messages.success(request, 'Skin profile updated successfully!')
        return redirect('product_list')
    return render(request, 'skin/update_profile.html', {
        'profile': profile,
        'skin_type_choices': SkinProfile.SKIN_TYPE_CHOICES
    })

class ProductListView(ListView):
    model = Product
    template_name = 'skin/product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filter by skin type if specified
        skin_type = self.request.GET.get('skin_type')
        if skin_type:
            queryset = queryset.filter(suitable_for=skin_type)
        # If no skin type filter, use current season's skin type for authenticated users
        elif self.request.user.is_authenticated:
            try:
                profile = self.request.user.skinprofile
                current_skin_type = profile.get_current_season_skin_type()
                queryset = queryset.filter(suitable_for=current_skin_type)
            except SkinProfile.DoesNotExist:
                pass
        
        # Filter by category if specified
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = self.request.user.skinprofile
                context['current_season_skin_type'] = profile.get_current_season_skin_type()
            except SkinProfile.DoesNotExist:
                context['needs_profile'] = True
        
        # Add filter states to context
        context['current_category'] = self.request.GET.get('category')
        context['current_skin_type'] = self.request.GET.get('skin_type')
        
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'skin/product_detail.html'
    context_object_name = 'product'

def home(request):
    return render(request, 'skin/home.html')