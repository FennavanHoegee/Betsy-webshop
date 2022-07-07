__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from select import select
from models import *



# Met onderstaande functie zoek je naar een term in de name en description fields van de Product tabel.
def search(term):
    """Search for products based on a term. 
    Searching for 'sweater' should yield all products that 
    have the word 'sweater' in the name. 
    This search should be case-insensitive"""
    template= "{product.product_name} | {product.description} | {product.price_unit} | {product.quantity_in_stock} "
    for product in Product.select().where((Product.product_name.contains(term)) | (Product.description.contains(term))):
        print(template.format(product=product))
        print('-'*35)




# Met onderstaande functie kan je alle producten van een enkele gebruiker in zien.
def list_user_products(user_id):
    """View the products of a given user."""
    for row in Product_User.select(Product_User.user_id, Product.product_name, Product_User.quantity).join(Product).where(Product_User.user_id==user_id).dicts():
        print(row)



# Met onderstaande functie kan je alle producten van een tag in zien.
def list_products_per_tag(tag_id):
    """View all products for a given tag."""
    for row in (ProductTags.select( Tag.tag, ProductTags.product_id, Product.product_name).join(Product).switch(ProductTags).join(Tag).where((ProductTags.tag_id==tag_id))).dicts():
        print(row)




# Met onderstaande functie voeg je een product toe aan een gebruiker. 
# Ik heb de functie uitgebreidt door een extra parameter genaamd 'quantity' toe te voegen. 
# Zo kunnen er meerdere stuks van hetzelfde product worden toegevoegd aan de user.
# Ook heb ik de functie naam aangepast van add_product_to_catalog() naar add_product_to_user() omdat ik dat logische vond.
def add_product_to_user(user_id, product, quantity):
    """Add a product to a user."""
    quantity=quantity
    product_id=(Product.select(Product.product_id) .where(Product.product_name==product))
    query= (Product_User.select().where((Product_User.product_id==product_id) & (Product_User.user_id==user_id)))
    already_exists = query.count()
    if already_exists > 0:
        qry=Product_User.update({Product_User.quantity: (Product_User.quantity + quantity)}).where((Product_User.product_id==product_id) & (Product_User.user_id==user_id))
        qry.execute()
    else:
        Product_User.create(user_id=user_id, product_id=product_id, quantity=quantity)





# Met onderstaande functie verwijder je een product van  een gebruiker. 
# Ik heb de functie uitgebreidt door een extra parameter genaamd 'quantity', en een parameter genaamd 'user_id' toe te voegen. 
# Zo kunnen er meerdere stuks van hetzelfde product worden toegevoegd aan de user. En zo weet ik van welke user er een product moet worden verwijderd.
# Ook heb ik de functie naam aangepast van remove_product() naar remove_product_from_user() omdat ik dat logische vond.
def remove_product_from_user(user_id, product, quantity):
    """Add a product to a user."""
    quantity=quantity
    product_id=(Product.select(Product.product_id) .where(Product.product_name==product))
    query= (Product_User.select().where((Product_User.product_id==product_id) & (Product_User.user_id==user_id)))
    already_exists = query.count()
    if already_exists > 0:
        qry=Product_User.update({Product_User.quantity: (Product_User.quantity - quantity)}).where((Product_User.product_id==product_id) & (Product_User.user_id==user_id))
        qry.execute()
    else:
        print("Error: user doesn't own this product, so it can't be removed.")
        exit()



# Met onderstaande functie wijzig je het aantal producten in stock.
def update_stock(product_id, new_quantity):
    """Update the stock quantity of a product."""
    query=Product.update({Product.quantity_in_stock: new_quantity}).where(Product.product_id==product_id)
    query.execute()





# Met onderstaande functie verwijder je een hoeveelheid producten uit de inventaris, deze functie zal later worden gebruikt.
def remove_product_from_stock( product, quantity):
    """Add a product to a user."""

    product_id=(Product.select(Product.product_id) .where(Product.product_name==product))
    quantity_stock= (Product.select(Product.quantity_in_stock).where((Product.product_id==product_id))).scalar()
    if quantity_stock > 1:
        qry=Product.update({Product.quantity_in_stock: (Product.quantity_in_stock - quantity)}).where((Product.product_id==product_id))
        qry.execute()
    else:
        qry = Product.delete().where(Product.product_id == product_id).execute()


# Met onderstaande functie wordt de verkoop van een product tussen de koper en verkoper geregeld voor een bepaald product. 
# Ten eerste wordt er een transactie aangemaakt in de tabel 'Transaction', omdat er natuurlijk een transactie plaatsvindt tussen koper en verkoper. 
# Ten tweede wordt het product toegevoegd aan de gebruiker door het aanroepen van een eerder gedefinieerde functie. 
# Als laatste moet het aantal verkochte producten natuurlijk uit de inventaris worden gehaald, om dit te doen heb ik vlak hierboven een functie gedefinieerd genaamd 'remove_product_from_stock'.

def purchase_product(product_id, user_id, quantity):
    """Handle a purchase between a buyer 
    and a seller for a given product"""
    Transaction.create(user_id=user_id)
    product=(Product.select(Product.product_name) .where(Product.product_id==product_id))
    add_product_to_user(user_id, product, quantity)
    remove_product_from_stock(product, quantity)





# Onderstaande functies zijn extra hulpfuncties om: 
# 1) Nieuwe producten toe te voegen aan de inventaris (in de Product tabel). 
# 2) De bijbehorende tag aan te maken (indien deze tag nog niet bestaat) (in de Tag tabel). 
# 3) Het product te linken aan de bijbehorende tag (in de ProductTag tabel).
def new_tag(tag):
    query= (Tag.select().where((Tag.tag==tag)))
    already_exists = query.count()
    if already_exists == 0:
        Tag.create(tag=tag)





def add_new_product(product_name, description, price_unit, quantity, tag):
    new_tag(tag)
    tag_id= (Tag.select(Tag.tag_id).where((Tag.tag==tag))).scalar()
    Product.create(product_name=product_name, description=description, price_unit=price_unit, quantity_in_stock=quantity)
    product_id=(Product.select(Product.product_id) .where(Product.product_name==product_name))
    ProductTags.create(product_id=product_id, tag=tag_id)






