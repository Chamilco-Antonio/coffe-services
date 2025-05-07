from ..database.models import Inventario 

class InventoryService:
    def __init__(self, session):
        self.session = session

    def _obtener_ingrediente(self, ingrediente_id: int):
        """Obtener el registro del inventario de un ingrediente"""
        return self.session.query(Inventario).filter_by(ingrediente_id=ingrediente_id).first()

    def cantidad_minima_ingrediente(self, ingrediente_id: int) -> bool:
        """Verifica si la cantidad de un ingrediente supera o iguala el
        umbral mínimo"""
        inventario = self._obtener_ingrediente(ingrediente_id)
        if inventario:
            return inventario.cantidad_actual >= inventario.cantidad_minima
        return False

    def comprobar_umbral_ingrediente(self, ingrediente_id: int, cantidad: int):
        """Hace las comprobaciones para comprobar que los ingredientes 
        tienen las cantidades minimas."""
        inventario = self._obtener_ingrediente(ingrediente_id)
        if inventario:
            comprobar_cantidad = (inventario.cantidad_actual - cantidad) >= inventario.cantidad_minima # Asegurar que el requerimiento del umbral se cumpla
            if not comprobar_cantidad:
                return {"status": "failed","messages": f"No hay suficiente {inventario.ingrediente.ingrediente_nombre}, solo se dispone de {inventario.cantidad_actual} {inventario.ingrediente.unidad_medida}. Recargue los insumos."}
            return {"status":"success", "messages": "Umbral minimo cumplido"}     
        return {"status":"failed", "messages": "Ingrediente no encontrado"} 

    def restar_ingredientes(self, ingrediente_id, cantidad: int):
        inventario = self._obtener_ingrediente(ingrediente_id)
        inventario.cantidad_actual  = inventario.cantidad_actual - cantidad
        self.session.commit()
        return {"status": "success", "messages":"Ingrediente consumido"}

    def reabastecer_ingrediente(self, ingrediente_id: int) -> dict:
        """Reabastece completamente el inventario de un ingrediente a su capacidad máxima."""
        inventario = self._obtener_ingrediente(ingrediente_id)
        if inventario:
            inventario.cantidad_actual = inventario.capacidad_maxima
            self.session.commit()
            return {"status":"success", "messages": f"{inventario.ingrediente.nombre_ingrediente} reabastecido completamente"}
        return {"status":"failed", "messages": "Ingrediente no encontrado"}