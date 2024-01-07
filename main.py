import sqlite3
import random

DATA_AMOUNT = 500_000 + 1

START_CART_ID = 9
END_CART_ID = 500_008

START_PRODUCT_ID = 2
END_PRODUCT_ID = 500_002

COLORS = [
    "Черный",
    "Белый",
    "Красный",
    "Оранжевый",
    "Желтые",
    "Зеленый",
    "Синий",
    "Голубой",
    "Фиолетовый",
    "Розовый",
    "Березевый",
    "Телесный",
    "Пурпуровый",
]
BRANDS = [
    "Addidas",
    "Nike",
    "Puma",
    "Gucci",
    "Balenciaga",
    "Columbia",
    "Crocs",
    "New Balance",
    "Skechers",
    "The North Face",
    "Timberland",
    "Vans",
    "Wilson",
    "Wrangler",
    "Armani",
]

def load_carts(connection: sqlite3.Connection) -> None:
    carts = [
        (random.randrange(0, 1 + 1), random.randrange(0, 1 + 1))
        for i in range(1, DATA_AMOUNT)
    ]

    sql = "INSERT INTO Cart (IsPaid, IsPromoApplied) VALUES (?, ?)"
    connection.executemany(sql, carts)
    connection.commit()

def load_categories(connection: sqlite3.Connection) -> None:
    categories = [
        ("Кроссовки", ),
        ("Ботинки", ),
        ("Туфли", ),
        ("Макасины", ),
        ("Каблуки", ),
        ("Тапочки", ),
        ("Кроксы", ),
        ("Сапоги", ),
        ("Сандали", ),
    ]

    sql = "INSERT INTO Category (Title) VALUES (?)"
    connection.executemany(sql, categories)
    connection.commit()

def load_properties(connection: sqlite3.Connection) -> None:
    properties = [
        (random.choice(COLORS), random.randrange(34, 46 + 1))
        for _ in range(1, DATA_AMOUNT)
    ]

    sql = "INSERT INTO Property (Color, Size) VALUES (?, ?)"
    connection.executemany(sql, properties)
    connection.commit()

def load_cart_products(connection: sqlite3.Connection) -> None:
    cartProducts = [
        (random.randrange(START_CART_ID, END_CART_ID), random.randrange(START_PRODUCT_ID, END_PRODUCT_ID))
        for _ in range(0, DATA_AMOUNT)
    ]

    sql = "INSERT INTO CartProducts (CartID, ProductID) VALUES (?, ?)"
    connection.executemany(sql, cartProducts)
    connection.commit()

def load_products(connection: sqlite3.Connection) -> None:
    products = []

    title_generator = lambda brandTitle, categoryTitle:  f"{categoryTitle} - {brandTitle}"
    description_generator = lambda brandTitle, categoryTitle, color, size, price: (f"Новые {categoryTitle.lower()}, отличного качества от бренда - {brandTitle}. "
                                                               f"Размер - {size} | Цвет - {color.lower()} | Цена - {price} рублей")


    for i in range(0, DATA_AMOUNT):
        categoryID = random.randrange(6, 14 + 1)
        propertyID = random.randrange(1, DATA_AMOUNT)
        brandIndex = random.randrange(0, len(BRANDS))
        price = float(random.randrange(1000, 100000 + 1, random.randrange(100, 1000 + 1)))

        categoryTitle = connection.execute("SELECT Title FROM Category WHERE ID = ?", (categoryID, )).fetchone()[0]
        color, size = connection.execute("SELECT Color, Size FROM Property WHERE ID = ?", (propertyID, )).fetchone()

        products.append((
            categoryID, propertyID, BRANDS[brandIndex],
            title_generator(BRANDS[brandIndex], categoryTitle),
            description_generator(BRANDS[brandIndex], categoryTitle, color, size, price),
            price
        ))

    sql = "INSERT INTO Product (CategoryID, PropertyID, Brand, Title, Description, Price) VALUES (?, ?, ?, ?, ?, ?)"
    connection.executemany(sql, products)
    connection.commit()

def load_users(connection: sqlite3.Connection) -> None:
    users = [
        (f"test{i}", f"test{i}", f"test{i}@example.com", random.randrange(0, 1 + 1), START_CART_ID + i)
        for i in range(0, DATA_AMOUNT - 1)
    ]

    sql = "INSERT INTO User (Login, Password, Email, IsEmailVerified, CartID) VALUES (?, ?, ?, ?, ?)"
    connection.executemany(sql, users)
    connection.commit()

def main() -> None:
    connection = sqlite3.connect("./shop.db")

    load_carts(connection)
    load_users(connection)
    load_categories(connection)
    load_properties(connection)
    load_products(connection)
    load_cart_products(connection)

    connection.close()

if __name__ == "__main__":
    main()
