from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)  # Optional, to categorize products
    content_vector = models.JSONField()  # Store product content features (e.g., [1, 0, 0] for one-hot encoded features)

    def __str__(self):
        return self.name

class UserInteraction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)  # e.g., 'view', 'purchase'
    rating = models.FloatField(null=True, blank=True)  # Optional: Store rating for explicit feedback (if any)

    class Meta:
        unique_together = ("user", "product")  # Ensure that a user can only have one interaction per product

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.interaction_type})"

