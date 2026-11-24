from exceptions import BatasTiketTerlampauiError, JadwalTidakDitemukanError, PembatalanDitolakError
from tiket import Tiket


class AgenTiket:
    """Agen penjualan: menyimpan jadwal dan tiket, serta menegakkan aturan pemesanan.

    Class ini tidak mencetak apa pun. Pelanggaran aturan bisnis dilaporkan
    lewat exception, dan lapisan program utama yang memutuskan tampilannya.
    """

    BATAS_TIKET_PER_PENUMPANG = 4

    def __init__(self, nama):
        self.nama = nama
        self.__jadwal = {}
        self.__tiket = {}
        self.__urutan = 0

    def tambah_jadwal(self, jadwal):
        self.__jadwal[jadwal.kode] = jadwal

    def cari_jadwal(self, kode_jadwal):
        try:
            return self.__jadwal[kode_jadwal]            # gaya EAFP
        except KeyError:
            raise JadwalTidakDitemukanError(kode_jadwal) from None

    def jumlah_tiket_aktif(self, nik, kode_jadwal):
        return sum(
            1
            for t in self.__tiket.values()
            if t.penumpang.nik == nik
            and t.jadwal.kode == kode_jadwal
            and t.status == Tiket.AKTIF
        )

    def pesan_tiket(self, kode_jadwal, penumpang, nomor_kursi):
        jadwal = self.cari_jadwal(kode_jadwal)            # JadwalTidakDitemukanError
        # Aturan murah diperiksa lebih dulu (LBYL) agar state tidak setengah jadi.
        if self.jumlah_tiket_aktif(penumpang.nik, jadwal.kode) >= AgenTiket.BATAS_TIKET_PER_PENUMPANG:
            raise BatasTiketTerlampauiError(penumpang.nik, AgenTiket.BATAS_TIKET_PER_PENUMPANG)
        jadwal.pesan_kursi(nomor_kursi)                   # KursiTidakValid / KursiSudahDipesan
        self.__urutan += 1                                # hanya naik jika kursi berhasil dipesan
        tiket = Tiket(f"TKT-{self.__urutan:04d}", jadwal, penumpang, nomor_kursi)
        self.__tiket[tiket.kode] = tiket
        return tiket

    def batalkan_tiket(self, kode_tiket, sekarang):
        try:
            tiket = self.__tiket[kode_tiket]              # gaya EAFP
        except KeyError:
            raise PembatalanDitolakError(kode_tiket, "tiket tidak ditemukan") from None
        tiket.batalkan(sekarang)                          # PembatalanDitolakError
        return tiket
