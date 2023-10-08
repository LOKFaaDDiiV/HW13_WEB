from django.db import models

# Create your models here.


class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.DateField()
    born_location = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    quote_text = models.CharField(max_length=5000)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.quote_text}"
