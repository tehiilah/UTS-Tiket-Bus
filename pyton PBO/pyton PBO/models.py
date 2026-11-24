from exceptions import (
    DataTidakValidError,
    KursiTidakDitemukanError,
    KursiSudahDipesanError,
    PemesananTidakValidError,
)


class FasilitasMixin:
    """Mixin: menambah kemampuan menampilkan fasilitas."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fasilitas = []

    def daftar_fasilitas(self):
        return ", ".join(self._fasilitas)


class Bus:
    jumlah_bus = 0

    def __init__(self, plat_nomor, baris, kursi_kiri, kursi_kanan):
        if not plat_nomor or not plat_nomor.strip():
            raise DataTidakValidError("Plat nomor bus tidak boleh kosong")
        if baris <= 0 or kursi_kiri <= 0 or kursi_kanan <= 0:
            raise DataTidakValidError("Jumlah baris dan konfigurasi kursi harus lebih dari 0")
        if (kursi_kiri + kursi_kanan) > 8:
            raise DataTidakValidError("Total kursi per baris maksimal 8 (A-H)")

        self.__plat_nomor = plat_nomor.strip()
        self._baris = baris
        self._kursi_kiri = kursi_kiri
        self._kursi_kanan = kursi_kanan
        Bus.jumlah_bus += 1

    @property
    def plat_nomor(self):
        return self.__plat_nomor

    @property
    def kapasitas(self):
        return self._baris * (self._kursi_kiri + self._kursi_kanan)

    def daftar_label_kursi(self):
        huruf = "ABCDEFGH"[: self._kursi_kiri + self._kursi_kanan]
        return [f"{b}{h}" for b in range(1, self._baris + 1) for h in huruf]

    def hitung_tarif(self, tarif_dasar):
        return tarif_dasar

    def info_konfigurasi(self):
        return f"Bus {self.__plat_nomor}, {self.kapasitas} kursi"


class BusEksekutif(FasilitasMixin, Bus):
    def __init__(self, plat_nomor, baris):
        super().__init__(plat_nomor, baris, 2, 2)
        self._fasilitas = ["AC", "Reclining seat", "Toilet"]

    def hitung_tarif(self, tarif_dasar):
        return int(tarif_dasar * 1.5)

    def info_konfigurasi(self):
        return (
            f"Eksekutif 2-2 | {super().info_konfigurasi()} | "
            f"{self.daftar_fasilitas()}"
        )


class BusEkonomi(Bus):
    def __init__(self, plat_nomor, baris):
        super().__init__(plat_nomor, baris, 2, 3)

    def hitung_tarif(self, tarif_dasar):
        return super().hitung_tarif(tarif_dasar)

    def info_konfigurasi(self):
        return f"Ekonomi 2-3 | {super().info_konfigurasi()}"


class Kursi:
    def __init__(self, label):
        self.__label = label
        self.__dipesan = False

    @property
    def label(self):
        return self.__label

    @property
    def dipesan(self):
        return self.__dipesan

    def pesan(self):
        if self.__dipesan:
            raise KursiSudahDipesanError(f"Kursi {self.__label} sudah dipesan")
        self.__dipesan = True

    def batalkan(self):
        self.__dipesan = False

    def __str__(self):
        return f"{self.__label}({'X' if self.__dipesan else '-'})"


class Rute:
    def __init__(self, asal, tujuan, jarak_km, tarif_dasar):
        if not asal or not tujuan:
            raise DataTidakValidError("Kota asal dan tujuan tidak boleh kosong")
        if jarak_km <= 0:
            raise DataTidakValidError("Jarak tempuh harus lebih dari 0 km")

        self.asal = asal
        self.tujuan = tujuan
        self.jarak_km = jarak_km
        self.tarif_dasar = tarif_dasar  # memanggil setter

    @property
    def tarif_dasar(self):
        return self.__tarif_dasar

    @tarif_dasar.setter
    def tarif_dasar(self, nilai):
        if nilai <= 0:
            raise DataTidakValidError("Tarif dasar harus lebih dari 0")
        self.__tarif_dasar = nilai

    def __str__(self):
        return f"{self.asal} - {self.tujuan} ({self.jarak_km} km)"


class Penumpang:
    def __init__(self, nama, no_hp):
        if not nama or not nama.strip():
            raise DataTidakValidError("Nama penumpang tidak boleh kosong")
        self._nama = nama.strip()
        self.no_hp = no_hp  # memanggil setter

    @property
    def nama(self):
        return self._nama

    @property
    def no_hp(self):
        return self.__no_hp

    @no_hp.setter
    def no_hp(self, nilai):
        if not Penumpang.validasi_no_hp(nilai):
            raise DataTidakValidError(
                f"Nomor HP '{nilai}' tidak valid (harus 10-13 digit angka)"
            )
        self.__no_hp = nilai

    @staticmethod
    def validasi_no_hp(nilai):
        return isinstance(nilai, str) and nilai.isdigit() and 10 <= len(nilai) <= 13

    @classmethod
    def dari_teks(cls, teks):
        if ";" not in teks:
            raise DataTidakValidError(
                "Format teks penumpang salah (gunakan format 'Nama; NoHP')"
            )
        bagian = teks.split(";")
        if len(bagian) != 2:
            raise DataTidakValidError("Format teks harus tepat berisi Nama dan NoHP")
        return cls(bagian[0].strip(), bagian[1].strip())

    def __str__(self):
        return f"{self._nama} ({self.__no_hp})"

    def __repr__(self):
        return f"Penumpang('{self._nama}', '{self.__no_hp}')"

    def __eq__(self, other):
        return isinstance(other, Penumpang) and self.__no_hp == other.no_hp

    def __hash__(self):
        return hash(self.__no_hp)


class Pemesanan:
    jumlah_pemesanan = 0

    def __init__(self, penumpang, jadwal, daftar_kursi):
        Pemesanan.jumlah_pemesanan += 1
        self.__kode = f"PSN{Pemesanan.jumlah_pemesanan:03d}"
        self._penumpang = penumpang
        self._jadwal = jadwal
        self._daftar_kursi = daftar_kursi
        self.__total = jadwal.harga_per_kursi * len(daftar_kursi)

    @property
    def kode(self):
        return self.__kode

    @property
    def total_harga(self):
        return self.__total

    def __str__(self):
        label = ", ".join(k.label for k in self._daftar_kursi)
        return (
            f"{self.__kode} | {self._penumpang.nama} | "
            f"Kursi {label} | Rp{self.__total:,}"
        )


class Jadwal:
    def __init__(self, kode, rute, bus, tanggal, jam):
        self.__kode = kode
        self._rute = rute
        self._bus = bus
        self._tanggal = tanggal
        self._jam = jam
        self.__daftar_kursi = [Kursi(l) for l in bus.daftar_label_kursi()]

    @property
    def kode(self):
        return self.__kode

    @property
    def harga_per_kursi(self):
        return self._bus.hitung_tarif(self._rute.tarif_dasar)

    def kursi_kosong(self):
        return [k.label for k in self.__daftar_kursi if not k.dipesan]

    def __cari_kursi(self, label):
        for k in self.__daftar_kursi:
            if k.label == label:
                return k
        return None

    def pesan(self, penumpang, daftar_label):
        if not daftar_label:
            raise PemesananTidakValidError("Daftar kursi yang dipesan tidak boleh kosong")
        if len(set(daftar_label)) != len(daftar_label):
            raise PemesananTidakValidError("Nomor kursi dalam satu pesanan tidak boleh duplikat")

        dipilih = []
        for label in daftar_label:
            kursi = self.__cari_kursi(label)
            if kursi is None:
                raise KursiTidakDitemukanError(
                    f"Kursi '{label}' tidak ditemukan pada {self._bus.info_konfigurasi()}"
                )
            if kursi.dipesan:
                raise KursiSudahDipesanError(f"Kursi '{label}' sudah dipesan")
            dipilih.append(kursi)

        for kursi in dipilih:
            kursi.pesan()
        return Pemesanan(penumpang, self, dipilih)

    def __str__(self):
        return (
            f"{self.__kode} | {self._rute} | {self._tanggal} {self._jam} | "
            f"Rp{self.harga_per_kursi:,}/kursi"
        )