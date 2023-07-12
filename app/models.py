from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your models here.

class Blog (models.Model) :
    content = models.TextField ()
    title = models.CharField (max_length = 250)
    category = models.CharField (max_length = 25, default = "News")
    date = models.DateTimeField (auto_now_add = True)
    author = models.IntegerField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="blogs/",default="default.jpg")
    def __str__(self):
        return f"{self.title} by {self.author.username}"
class Comment (models.Model) :
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.comment} by {self.author.username}"