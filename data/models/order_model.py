from dataclasses import dataclass
from data.models.food_model import FoodModel


@dataclass
class OrderModel:
    id: str
    user_id: str
    food_id: int
    order_quantity: int
    already_paid: bool
    food: FoodModel

    def from_dict(data):
        return OrderModel(
            data['id'],
            data['user_id'],
            data['food_id'],
            data['order_quantity'],
            bool(data['already_paid']),
            FoodModel.from_dict(data)
        )
