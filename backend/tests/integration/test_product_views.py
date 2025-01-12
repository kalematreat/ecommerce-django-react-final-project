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
    def test_create_product_as_admin(self,product_payload):
        response = self.client.post("/api/products/create/", product_payload, format="json")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        response_data = response.data
        try:
            assert response_data["name"] == product_payload["name"], "Product name mismatch"
        except AssertionError as e:
            print(f"Name assertion failed: {e}")
            
        try:
            assert str(response_data["price"]) == str(product_payload["price"]), "Product price mismatch"
        except AssertionError as e:
            print(f"Price assertion failed: {e}")
            
        try:
            assert response_data["brand"] == product_payload["brand"], "Product brand mismatch"
        except AssertionError as e:
            print(f"Brand assertion failed: {e}")
            
        try:
            assert response_data["countInStock"] == product_payload["countInStock"], "Product stock mismatch"
        except AssertionError as e:
            print(f"Stock assertion failed: {e}")
            
        try:
            assert response_data["category"] == product_payload["category"], "Product category mismatch"
        except AssertionError as e:
            print(f"Category assertion failed: {e}")
            
        try:
            assert response_data["description"] == product_payload["description"], "Product description mismatch"
        except AssertionError as e:
            print(f"Description assertion failed: {e}")

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

    @pytest.mark.django_db
    def test_get_top_products(self):
        response = self.client.get("/api/products/top/")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        response_data = response.data
        try:
            assert len(response_data) > 0, "No products found with rating >= 4"
        except AssertionError as e:
            print(f"Top products assertion failed: {e}")

    @pytest.mark.django_db
    def test_get_product(self):
        product = Product.objects.create(_id=1, name="Test Product", price=100)
        response = self.client.get(f"/api/products/{product._id}/")
        assert response.status_code == 200
        assert response.data['name'] == product.name
        assert response.data["_id"] == product._id, "Product ID mismatch"

    @pytest.mark.django_db
    def test_update_product_as_admin(self, product_payload):
        product = Product.objects.create(
            name="Initial Product",
            brand="Classic Minds",
            category="Classic Board Games",
            description="A timeless strategy game.",
            price=25.99,
            countInStock=100
        )
        assert product._id is not None, "Product ID should not be None"
        update_payload = product_payload.copy()
        update_payload["name"] = "Updated Name"
        response = self.client.put(f"/api/products/update/{product._id}/", update_payload, format="json")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        response_data = response.data
        try:
            assert response_data["name"] == update_payload["name"], "Updated product name mismatch"
        except AssertionError as e:
            print(f"Updated name assertion failed: {e}")

    def create_product(self):
        return Product.objects.create(
            _id=1,
            name="Initial Product",
            brand="Classic Minds",
            category="Classic Board Games",
            description="A timeless strategy game.",
            price=25.99,
            countInStock=100
        )

    







    



        


