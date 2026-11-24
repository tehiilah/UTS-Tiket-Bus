from datetime import datetime, timedelta

from exceptions import PembatalanDitolakError
from jadwal import Jadwal
from penumpang import Penumpang


class Tiket:
    """Tiket milik satu penumpang untuk satu kursi pada satu jadwal."""

    AKTIF = "AKTIF"
    DIBATALKAN = "DIBATALKAN"
    BATAS_PEMBATALAN = timedelta(hours=3)

    def __init__(self, kode, jadwal, penumpang, nomor_kursi):
        self.kode = kode
        self.jadwal = jadwal
        self.penumpang = penumpang
        self.nomor_kursi = nomor_kursi
        self.__status = Tiket.AKTIF

    @property
    def kode(self):
        return self.__kode

    @kode.setter
    def kode(self, nilai):
        if not isinstance(nilai, str):
            raise TypeError(f"Kode tiket harus berupa teks, bukan {type(nilai).__name__}")
        if not nilai.strip():
            raise ValueError("Kode tiket tidak boleh kosong")
        self.__kode = nilai.strip().upper()

    @property
    def jadwal(self):
        return self.__jadwal

    @jadwal.setter
    def jadwal(self, nilai):
        if not isinstance(nilai, Jadwal):
            raise TypeError(f"jadwal harus berupa objek Jadwal, bukan {type(nilai).__name__}")
        self.__jadwal = nilai

    @property
    def penumpang(self):
        return self.__penumpang

    @penumpang.setter
    def penumpang(self, nilai):
        if not isinstance(nilai, Penumpang):
            raise TypeError(
                f"penumpang harus berupa objek Penumpang, bukan {type(nilai).__name__}"
            )
        self.__penumpang = nilai

    @property
    def nomor_kursi(self):
        return self.__nomor_kursi

    @nomor_kursi.setter
    def nomor_kursi(self, nilai):
        if isinstance(nilai, bool) or not isinstance(nilai, int):
            raise TypeError(f"Nomor kursi harus berupa bilangan bulat, bukan {type(nilai).__name__}")
        if nilai < 1:
            raise ValueError(f"Nomor kursi minimal 1, diberikan {nilai}")
        self.__nomor_kursi = nilai

    @property
    def status(self):
        return self.__status

    @property
    def harga(self):
        return self.jadwal.rute.harga

    def batalkan(self, sekarang):
        """Batalkan tiket. Aturan: belum dibatalkan dan minimal 3 jam sebelum berangkat."""
        if not isinstance(sekarang, datetime):
            raise TypeError(f"sekarang harus berupa datetime, bukan {type(sekarang).__name__}")
        if self.__status == Tiket.DIBATALKAN:
            raise PembatalanDitolakError(self.kode, "tiket sudah dibatalkan sebelumnya")
        if self.jadwal.berangkat - sekarang < Tiket.BATAS_PEMBATALAN:
            raise PembatalanDitolakError(
                self.kode,
                "pembatalan hanya bisa dilakukan minimal 3 jam sebelum keberangkatan",
            )
        self.__status = Tiket.DIBATALKAN
        self.jadwal.lepas_kursi(self.nomor_kursi)

    def __str__(self):
        harga = f"{self.harga:,.0f}".replace(",", ".")
        return (
            f"{self.kode} | {self.penumpang.nama} | {self.jadwal.rute} | "
            f"kursi {self.nomor_kursi} | Rp{harga} | {self.status}"
        )
