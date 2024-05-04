from rest_framework import serializers
from .models import Produto, Categoria

class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.titulo', read_only=True)

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'categoria_nome', 'preco_venda', 'quantidade']
    