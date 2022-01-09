from dataclasses import dataclass
from data.models.food_model import FoodModel


@dataclass
class OrderModel:
    id: str
    user_id: str | None
    food_id: int | None
    order_quantity: int | None
    already_paid: bool | None
    food: FoodModel | None

    def from_dict(data):
        return OrderModel(
            data['id'],
            data['user_id'],
            data['food_id'],
            data['order_quantity'],
            bool(data['already_paid']),
            FoodModel.from_dict(data)
        )
