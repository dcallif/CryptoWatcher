import requests
from models import CryptoWatcherModel, UserModel


class CryptoWatcherService:
    def __init__(self):
        self.model = CryptoWatcherModel()

    def create(self, params):
        return self.model.create(params)

    def update(self, item_id, user_id, params):
        return self.model.update(item_id, user_id, params)

    def delete(self, item_id, params):
        return self.model.delete(item_id, params)

    def list(self, user_id):
        response = self.model.list_items(user_id)
        return response

    def get_by_id(self, item_id):
        response = self.model.get_by_id(item_id)
        return response

    def get_token(self, item_id, user_id):
        response = self.model.get_token(item_id, user_id)
        return response


class UserService:
    def __init__(self):
        self.model = UserModel()

    def create(self, email, name, password):
        return self.model.create(email, name, password)

    def update(self, item_id, params):
        return self.model.update(item_id, params)

    def delete(self, item_id):
        return self.model.delete(item_id)

    def list(self):
        response = self.model.list_items()
        return response

    def get_by_id(self, item_id):
        response = self.model.get_by_id(item_id)
        return response

    def get_by_email(self, email):
        response = self.model.get_by_email(email)
        return response
