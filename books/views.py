from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Book
from .serializers import BookSerializer
from .services import get_exchange_rate

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # 1. Endpoint Opcional: Buscar por categoría
    # GET /books/?category=Literatura
    def get_queryset(self):
        queryset = Book.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

    # 2. Endpoint Opcional: Libros con stock bajo
    # GET /books/low-stock/?threshold=10
    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        threshold = request.query_params.get('threshold', 10)
        try:
            threshold = int(threshold)
        except ValueError:
            return Response({"error": "Threshold debe ser un número"}, status=status.HTTP_400_BAD_REQUEST)
            
        books = Book.objects.filter(stock_quantity__lt=threshold)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 3. Endpoint Importante: Calcular precio de venta
    # POST /books/{id}/calculate-price/
    @action(detail=True, methods=['post'], url_path='calculate-price')
    def calculate_price(self, request, pk=None):
        book = self.get_object() # Obtiene el libro por ID o lanza 404
        
        # Lógica de negocio
        exchange_rate = get_exchange_rate()
        margin = 1.40  # Margen del 40%
        
        cost_local = float(book.cost_usd) * exchange_rate
        selling_price = cost_local * margin
        
        # Guardar en base de datos
        book.selling_price_local = round(selling_price, 2)
        book.save()
        
        # Respuesta detallada según el requerimiento
        return Response({
            "book_id": book.id,
            "cost_usd": float(book.cost_usd),
            "exchange_rate": exchange_rate,
            "cost_local": round(cost_local, 2),
            "margin_percentage": 40,
            "selling_price_local": book.selling_price_local,
            "currency": "EUR",
            "calculation_timestamp": timezone.now()
        }, status=status.HTTP_200_OK)