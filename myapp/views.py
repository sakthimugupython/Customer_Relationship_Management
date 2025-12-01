from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta
from .models import Customer, FollowUp


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'myapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'myapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    today = timezone.now().date()
    today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    today_end = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))
    
    total_customers = Customer.objects.count()
    new_customers = Customer.objects.filter(status='new').count()
    contacted_customers = Customer.objects.filter(status='contacted').count()
    converted_customers = Customer.objects.filter(status='converted').count()
    lost_customers = Customer.objects.filter(status='lost').count()
    
    today_followups = FollowUp.objects.filter(
        follow_up_date__gte=today_start,
        follow_up_date__lte=today_end
    ).select_related('customer')
    
    context = {
        'total_customers': total_customers,
        'new_customers': new_customers,
        'contacted_customers': contacted_customers,
        'converted_customers': converted_customers,
        'lost_customers': lost_customers,
        'today_followups': today_followups,
        'today_count': today_followups.count(),
    }
    return render(request, 'myapp/dashboard.html', context)


@login_required(login_url='login')
def customer_list(request):
    status_filter = request.GET.get('status')
    customers = Customer.objects.all()
    
    if status_filter:
        customers = customers.filter(status=status_filter)
    
    context = {
        'customers': customers,
        'status_filter': status_filter,
        'status_choices': Customer.STATUS_CHOICES,
    }
    return render(request, 'myapp/customer_list.html', context)


@login_required(login_url='login')
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    followups = customer.followups.all()
    
    context = {
        'customer': customer,
        'followups': followups,
    }
    return render(request, 'myapp/customer_detail.html', context)


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def customer_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        status = request.POST.get('status', 'new')
        
        customer = Customer.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
            status=status,
        )
        return redirect('customer_detail', pk=customer.pk)
    
    context = {
        'status_choices': Customer.STATUS_CHOICES,
    }
    return render(request, 'myapp/customer_form.html', context)


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        customer.address = request.POST.get('address')
        customer.status = request.POST.get('status')
        customer.save()
        return redirect('customer_detail', pk=customer.pk)
    
    context = {
        'customer': customer,
        'status_choices': Customer.STATUS_CHOICES,
        'is_edit': True,
    }
    return render(request, 'myapp/customer_form.html', context)


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    
    context = {'customer': customer}
    return render(request, 'myapp/customer_confirm_delete.html', context)


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def followup_add(request, customer_pk=None):
    customer = None
    if customer_pk:
        customer = get_object_or_404(Customer, pk=customer_pk)
    
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        note = request.POST.get('note')
        follow_up_date = request.POST.get('follow_up_date')
        next_follow_up_date = request.POST.get('next_follow_up_date')
        
        customer_obj = get_object_or_404(Customer, pk=customer_id)
        
        followup = FollowUp.objects.create(
            customer=customer_obj,
            note=note,
            follow_up_date=follow_up_date,
            next_follow_up_date=next_follow_up_date if next_follow_up_date else None,
        )
        
        return redirect('customer_detail', pk=customer_obj.pk)
    
    context = {
        'customer': customer,
        'customers': Customer.objects.all(),
    }
    return render(request, 'myapp/followup_form.html', context)
