import requests
from models import CryptoWatcherModel, UserModel


class CryptoWatcherService:
    def __init__(self):
        self.model = CryptoWatcherModel()

    def create(self, params):
        return self.model.create(params)

    def update(self, item_id, params):
        return self.model.update(item_id, params)

    def delete(self, item_id, params):
        return self.model.delete(item_id, params)

    def list(self, user_id):
        response = self.model.list_items(user_id)
        # Check if accountAddress needs to be updated
        # (only works for XRP currently)
        for coin in response:
            if coin.get("name") == "XRP" and coin.get("accountAddress") is not None:
                print("Checking account balance against ledger...")
                get_balance = requests.get(f"https://api.xrpscan.com/api/v1/account/{coin.get('accountAddress')}")
                if get_balance.json()['xrpBalance']:
                    # Removes decimals for the moment
                    coin['amountHeld'] = get_balance.json()['xrpBalance'].split(".")[0]
        return response

    def get_by_id(self, item_id):
        response = self.model.get_by_id(item_id)
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
