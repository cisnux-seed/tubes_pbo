from dataclasses import dataclass


@dataclass
class FoodModel:
    id: str
    name: str
    food_quantity: int
    price: int

    def from_dict(data):
        return FoodModel(data['id'], data['name'], data['food_quantity'], data['price'])

    def from_order_dict(data):
        return FoodModel(data['food_id'], data['name'], data['food_quantity'], data['price'])
