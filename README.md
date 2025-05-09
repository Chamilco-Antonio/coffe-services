## Cómo Ejecutar

1.  **Clonar el repositorio**
2.  **Navegar al directorio del proyecto.**
3.  **Crear un entorno virtual**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate  # En Windows
    ```
4.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```

## Flujo de la Aplicación

1.  Al ejecutar `main.py`, se verifica la existencia de la base de datos (`coffee.db`). Si no existe, se crea y se inicializan las tablas con datos predeterminados.
2.  Se presenta al usuario un menú principal con opciones para la "Gestión" del inventario o para "Salir".
3.  Si algún ingrediente necesita ser reabastecido (cantidad actual por debajo de la cantidad mínima), el usuario es dirigido al menú de gestión.
4.  En el menú de gestión, el usuario puede seleccionar qué ingrediente reabastecer.
5.  Si el inventario está en niveles suficientes, el usuario puede acceder al menú de compra.
6.  En el menú de compra, el usuario elige un tipo de café.
7.  Se le pregunta al usuario la cantidad de azúcar que desea.
8.  El sistema verifica si hay suficientes ingredientes para preparar el café.
9.  Si los ingredientes están disponibles, se descuentan del inventario, se informa al usuario y se registra el pedido en la base de datos.
10. El usuario puede seguir comprando o volver al menú principal hasta que elige la opción de "Salir".

## Tecnologías Utilizadas

-   **Python**: El lenguaje de programación principal.
-   **SQLAlchemy**: Un potente Object Relational Mapper (ORM) para interactuar con la base de datos SQLite de manera orientada a objetos.
-   **SQLite**: Una base de datos ligera y autónoma utilizada para persistir los datos de la máquina de café.

## Convenciones de Código

-   **CamelCase**: Se utiliza para nombrar las clases (e.g., `CoffeeService`, `TipoCafe`).
-   **snake\_case**: Se utiliza para nombrar las funciones y las variables (e.g., `obtener_receta`, `cantidad_agua`).
-   **Docstrings**: Todas las clases y métodos están documentados con Docstrings descriptivos que explican su propósito, parámetros y valores de retorno, facilitando la comprensión y el mantenimiento del código.

