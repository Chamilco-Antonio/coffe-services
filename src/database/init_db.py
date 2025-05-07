from .connection import engine
from .models import Base, Ingrediente, Inventario, TipoCafe, Receta
from sqlalchemy.orm import Session

def init_db():
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    # Insertar ingredientes
    ingredientes_iniciales = [
        Ingrediente(nombre_ingrediente="Cartucho de Café", unidad_medida="unidad"),  # ID 1
        Ingrediente(nombre_ingrediente="Azúcar", unidad_medida="gr"), # ID 2
        Ingrediente(nombre_ingrediente="Agua", unidad_medida="ml") # ID 3
    ]
    session.add_all(ingredientes_iniciales)
    session.commit()
    #print("Ingredientes iniciales insertados.")

    # Insertar inventario 
    inventario_inicial = [
        Inventario(ingrediente_id=1, capacidad_maxima=10, cantidad_minima=1, cantidad_actual=5), # Cartucho de Café
        Inventario(ingrediente_id=2, capacidad_maxima=100, cantidad_minima=10, cantidad_actual=5), # Azúcar
        Inventario(ingrediente_id=3, capacidad_maxima=1000, cantidad_minima=200, cantidad_actual=100) # Agua
    ]
    session.add_all(inventario_inicial)
    session.commit()
    #print("Inventario inicial insertado.")

    # Insertar tipos de café
    tipos_cafe_iniciales = [
        TipoCafe(nombre="Expreso", descripcion="Café concentrado y aromático con un cuerpo intenso y una capa de crema dorada.", min_agua=50, max_agua=60), # ID 1
        TipoCafe(nombre="Capuchino", descripcion="Café con espuma de leche cremosa y suave.", min_agua=45, max_agua=55), # ID 2
        TipoCafe(nombre="Mocaccino", descripcion="Café con chocolate, espuma de leche cremosa y un toque de cacao o chocolate rallado", min_agua=40, max_agua=50) # ID 3
    ]
    session.add_all(tipos_cafe_iniciales)
    session.commit()
    #print("Tipos de café iniciales insertados.")

    # Insertar recetas
    recetas_iniciales = [
        # Expreso (ID 1): 1 cartucho, agua, azúcar
        Receta(cafe_id=1, ingrediente_id=1, cantidad=1, es_agua=False),
        Receta(cafe_id=1, ingrediente_id=2, cantidad=1, es_agua=False),
        Receta(cafe_id=1, ingrediente_id=3, cantidad=1, es_agua=False),
        # Capuchino (ID 2): 1 cartucho, agua, azúcar
        Receta(cafe_id=2, ingrediente_id=1, cantidad=1, es_agua=False),
        Receta(cafe_id=2, ingrediente_id=3, cantidad=None, es_agua=True),
        Receta(cafe_id=2, ingrediente_id=2, cantidad=None, es_agua=False),
        # Mocaccino (ID 3): 1 cartucho, agua, azúcar
        Receta(cafe_id=3, ingrediente_id=1, cantidad=1, es_agua=False),
        Receta(cafe_id=3, ingrediente_id=3, cantidad=None, es_agua=True),
        Receta(cafe_id=3, ingrediente_id=2, cantidad=None, es_agua=False)
    ]
    session.add_all(recetas_iniciales)
    session.commit()
    #print("Recetas iniciales insertadas.")

    session.close()

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada y datos insertados.")