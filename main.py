from src.services.inventory_service import InventoryService
from src.services.coffee_service import CoffeeService
from src.database.connection import engine
from sqlalchemy.orm import Session
from src.database.models import Pedido 
from src.database.init_db import init_db
from pathlib import Path
import os

def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_inicio():
    print(50*"-")
    print()
    print("1. Gestión")
    print("2. Salir")
    opcion = input("\nOpción [1, 2]: ")
    return opcion

def opcion_gestion(reabastecer: list):
    print(50*"-")
    print()
    print(f"1. Añadir cartuchos de café {reabastecer[0]}")
    print(f"2. Añadir azucar {reabastecer[1]}")
    print(f"3. Añadir agua {reabastecer[2]}")
    opcion = input("\nOpción [1, 3]: ")
    return opcion

def opcion_compra():
    print(50*"-")
    print("1. Comprar un Café Espresso")
    print("2. Comprar un Capuchno")
    print("3. Comprar un Mocaccino")
    print("4. Gestión")
    print("5. Salir")
    opcion = input("\nOpción [1, 5]: ")
    return opcion

def cantidad_azucar():
    print(50*"-")
    print("1. Nada")
    print("2. Algo")
    print("3. Medio")
    print("4. Bastante")
    print("5. Mucho")
    opcion = input("\nOpción [1, 5]: ")
    return opcion

def main():
    session = Session(engine)
    inventario_servicio = InventoryService(session=session)
    coffee_servicio = CoffeeService(session=session)
    CANTIDAD_OPCIONES = 3 # LA cantidad de opciones == cantidad ingredientes

    while True: # convertir un una variable booleana para que la opción 2 termine el bucle por parte del menu_inicio()
        # Lógica para el reabastecimiento y restricción
        lista_reabastecimiento = [] # capturar ingredientes a reabastecer
        restablecer = "(Reabastecer)"
        for opcion in range(1, CANTIDAD_OPCIONES+1):
            # Indicar que ingredientes serán restablecidos
            if not inventario_servicio.cantidad_minima_ingrediente(opcion):
                lista_reabastecimiento.append(restablecer)
            else:
                lista_reabastecimiento.append("")
            
        # Comprobar si la lógica de restablecimiento se aplicara o no
        necesita_reabastecer = restablecer in lista_reabastecimiento
        if not necesita_reabastecer: ### LOGICA DE COMPRAS DE CAFE ###
            limpiar_terminal()
            mostrar_opcion_comprar = opcion_compra()
            # Asegurar la entrada del usuario
            if mostrar_opcion_comprar in ('1', '2', '3'):
                cafe_id = int(mostrar_opcion_comprar) # obtener id_cafe por la opción del usuario
                # Asegurar la integridad de todas maneras con una consulta de receta
                receta = coffee_servicio.obtener_receta(cafe_id)
                if not receta:
                    print("No se encontró la receta para este café.")
                    input("Presione Enter para continuar...")
                    continue
                # Determinar la cantidad de agua
                cantidad_agua = coffee_servicio._cantidad_agua_por_tipocafe(cafe_id)
                if cantidad_agua is None:
                    print("No se encontró la información del tipo de café.")
                    input("Presione Enter para continuar...")
                    continue

                ### OBTENER CANTIDAD DE AZUCAR SEGÚN EL USUARIO
                opcion_azucar = cantidad_azucar()
                cantidad_azucar_usuario = 0
                match opcion_azucar:
                    case '2': cantidad_azucar_usuario = 5
                    case '3': cantidad_azucar_usuario = 10
                    case '4': cantidad_azucar_usuario = 15
                    case '5': cantidad_azucar_usuario = 20
                    case '_': cantidad_azucar_usuario = 0

                # 1 -> cartuchos, 2 -> azucar, 3 -> agua
                cantidades_a_consumir = [1, cantidad_azucar_usuario, cantidad_agua] # lista de cantidades a consumir

                # Intentar consumir los ingredientes
                resultado_consumo = coffee_servicio._consumo_ingredientes_por_cafe(cafe_id, cantidades_a_consumir)
                #print(resultado_consumo["messages"])
                if resultado_consumo["status"] == "success":
                    detalles_tipo_cafe = coffee_servicio.obtener_receta(cafe_id)
                    nombre = detalles_tipo_cafe[0].tipo_cafe.nombre
                    descripcion = detalles_tipo_cafe[0].tipo_cafe.descripcion

                    print(f"* {nombre}")
                    print(f"\t- Descripción: {descripcion}")
                    print(f"\t- Consumo:")
                    print(f"\t\t+ Agua: {cantidad_agua} ml")
                    print(f"\t\t+ Café: {1} cartucho")
                    print(f"\t\t+ Azucar: {cantidad_azucar_usuario} g")
                    print("¡Disfrute su café!")
                    
                    # REGISTRO A LA TABLA PEDIDOS
                    pedido = Pedido(
                        cafe_id=cafe_id,
                        cantidad_agua=cantidad_agua,
                        cantidad_azucar=cantidad_azucar_usuario
                    )
                    session.add(pedido)
                    session.commit()

                input("Presione Enter para continuar...")
            elif mostrar_opcion_comprar == '4':
                necesita_reabastecer = True
            elif mostrar_opcion_comprar == '5':
                print("¡Hasta luego!")
                break 
            else:
                print('Ingrese una opción correcta')
                input("Presione Enter para continuar...")
            
        else: # REABASTECIMIENTO DE INGREDIENTES
            # Asegurar que el usuairo ingrese una opción correcta
            while True:
                mostrar_menu_inicio = menu_inicio()
                if mostrar_menu_inicio in ('1', '2'): # ejecuta el reabastecimiento si coloco las opciones correctas
                    break  # agregar la validación de una variable booleana con while inicial
                print('Ingrese una opción correcta')

            if mostrar_menu_inicio == '2': continue # sale de la ejecución y vuelve al inicio
            # Ejecutar reabastecimiento
            mostrar_opcion_gestion = opcion_gestion(lista_reabastecimiento)
            # Gestionar ingreso de datos por el usuario
            if mostrar_opcion_gestion in ('1', '2', '3'):
                resultado = inventario_servicio.reabastecer_ingrediente(int(mostrar_opcion_gestion)) # Reabastecimiento
                print(resultado["messages"])
                input("Presione Enter para continuar...")
            else: 
                print('Ingrese una opción correcta')
                input("Presione Enter para continuar...")
                


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent
    DIRECCION_DB = BASE_DIR / "src" / "database" / "coffee.db"

    if not DIRECCION_DB.exists():
        init_db()

    main()
    

    