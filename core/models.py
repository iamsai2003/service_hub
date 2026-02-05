from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=[('Home', 'Home'), ('Appliance', 'Appliance'), ('Cleaning', 'Cleaning')], default='Home')
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([r.rating for r in reviews]) / len(reviews)
        return 0

    def __str__(self):
        return self.name

class Review(models.Model):
    service = models.ForeignKey(Service, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    address = models.TextField(default="Hyderabad")
    booking_date = models.DateField(default=timezone.now)
    booking_time = models.TimeField(default="10:00")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending','Pending'), ('Confirmed','Confirmed'), ('Completed','Completed')])
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"

class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, related_name='items', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.service.name}"