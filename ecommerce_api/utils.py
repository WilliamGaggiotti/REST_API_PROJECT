from ecommerce_api.models import Product

class ProductUtil:

    @staticmethod
    def update_product_stock(prod_and_cants, operating=1):
        '''
        Función que recibe una lista de diccionarios, donde cada diccionario tiene un producto y un stock, y un operando que indica si hay que restar o sumar stock a los productos.
        prod_and_cant = [{“product”: Product(1), “cuantity”: 10},
                        {“product”: Product(2), “cuantity”: 8},
                        {“product”: Product(7), “cuantity”: 12}]
        ‘operating’ puede ser 1 o -1. Lo que hará que se sume y se reste al stock del producto respectivamente 
        '''
        products = []
        for prod_and_cant in prod_and_cants:
            prod_and_cant['product'].set_stock(prod_and_cant['product'].get_stock() + (prod_and_cant['cuantity'] * operating))
            products.append(prod_and_cant['product'])

        Product.objects.bulk_update(products, ['stock'])