from locust import HttpUser, task, between
from random import randint

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task(2)
    def view_products(self):
        print("view_products")
        collection_id = randint(1, 10)
        self.client.get("/store/products/?collection_id={}".format(collection_id),
                        name="/store/products/")

    @task(4)
    def view_product(self):
        print("view_product")
        product_id = randint(1, 10)
        self.client.get(f"/store/products/{product_id}",
                        name="/store/products/:id")

    @task(1)
    def add_to_cart(self):
        print("add_to_cart")
        product_id = randint(1, 10)
        self.client.post(f"/store/cart/{product_id}/",
                         name="/store/cart/items", json={"product_id": product_id, "quantity": 1})


    @task(1)
    def say_hello(self):
        self.client.get("/playground/hello/")





    def on_start(self): # called when a Locust start before any task is scheduled
        response = self.client.post("/store/carts/")
        result = response.json()
        self.cart_id = result['id']

