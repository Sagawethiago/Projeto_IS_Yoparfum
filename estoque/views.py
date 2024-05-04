from django.shortcuts import render
from .forms import ProdutoForm
from .models import Categoria, Produto, Imagem
from django.http import HttpResponse
from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from rolepermissions.decorators import has_permission_decorator
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProdutoSerializer
from django.contrib.auth.decorators import login_required
import requests
from django.db.models import Count
from collections import Counter



@login_required
def minha_view(request):
    url = "http://127.0.0.1:8000/estoque/api/produtos/"
    response = requests.get(url)
    dados = response.json()

    return render(request, 'apivz.html', {'dados': dados})
@login_required
def dashboard(request):
    url = "http://127.0.0.1:8000/estoque/api/produtos/"
    response = requests.get(url)
    produtos = response.json()  # assumindo que isso retorna uma lista de produtos

    # Processando os dados para o dashboard
    total_produtos = len(produtos)
    count_by_name = Counter([produto['nome'] for produto in produtos])
    count_by_categoria = Counter([produto['categoria_nome'] for produto in produtos if produto['categoria_nome']])


    price_ranges = {
        'Até R$50': sum(1 for produto in produtos if produto['preco_venda'] <= 50),
        'R$51 a R$100': sum(1 for produto in produtos if 50 < produto['preco_venda'] <= 100),
        'R$101 a R$500': sum(1 for produto in produtos if 100 < produto['preco_venda'] <= 500),
        'Mais de R$500': sum(1 for produto in produtos if produto['preco_venda'] > 500)
    }

    # Preparando dados para enviar ao template
    dados_dashboard = {
        'total_produtos': total_produtos,
        'count_by_name': count_by_name.items(),
        'count_by_categoria': count_by_categoria.items(),
        'price_ranges': [ {'range': k, 'count': v} for k, v in price_ranges.items() ]
    }

    return render(request, 'dashboard.html', dados_dashboard)


@login_required
def index(request):
    return render(request, 'index.html')

class ProdutoList(APIView):
    def get(self, request, format=None):
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)

@login_required
def list_produtos(request):
    query = Q()
    nome = request.GET.get('nome')
    categoria_id = request.GET.get('categoria_id')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')

    if nome:
        query &= Q(nome__icontains=nome)
    if categoria_id:
        query &= Q(categoria_id=categoria_id)
    if preco_min:
        query &= Q(preco_venda__gte=preco_min)
    if preco_max:
        query &= Q(preco_venda__lte=preco_max)

    produtos = Produto.objects.filter(query)
    categorias = Categoria.objects.all()
    return render(request, 'list_produtos.html', {
        'produtos': produtos,
        'categorias': categorias,
        'nome': nome,
        'categoria_id': categoria_id,
        'preco_min': preco_min,
        'preco_max': preco_max
    })


@login_required
#@has_permission_decorator('cadastrar_produtos')
def add_produto(request):
    if request.method == "GET":
        nome = request.GET.get('nome')
        categoria = request.GET.get('categoria')
        preco_min = request.GET.get('preco_min')
        preco_max = request.GET.get('preco_max')
        produtos = Produto.objects.all()

        if nome or categoria or preco_min or preco_max:

            if not preco_min:
                preco_min = 0

            if not preco_max:
                preco_max = 9999999

            if nome:
                produtos = produtos.filter(nome__icontains=nome)

            if categoria:
                produtos = produtos.filter(categoria=categoria)

            produtos = produtos.filter(preco_venda__gte=preco_min).filter(preco_venda__lte=preco_max)

        categorias = Categoria.objects.all()
        return render(request, 'add_produto.html', {'categorias': categorias, 'produtos': produtos})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        quantidade = request.POST.get('quantidade')
        preco_compra = request.POST.get('preco_compra')
        preco_venda = request.POST.get('preco_venda')

        produto = Produto(nome=nome,
                          categoria_id=categoria,
                          quantidade=quantidade,
                          preco_compra=preco_compra,
                          preco_venda=preco_venda)

        produto.save()

        for f in request.FILES.getlist('imagens'):
            name = f'{date.today()}-{produto.id}.jpg'

            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((300, 300))
            draw = ImageDraw.Draw(img)
            draw.text((20, 280), f"CONSTRUCT {date.today()}", (255, 255, 255))
            output = BytesIO()
            img.save(output, format="JPEG", quality=100)
            output.seek(0)
            img_final = InMemoryUploadedFile(output,
                                             'ImageField',
                                             name,
                                             'image/jpeg',
                                             sys.getsizeof(output),
                                             None
                                             )

            img_dj = Imagem(imagem=img_final, produto=produto)
            img_dj.save()
        messages.add_message(request, messages.SUCCESS, 'Produto cadastrado com sucesso')
        return redirect(reverse('add_produto'))

@login_required
def produto(request, slug):
    if request.method == "GET":
        produto = Produto.objects.get(slug=slug)
        data = produto.__dict__
        data['categoria'] = produto.categoria.id
        form = ProdutoForm(initial=data)
        return render(request, 'produto.html', {'form': form})