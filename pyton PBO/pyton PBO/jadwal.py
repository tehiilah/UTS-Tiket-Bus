from datetime import datetime

from bus import Bus
from exceptions import KursiSudahDipesanError, KursiTidakValidError
from rute import Rute


class Jadwal:
    """Satu keberangkatan: rute + bus + waktu, sekaligus pengelola kursi yang terisi."""

    def __init__(self, kode, rute, bus, berangkat):
        self.kode = kode
        self.rute = rute
        self.bus = bus
        self.berangkat = berangkat
        self.__kursi_terisi = set()

    @property
    def kode(self):
        return self.__kode

    @kode.setter
    def kode(self, nilai):
        if not isinstance(nilai, str):
            raise TypeError(f"Kode jadwal harus berupa teks, bukan {type(nilai).__name__}")
        if not nilai.strip():
            raise ValueError("Kode jadwal tidak boleh kosong")
        self.__kode = nilai.strip().upper()

    @property
    def rute(self):
        return self.__rute

    @rute.setter
    def rute(self, nilai):
        if not isinstance(nilai, Rute):
            raise TypeError(f"rute harus berupa objek Rute, bukan {type(nilai).__name__}")
        self.__rute = nilai

    @property
    def bus(self):
        return self.__bus

    @bus.setter
    def bus(self, nilai):
        if not isinstance(nilai, Bus):
            raise TypeError(f"bus harus berupa objek Bus, bukan {type(nilai).__name__}")
        self.__bus = nilai

    @property
    def berangkat(self):
        return self.__berangkat

    @berangkat.setter
    def berangkat(self, nilai):
        if not isinstance(nilai, datetime):
            raise TypeError(
                f"Waktu berangkat harus berupa datetime, bukan {type(nilai).__name__}"
            )
        self.__berangkat = nilai

    @property
    def kursi_terisi(self):
        return frozenset(self.__kursi_terisi)

    def kursi_tersedia(self):
        return [n for n in range(1, self.bus.kapasitas + 1) if n not in self.__kursi_terisi]

    def pesan_kursi(self, nomor):
        """Tandai kursi terisi. Aturan: nomor harus 1..kapasitas dan belum terisi."""
        if isinstance(nomor, bool) or not isinstance(nomor, int) \
                or not 1 <= nomor <= self.bus.kapasitas:
            raise KursiTidakValidError(nomor, self.bus.kapasitas)
        if nomor in self.__kursi_terisi:
            raise KursiSudahDipesanError(nomor, self.kode)
        self.__kursi_terisi.add(nomor)

    def lepas_kursi(self, nomor):
        self.__kursi_terisi.discard(nomor)

    def __str__(self):
        return f"{self.kode} | {self.rute} | {self.berangkat:%d-%m-%Y %H:%M} | {self.bus}"
