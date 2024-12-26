from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Canvas(models.Model):
    title = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    cooldown = models.IntegerField(default=300)  # valeur par défaut de 5 minutes
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.width}x{self.height})"

class Pixel(models.Model):
    canvas = models.ForeignKey(Canvas, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    color = models.CharField(max_length=7)  # Format: #RRGGBB
    placed_at = models.DateTimeField(default=timezone.now)
    placed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['canvas', 'x', 'y']),
        ]

    def __str__(self):
        return f"Pixel at ({self.x},{self.y}) on {self.canvas.title}"