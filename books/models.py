from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.urls import reverse
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=50, db_index = True)
    slug = models.SlugField(max_length = 100,unique=True)
        
    def __str__(self):
        return self.name
    
    
class Pdf_Info(models.Model):
    genre = models.ForeignKey(Genre,related_name='genere', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    publisher = models.CharField(max_length=250)
    image = models.ImageField(upload_to = 'book_image/')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100)
    published_year = models.CharField(max_length=4, blank=True)
    book_pdf = models.FileField(upload_to='book/')
    is_premium = models.BooleanField(default=False)
 
    def get_absolute_url(self):
        return reverse("books:book_detail", args=[self.slug])
    
    def get_rating(self):
        reviews_total = 0
        
        for review in self.reviews.all():
            reviews_total += review.rating
        
        if reviews_total > 0:
            return round(reviews_total / self.reviews.count(), 1)
        
        return 0
    
    
    def __str__(self):
        return self.title
    

class Review(models.Model):
    book = models.ForeignKey(Pdf_Info, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField(max_length= 300)
    created_at = models.DateTimeField(auto_now_add=True)
    isbn = models.CharField(max_length=13)
    
    def save(self, *args, **kwargs):
        self.isbn = self.book.isbn
        super().save(*args, **kwargs)
    
    # def __str__(self):
    #     return f"{self.created_by.username} - {self.book.title}"
    
