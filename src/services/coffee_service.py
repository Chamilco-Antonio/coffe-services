from .inventory_service import InventoryService
from ..database.models import Pedido, Receta, TipoCafe
from random import randint

class CoffeeService:
    def __init__(self, session):
        self.session = session

    def obtener_receta(self, cafe_id: int):
        return self.session.query(Receta).filter_by(cafe_id=cafe_id).all()

    def _cantidad_agua_por_tipocafe(self, cafe_id: int):
        tipo_cafe = self.session.query(TipoCafe).filter_by(cafe_id=cafe_id).first()
        if tipo_cafe:
            return randint(tipo_cafe.min_agua, tipo_cafe.max_agua)
        return 50 # crear una posible excepción

    def _consumo_ingredientes_por_cafe(self, cafe_id: int, cantidades: list):
        receta = self.obtener_receta(cafe_id) # lista de ingredientes
        inventory_service = InventoryService(session=self.session)
        umbrales_minimos = []

        for indice, ingrediente in enumerate(receta):
            id_ingrediente = ingrediente.ingrediente_id
            consumo_ingrediente = inventory_service.comprobar_umbral_ingrediente(id_ingrediente, cantidades[indice])
            umbrales_minimos.append(consumo_ingrediente["status"])

        if not "failed" in umbrales_minimos:
            for indice, ingrediente in enumerate(receta):
                id_ingrediente = ingrediente.ingrediente_id
                inventory_service.restar_ingredientes(id_ingrediente, cantidades[indice])
            return {"status":"success", "messages":"OK"}
        else:
            return {"status":"failed", "messages":"Recargue los insumos."}


    def preparacion_cafe(self, cafe_id: int, cantidad_azucar: int = 0):
        pass
