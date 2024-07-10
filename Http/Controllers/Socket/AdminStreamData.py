from Models.main import ModelMain

class AdminStreamData(ModelMain):
    def __init__(self):
        self.collection = self.mongo_client[self.db_name][self.room_collection]

    def stream_user_list(self):
        collection = self.collection

