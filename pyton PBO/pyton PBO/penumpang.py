class Penumpang:
    """Penumpang bus yang diidentifikasi dengan NIK 16 digit."""

    def __init__(self, nik, nama, usia):
        self.nik = nik
        self.nama = nama
        self.usia = usia

    @property
    def nik(self):
        return self.__nik

    @nik.setter
    def nik(self, nilai):
        if not isinstance(nilai, str):
            raise TypeError(f"NIK harus berupa teks, bukan {type(nilai).__name__}")
        if not (nilai.isascii() and nilai.isdigit() and len(nilai) == 16):
            raise ValueError(f"NIK harus terdiri dari 16 digit angka, diberikan {nilai!r}")
        self.__nik = nilai

    @property
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, nilai):
        if not isinstance(nilai, str):
            raise TypeError(f"Nama harus berupa teks, bukan {type(nilai).__name__}")
        if not nilai.strip():
            raise ValueError("Nama penumpang tidak boleh kosong")
        self.__nama = nilai.strip().title()

    @property
    def usia(self):
        return self.__usia

    @usia.setter
    def usia(self, nilai):
        if isinstance(nilai, bool) or not isinstance(nilai, int):
            raise TypeError(f"Usia harus berupa bilangan bulat, bukan {type(nilai).__name__}")
        if not 0 <= nilai <= 120:
            raise ValueError(f"Usia harus di antara 0 dan 120, diberikan {nilai}")
        self.__usia = nilai

    def __str__(self):
        return f"{self.nama} (NIK {self.nik})"
