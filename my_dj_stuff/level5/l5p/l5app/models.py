from django.db import models
from django.contrib.auth.models import User     # default User model from django


# Create your models here.
class UserProfileInfo(models.Model):
    # create relationship (don't inherit from User)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want
    portfolio = models.URLField(blank=True)
    picture = models.ImageField(upload_to='portfolio_pics', blank=True)  # to make python work with imagies pillow needs to be installed

    def __str__(self) -> str:
        return self.user.username
    