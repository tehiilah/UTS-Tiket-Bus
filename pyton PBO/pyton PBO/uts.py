class FasilitasMixin:
    """Mixin: menambah kemampuan menampilkan fasilitas."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fasilitas = []

    def daftar_fasilitas(self):
        return ", ".join(self._fasilitas)


class Bus:
    jumlah_bus = 0  # class attribute

    def __init__(self, plat_nomor, baris, kursi_kiri, kursi_kanan):
        self.__plat_nomor = plat_nomor
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
        huruf = "ABCDEFGH"[:self._kursi_kiri + self._kursi_kanan]
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
        return (f"Eksekutif 2-2 | {super().info_konfigurasi()} | "
                f"{self.daftar_fasilitas()}")


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
            raise ValueError(f"Kursi {self.__label} sudah dipesan")
        self.__dipesan = True

    def batalkan(self):
        self.__dipesan = False

    def __str__(self):
        return f"{self.__label}({'X' if self.__dipesan else '-'})"


class Rute:
    def __init__(self, asal, tujuan, jarak_km, tarif_dasar):
        self.asal = asal
        self.tujuan = tujuan
        self.jarak_km = jarak_km
        self.tarif_dasar = tarif_dasar  # lewat setter

    @property
    def tarif_dasar(self):
        return self.__tarif_dasar

    @tarif_dasar.setter
    def tarif_dasar(self, nilai):
        if nilai <= 0:
            raise ValueError("Tarif dasar harus lebih dari 0")
        self.__tarif_dasar = nilai

    def __str__(self):
        return f"{self.asal} - {self.tujuan} ({self.jarak_km} km)"


class Penumpang:
    def __init__(self, nama, no_hp):
        self._nama = nama
        self.no_hp = no_hp  # lewat setter

    @property
    def nama(self):
        return self._nama

    @property
    def no_hp(self):
        return self.__no_hp

    @no_hp.setter
    def no_hp(self, nilai):
        if not Penumpang.validasi_no_hp(nilai):
            raise ValueError("Nomor HP tidak valid")
        self.__no_hp = nilai

    @staticmethod
    def validasi_no_hp(nilai):
        return nilai.isdigit() and 10 <= len(nilai) <= 13

    @classmethod
    def dari_teks(cls, teks):
        nama, no_hp = teks.split(";")
        return cls(nama.strip(), no_hp.strip())

    def __str__(self):
        return f"{self._nama} ({self.__no_hp})"

    def __repr__(self):
        return f"Penumpang('{self._nama}', '{self.__no_hp}')"

    def __eq__(self, other):
        return isinstance(other, Penumpang) and self.__no_hp == other.no_hp

    def __hash__(self):
        return hash(self.__no_hp)


class Pemesanan:
    jumlah_pemesanan = 0  # class attribute

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
        return (f"{self.__kode} | {self._penumpang.nama} | "
                f"Kursi {label} | Rp{self.__total:,}")


class Jadwal:
    def __init__(self, kode, rute, bus, tanggal, jam):
        self.__kode = kode
        self._rute = rute            # aggregation
        self._bus = bus              # aggregation
        self._tanggal = tanggal
        self._jam = jam
        self.__daftar_kursi = [Kursi(l) for l in bus.daftar_label_kursi()]  # composition

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
        if len(set(daftar_label)) != len(daftar_label):
            raise ValueError("Nomor kursi duplikat")
        dipilih = []
        for label in daftar_label:
            kursi = self.__cari_kursi(label)
            if kursi is None:
                raise ValueError(f"Kursi {label} tidak ada")
            if kursi.dipesan:
                raise ValueError(f"Kursi {label} sudah dipesan")
            dipilih.append(kursi)
        for kursi in dipilih:
            kursi.pesan()
        return Pemesanan(penumpang, self, dipilih)

    def __str__(self):
        return (f"{self.__kode} | {self._rute} | {self._tanggal} {self._jam} | "
                f"Rp{self.harga_per_kursi:,}/kursi")


if __name__ == "__main__":
    rute = Rute("Denpasar", "Surabaya", 420, 200000)
    bus_eks = BusEksekutif("DK 7001 AB", 5)
    bus_eko = BusEkonomi("DK 7002 CD", 4)
    print(bus_eks.info_konfigurasi())
    print(bus_eko.info_konfigurasi())
    print("Jumlah bus:", Bus.jumlah_bus)

    jadwal = Jadwal("JD01", rute, bus_eks, "28-10-2026", "20:00")
    print(jadwal)
    print("Kursi kosong:", len(jadwal.kursi_kosong()))

    budi = Penumpang.dari_teks("Budi Santoso; 081234567890")
    pesanan1 = jadwal.pesan(budi, ["1A", "1B"])
    print(pesanan1)
    print("Kursi kosong:", len(jadwal.kursi_kosong()))

    sari = Penumpang("Sari Dewi", "085711223344")
    try:
        jadwal.pesan(sari, ["1B", "2A"])
    except ValueError as e:
        print("Gagal pesan:", e)

    try:
        rute.tarif_dasar = -5000
    except ValueError as e:
        print("Validasi tarif:", e)
    try:
        sari.no_hp = "abc123"
    except ValueError as e:
        print("Validasi HP:", e)

    budi2 = Penumpang("B. Santoso", "081234567890")
    print("budi == budi2:", budi == budi2)
    print("budi == sari:", budi == sari)

    pesanan2 = jadwal.pesan(sari, ["2A"])
    print(pesanan2)
    print("Total pemesanan:", Pemesanan.jumlah_pemesanan)
print([c.__name__ for c in BusEksekutif.__mro__])