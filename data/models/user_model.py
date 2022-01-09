from dataclasses import dataclass


@dataclass
class UserModel:
    id: str
    email: str
    password: str
    is_admin: bool

    def from_dict(data):
        return UserModel(data['id'], data['email'], data['password'], bool(data['is_admin']))
