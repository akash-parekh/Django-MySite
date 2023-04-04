from django.db import models

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name()}"


class Tag(models.Model):
    caption = models.CharField(max_length=80)

    def __str__(self):
        return f"#{self.caption}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField()
    slug = models.SlugField(default="", null=False, unique=True)
    content = models.TextField()
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    caption = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Comment(models.Model):
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
