import pytest
from rest_framework.test import APIClient
from rest_framework import status
from base.models import Product, Review, User
from rest_framework_simplejwt.tokens import RefreshToken
import unittest

@pytest.fixture
def product_payload():
    return {
        "name": "Code",
        "price": "10.00",
        "brand": "Classic Minds",
        "countInStock": 100,
        "category": "Classic Board Games",
        "description": (
            "A timeless strategy game where two players compete to capture or block all of the "
            "opponent's pieces. This set features smooth, durable pieces and a wooden board for a high-quality experience."
        )
    }

@pytest.fixture()
def id_product():
    return 70


@pytest.mark.django_db
class TestProductAPI():
   
    def setup_method(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            email="admin@test.com",
            password="adminpassword"
        )
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')


    @pytest.mark.django_db
    def test_get_products(self):
        response = self.client.get("/api/products/")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

        response_data = response.data
        try:
            assert "products" in response_data, "Missing products data"
        except AssertionError as e:
            print(f"Products key assertion failed: {e}")
        try:
            assert "page" in response_data, "Missing page information"
        except AssertionError as e:
            print(f"Page key assertion failed: {e}")
        try:
            assert "pages" in response_data, "Missing total pages information"
        except AssertionError as e:
            print(f"Pages key assertion failed: {e}")








    



        


