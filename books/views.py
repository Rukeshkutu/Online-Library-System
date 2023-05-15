from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Pdf_Info, Review
from .form import *

import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.

def digital_books(request, pram = None):
    book = Pdf_Info.objects.all()
    if pram is not None:
        book=book.filter(title__startswith=pram)
    context = {
        'book':book
    }

    return render(request, 'books/home.html', context)

def view_book(request):
    book = Pdf_Info.objects.all()
    context={
        'book':book
    }
    return render(request, 'books/view_books.html', context)


def add_Book(request,pk=None):
    form = BookForm()#improt productform form form.py
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)#request.File send request to the file to be uploaded to uploade the file, without it there would be error while saving file
        print(form)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            messages.success(request, 'product added succcssfully')
            return redirect('books:digital_books')
        else:
            messages.error(request, 'Failed to add Product')
    
    context = {
        'form':form
    }
    return render(request, 'books/addbook.html', context)


def book_detail(request, slug):
    # book = get_object_or_404(Pdf_Info, slug = slug)
    # book = Pdf_Info.objects.get(slug=slug)
    book = Pdf_Info.objects.filter(slug = slug).first()
    # books.user_rating = rating.rating if rating else 0
    
    if request.method == "POST":
        rating = request.POST.get('rating')
        content = request.POST.get("content",'')
        
        if content:
            reviews = Review.objects.filter(created_by=request.user, book = book)
            
            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.content = content
                review.save()
            
            else:
                review = Review.objects.create(
                    book = book,
                    rating = rating,
                    content = content,
                    created_by= request.user
                )
            
            return redirect('books:book_detail', slug = slug)
        
    context = {'book':book}
    
    return render(request, 'books/book_detail.html', context)



def delete_book(request, pk):
    book = Pdf_Info.objects.filter(id = pk)
    
    # if request. != item.created_by:
    #     messages.INFO(request, 'You are not authorized')
    
    if request.method == 'POST':
        book.delete()
        return redirect('books:digital_books')

    context = {
        'book':book
    }
    return render(request, 'books/delete.html', context)



def search(request):
    queries = request.GET.get('query', False)# here 'query' is from 'name= query' in navbar
    if len(queries) > 50:
        book = Pdf_Info.objects.none()
    else:
        book = Pdf_Info.objects.filter(title__icontains = queries)

    if book.count() == 0:
        messages.warning(request, 'Search result not found.Please search again.')
    context = {
        'book':book,
        'queries':queries ,
        # 'recommended_books' : recommended_books
    }
    return render(request, 'books/search.html', context)