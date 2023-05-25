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

#item based collaborative system
def recommend(request):
    # Fetch data from database and store in dataframes
    df_books = pd.DataFrame(list(Pdf_Info.objects.all().values()))
    df_books.dropna(inplace=True)
    df_reviews = pd.DataFrame(list(Review.objects.all().values()))
    df_books.fillna(0, inplace=True)
    df_reviews.fillna(0, inplace=True)

    # Merge dataframes to create a single ratings dataframe
    ratings_with_name = df_reviews.merge(df_books, on='isbn')

    # Filter ratings and books to only include users and books with sufficient ratings
    x = ratings_with_name.groupby('created_by_id').count()['rating'] > 3
    read_users = x[x].index
    filtered_rating = ratings_with_name[ratings_with_name['created_by_id'].isin(read_users)]
    y = filtered_rating.groupby('title').count()['rating'] >= 2
    famous_books = y[y].index
    final_ratings = filtered_rating[filtered_rating['created_by_id'].isin(read_users) & filtered_rating['title'].isin(famous_books)]

    # Create pivot table with ratings as values
    pt = final_ratings.pivot_table(index='title', columns='created_by_id', values='rating')
    # Replace NaN values with mean rating of the book
    pt = pt.apply(lambda row: row.fillna(row.mean()), axis=1)

    if request.method == 'POST':
        # Fetch user input
        user_input = request.POST.get('user_input')

        if user_input is not None:
            # Get indices of books that match the user query
            match_indices = np.where(pt.index.str.contains(user_input, case=False))[0]

            if len(match_indices) > 0:
                # Get similarity scores for all books
                similarity_scores = cosine_similarity(pt)

                # Get indices of similar books with the same genre as the searched book
                similar_items = []
                for i in range(similarity_scores.shape[0]):
                    if i in match_indices:
                        # Check if book has the same genre as the searched book
                        if df_books.loc[df_books['title'] == pt.index[i], 'genre_id'].iloc[0] == df_books.loc[df_books['title'] == pt.index[match_indices[-1]], 'genre_id'].iloc[0]:
                            # Append index and similarity score to list
                            if i != match_indices[-1]:
                                similar_items.append((i, similarity_scores[match_indices[-1]][i]))

                # Sort by similarity score
                similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)[:9]

                # Get book information and append to list
                data = []
                for i in similar_items:
                    item = {}
                    temp_pdf_info = ratings_with_name[ratings_with_name['isbn'] == final_ratings[final_ratings['title'] == pt.index[i[0]]]['isbn'].iloc[0]]
                    # temp_pdf_info = df_books[df_books['isbn'] == final_ratings[final_ratings['title'] == pt.index[i[0]]]['isbn'].iloc[0]]
                    if len(temp_pdf_info) == 0:
                        continue
                    item['title'] = temp_pdf_info.iloc[0]['title']
                    item['author'] = temp_pdf_info.iloc[0]['author']
                    item['image'] = temp_pdf_info.iloc[0]['image']
                    item['description'] = temp_pdf_info.iloc[0]['description']
                    item['isbn'] = temp_pdf_info.iloc[0]['isbn']
                    item['published_year'] = temp_pdf_info.iloc[0]['published_year']
                    item['book_pdf'] = temp_pdf_info.iloc[0]['book_pdf']
                    item['is_premium'] = temp_pdf_info.iloc[0]['is_premium']
                    item['reviews'] = []
                    book_isbn = df_books[df_books['title'] == pt.index[i[0]]]['isbn'].iloc[0]
                    book_reviews = df_reviews[df_reviews['isbn'] == book_isbn]
                    print(book_reviews)
                    for review in book_reviews.itertuples():
                        temp_review = {}
                        temp_review['rating'] = review.rating
                        temp_review['content'] = review.content
                        temp_review['created_at'] = review.created_at
                        temp_review['created_by'] = review.created_by_id
                        item['reviews'].append(temp_review)
                    
                    if len(item['reviews']) > 0:
                        item['avg_rating'] = round(sum([review['rating'] for review in item['reviews']]) / len(item['reviews']), 1)
                    else:
                        item['avg_rating'] = 0
                    data.append(item)
                    data = sorted(data, key=lambda x: x['avg_rating'], reverse=True)
            else:
                messages.info(request, 'Recommendations not found')
                data = []
        else:
            messages.info(request, 'Please enter a book name')
            data = []

        context = {
            'data' : data
        }

        return render(request, 'books/recommendation.html', context)

    return render(request, 'books/recommendation.html')