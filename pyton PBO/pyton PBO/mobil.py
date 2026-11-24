from abc import ABC, abstractmethod


# =========================
# ABSTRACTION
# =========================
class Kendaraan(ABC):

    def __init__(self, merek, tahun):
        # =========================
        # ENCAPSULATION
        # =========================
        self.__merek = merek
        self.__tahun = tahun

    # Mengakses merek
    @property
    def merek(self):
        return self.__merek

    # Mengubah merek
    @merek.setter
    def merek(self, value):
        self.__merek = value

    # Mengakses tahun
    @property
    def tahun(self):
        return self.__tahun

    # Mengubah tahun
    @tahun.setter
    def tahun(self, value):
        self.__tahun = value

    # Aturan yang harus dimiliki setiap Kendaraan
    @abstractmethod
    def suara(self):
        pass

    @abstractmethod
    def deskripsi(self):
        pass


# =========================
# INHERITANCE
# =========================
class Mobil(Kendaraan):

    # =========================
    # POLYMORPHISM
    # =========================
    def suara(self):
        return "Tin tin!"

    def deskripsi(self):
        return f"{self.merek} adalah mobil keluaran tahun {self.tahun}"


class Motor(Kendaraan):

    # =========================
    # POLYMORPHISM
    # =========================
    def suara(self):
        return "Brmm brmm!"

    def deskripsi(self):
        return f"{self.merek} adalah motor keluaran tahun {self.tahun}"


# =========================
# OBJECT
# =========================
mobil = Mobil("Toyota Avanza", 2022)
motor = Motor("Honda Vario", 2020)


print(mobil.deskripsi())
print(mobil.suara())

print(motor.deskripsi())
print(motor.suara())