from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.


class Profile(models.Model):
    # second arg: if user delete, delete profile, not other way around
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # second arg: dir. where pics are uploaded
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):  # overriding parent class save. kwargs takes in extra arguments if there are any
        super().save()
        # open cur. instance image to resize
        current_img = Image.open(self.image.path)
        if current_img.height > 300 or current_img.width > 300:
            output_size = (300, 300)
            current_img.thumbnail(output_size)
            current_img.save(self.image.path)
