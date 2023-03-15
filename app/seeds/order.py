from app.models import db, Product, Order, environment, SCHEMA, Cart, cartJoined, orderJoined
import datetime
from sqlalchemy.sql import text
from random import choice

def seed_order():
    products = Product.query.all()
    order1 = Order(
        user_id= 1, date="03/05/2023", products=[choice(products)]
    )
    order2 = Order(
        user_id= 2, date="06/05/2023", products=[choice(products)]
    )
    order3 = Order(
        user_id= 3, date="07/05/2023", products=[choice(products)]
    )

    db.session.add(order1)
    db.session.add(order2)
    db.session.add(order3)
    db.session.commit()

    for order in [order1, order2, order3]:
        for product in order.product:
            orderjoined = orderJoined(
                user_id = order.user_id,
                product_id = product.id,
                order_id = order.id
            )
            db.session.add(orderjoined)
            db.session.commit()

    print("Cart items seeded successfully!")

def undo_order():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.order RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM order"))

    db.session.commit()
