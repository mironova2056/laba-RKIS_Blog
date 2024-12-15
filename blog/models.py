from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    bio = models.TextField(blank=True)
    def __str__(self):
        return self.full_name
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    title = models.CharField(max_length=50, default='Заголовок')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.author.username} - {self.created_at}'
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'post')
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'
