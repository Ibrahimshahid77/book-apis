from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Book,Purchase
from .serializers import BookSerializer

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        validate_email(email)
    except ValidationError:
        return Response({"error": "Invalid email format"})

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"})
    
    User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "User created successfully"})                 

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'message': f"Welcome {user.username}!"
        })
    else:
        return Response({"error": "Invalid credentials"})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def newview(request):
    return Response({"message": f"Hello, {request.user.username}!"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_book(request):
    title = request.data.get('title')
    author = request.data.get('author')
    
    if not title or not author:
        return Response({"error": "Both title and author are required"})
    if Book.objects.filter(user=request.user, title=title, author=author).exists():
        return Response({"error": "This book is already added"})
    book = Book.objects.create(title=title, author=author, user=request.user)
    return Response({"Msg": "Book is added", "book_id": book.id})
 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_books(request):
    books = Book.objects.filter(user=request.user)
    books_list = [{ "title": b.title, "author": b.author} for b in books]
    return Response({"books": books_list})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_books(request):
    books = Book.objects.all()
    books_list = [{
        "title": b.title,
        "author": b.author,
        "user": b.user.username} for b in books]
    return Response({"books": books_list})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getall_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_book(request):
    book_id = request.data.get('book_id')
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found."}, status=404)
    Purchase.objects.create(user=request.user, book=book)
    return Response({
        "message": f"You bought '{book.title}'",
        "book": {
            "title": book.title,
            "author": book.author
        }
    })        


