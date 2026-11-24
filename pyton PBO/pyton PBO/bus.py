class Bus:
    """Armada bus dengan plat nomor, kapasitas kursi, dan kelas layanan."""

    KELAS_VALID = ("Ekonomi", "Bisnis", "Eksekutif")
    KAPASITAS_MAKS = 60

    def __init__(self, plat, kapasitas, kelas):
        self.plat = plat
        self.kapasitas = kapasitas
        self.kelas = kelas

    @property
    def plat(self):
        return self.__plat

    @plat.setter
    def plat(self, nilai):
        if not isinstance(nilai, str):
            raise TypeError(f"Plat nomor harus berupa teks, bukan {type(nilai).__name__}")
        if not nilai.strip():
            raise ValueError("Plat nomor tidak boleh kosong")
        self.__plat = nilai.strip().upper()

    @property
    def kapasitas(self):
        return self.__kapasitas

    @kapasitas.setter
    def kapasitas(self, nilai):
        if isinstance(nilai, bool) or not isinstance(nilai, int):
            raise TypeError(f"Kapasitas harus berupa bilangan bulat, bukan {type(nilai).__name__}")
        if not 1 <= nilai <= Bus.KAPASITAS_MAKS:
            raise ValueError(
                f"Kapasitas harus di antara 1 dan {Bus.KAPASITAS_MAKS}, diberikan {nilai}"
            )
        self.__kapasitas = nilai

    @property
    def kelas(self):
        return self.__kelas

    @kelas.setter
    def kelas(self, nilai):
        if nilai not in Bus.KELAS_VALID:
            raise ValueError(
                f"Kelas bus harus salah satu dari {', '.join(Bus.KELAS_VALID)}, diberikan {nilai!r}"
            )
        self.__kelas = nilai

    def __str__(self):
        return f"{self.plat} ({self.kelas}, {self.kapasitas} kursi)"
