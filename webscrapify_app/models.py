from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class Metadata(models.Model):
    schedule_id = models.CharField(max_length=100)  # Assuming schedule ID as a string
    user_id = models.IntegerField()
    file_path = models.CharField(max_length=255)  # File path where scraped data is saved

    # Add more fields as needed, like timestamp, etc.

    def __str__(self):
        return f"Schedule ID: {self.schedule_id}, User ID: {self.user_id}"