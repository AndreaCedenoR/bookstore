from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'selling_price_local')

    def validate_isbn(self, value):
        # Obtenemos el ID del libro que estamos editando (si existe)
        instance = getattr(self, 'instance', None)
        
        # Buscamos si hay OTRO libro (excluyendo el actual) con ese mismo ISBN
        query = Book.objects.filter(isbn=value)
        if instance:
            query = query.exclude(pk=instance.pk)
            
        if query.exists():
            raise serializers.ValidationError("Este ISBN ya está registrado en otro libro.")
            
        return value