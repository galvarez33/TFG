import uuid
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear un motor de base de datos (SQLite en este caso)
engine = create_engine('sqlite:///productos.db', echo=True)

# Declarar una clase base para nuestras clases de modelo
Base = declarative_base()

# Definir la clase del modelo (usando herencia de Base)
class Product(Base):
    __tablename__ = 'productos'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True)
    name = Column(String)
    price = Column(Float)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una instancia de la clase Product con un nuevo UUID
new_product = Product(name="Producto Ejemplo", price=29.99)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Añadir el nuevo producto a la sesión
session.add(new_product)

# Confirmar la transacción
session.commit()

# Consultar todos los productos
productos = session.query(Product).all()
for producto in productos:
    print(f"ID: {producto.id}, Nombre: {producto.name}, Precio: {producto.price}")

# Cerrar la sesión
session.close()
