class Rute:
    """Rute perjalanan bus: kode, kota asal, kota tujuan, dan harga per kursi."""

    def __init__(self, kode, asal, tujuan, harga):
        self.kode = kode
        self.asal = asal
        self.tujuan = tujuan          # divalidasi terhadap asal
        self.harga = harga

    @property
    def kode(self):
        return self.__kode

    @kode.setter
    def kode(self, nilai):
        if not isinstance(nilai, str):
            raise TypeError(f"Kode rute harus berupa teks, bukan {type(nilai).__name__}")
        if not nilai.strip():
            raise ValueError("Kode rute tidak boleh kosong")
        self.__kode = nilai.strip().upper()

    @property
    def asal(self):
        return self.__asal

    @asal.setter
    def asal(self, nilai):
        if not isinstance(nilai, str):
            raise TypeError(f"Kota asal harus berupa teks, bukan {type(nilai).__name__}")
        if not nilai.strip():
            raise ValueError("Kota asal tidak boleh kosong")
        self.__asal = nilai.strip().title()

    @property
    def tujuan(self):
        return self.__tujuan

    @tujuan.setter
    def tujuan(self, nilai):
        if not isinstance(nilai, str):
            raise TypeError(f"Kota tujuan harus berupa teks, bukan {type(nilai).__name__}")
        if not nilai.strip():
            raise ValueError("Kota tujuan tidak boleh kosong")
        if nilai.strip().title() == self.asal:
            raise ValueError("Kota tujuan tidak boleh sama dengan kota asal")
        self.__tujuan = nilai.strip().title()

    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, nilai):
        if isinstance(nilai, bool) or not isinstance(nilai, (int, float)):
            raise TypeError(f"Harga harus berupa angka, bukan {type(nilai).__name__}")
        if nilai <= 0:
            raise ValueError(f"Harga harus lebih dari 0, diberikan {nilai}")
        self.__harga = nilai

    def __str__(self):
        return f"{self.kode}: {self.asal} - {self.tujuan}"
