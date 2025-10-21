# api/tests/factories.py
import factory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall('set_password', '123456')
    is_staff = False  # padrão para a maioria dos testes
    is_superuser = False  # padrão para a maioria dos testes
