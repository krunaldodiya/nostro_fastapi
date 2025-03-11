import os
import MT5Manager


class Manager:
    def __init__(self):
        self.client = MT5Manager.ManagerAPI()

        self.mt5_server = os.getenv("MT5_SERVER")
        self.mt5_login = int(os.getenv("MT5_LOGIN"))
        self.mt5_password = os.getenv("MT5_PASSWORD")

    def connect(self):
        try:
            assert isinstance(self.mt5_server, str), "mt5_server must be a string"
            assert isinstance(self.mt5_login, int), "mt5_server must be an integer"
            assert isinstance(self.mt5_password, str), "mt5_server must be a string"

            response = self.client.Connect(
                self.mt5_server,
                self.mt5_login,
                self.mt5_password,
                MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_FULL,
                30000,
            )

            if not response:
                raise Exception(MT5Manager.LastError())
        except Exception as e:
            raise e

    def disconnect(self):
        try:
            self.client.Disconnect()
        except Exception as e:
            raise e
