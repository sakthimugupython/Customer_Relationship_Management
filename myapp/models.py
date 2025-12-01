from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class FollowUp(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='followups')
    note = models.TextField()
    follow_up_date = models.DateTimeField()
    next_follow_up_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-follow_up_date']
    
    def __str__(self):
        return f"Follow-up for {self.customer.name} on {self.follow_up_date.strftime('%Y-%m-%d')}"
