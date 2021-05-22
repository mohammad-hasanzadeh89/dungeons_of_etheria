from models.inventory import Inventory


class Shop:

    def __init__(self, id=0, name="shop", description="this a shop", commission=5, inventory=Inventory()):
        self.id = id
        self.name = name
        self.description = description
        self.commission = commission
        self.inventory = inventory

    def buy_from_shop(self, item, buyer):
        result = {
            "Log": []
        }
        if buyer.inventory.coin >= item.price:
            buyer.inventory.add_or_remove_coin(-item.price, result,
                                               buyer.character_type)
            self.inventory.add_or_remove_coin(item.price, {})

            buyer.inventory.add(item, result)
        else:
            result["Log"].append(("#ff0000", f"Not enough coin..."))

        return result

    def sell_to_shop(self, item, seller):
        result = {
            "Sold_item": item,
            "Log": []
        }
        seller.inventory.add_or_remove_coin(
            (item.price - self.commission), result, seller.character_type)
        seller.inventory.remove(item, result)
        return result

    def show_shop(self):
        result = {
            "Log": [
                ("#ffffff", f"--------------{self.name}--------------\n"),
                ("#ffffff", f"{self.description}\n"),
            ]
        }
        return result
