# api/tests/test_product_viewset.py
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from api.models import Product
from api.factories import UserFactory

class TestProductViewSet(APITestCase):
    def setUp(self):
        # Cria um usuário staff para passar nas permissões
        self.user = UserFactory(is_staff=True)
        
        # Cria token ou pega o token existente
        self.token, _ = Token.objects.get_or_create(user=self.user)
        
        # Configura o client para usar o token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        
        # URL base da ViewSet
        self.list_url = reverse('product-list')  # ajuste para o name correto da rota

    def test_list_products(self):
        # Cria alguns produtos para teste
        Product.objects.create(title="Produto 1", description="Descrição 1", price=10)
        Product.objects.create(title="Produto 2", description="Descrição 2", price=20)
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_product(self):
        data = {
            'title': 'World of Warcraft (1 mo.)',
            'description': 'Adiciona 1 mês de assinatura à conta.',
            'price': 35
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Confirma se o produto foi criado no banco
        product = Product.objects.get(title='World of Warcraft (1 mo.)')
        self.assertEqual(product.price, 35)
