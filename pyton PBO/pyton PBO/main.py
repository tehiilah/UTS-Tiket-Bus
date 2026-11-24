from exceptions import (
    TiketBusError,
    DataTidakValidError,
    KursiTidakDitemukanError,
    KursiSudahDipesanError,
    PemesananTidakValidError,
)
from models import Bus, BusEksekutif, BusEkonomi, Rute, Penumpang, Jadwal, Pemesanan


def proses_pemesanan(jadwal, penumpang, daftar_kursi):
    """Helper untuk mendemonstrasikan blok lengkap try - except - else - finally."""
    print(f"\n[PROSES] {penumpang.nama} mencoba memesan kursi {daftar_kursi}...")
    try:
        pesanan = jadwal.pesan(penumpang, daftar_kursi)
    except KursiSudahDipesanError as e:
        print(f"  [GAGAL - Kursi Terisi] {e}")
    except KursiTidakDitemukanError as e:
        print(f"  [GAGAL - Kursi Tidak Ada] {e}")
    except PemesananTidakValidError as e:
        print(f"  [GAGAL - Pesanan Tidak Valid] {e}")
    except TiketBusError as e:
        print(f"  [GAGAL - Kesalahan Sistem] {e}")
    else:
        print(f"  [BERHASIL] Tiket terbit -> {pesanan}")
        return pesanan
    finally:
        print(f"  [INFO] Sisa kursi kosong pada {jadwal.kode}: {len(jadwal.kursi_kosong())} kursi")
    return None


if __name__ == "__main__":
    # 1. Inisialisasi Data Master
    rute = Rute("Denpasar", "Surabaya", 420, 200000)
    bus_eks = BusEksekutif("DK 7001 AB", 5)
    bus_eko = BusEkonomi("DK 7002 CD", 4)
    print(bus_eks.info_konfigurasi())
    print(bus_eko.info_konfigurasi())
    print("Jumlah bus:", Bus.jumlah_bus)

    jadwal = Jadwal("JD01", rute, bus_eks, "28-10-2026", "20:00")
    print("\nJadwal Aktif:", jadwal)

    # 2. Pemesanan Berhasil (blok try -> else -> finally)
    budi = Penumpang.dari_teks("Budi Santoso; 081234567890")
    proses_pemesanan(jadwal, budi, ["1A", "1B"])

    # 3. Pelanggaran Aturan Bisnis: Kursi sudah dipesan (Atomik: 2A batal ikut terpesan)
    sari = Penumpang("Sari Dewi", "085711223344")
    proses_pemesanan(jadwal, sari, ["1B", "2A"])

    # 4. Pelanggaran Aturan Bisnis: Kursi tidak ditemukan pada bus 2-2 (tidak ada kursi E)
    proses_pemesanan(jadwal, sari, ["1E"])

    # 5. Pelanggaran Aturan Bisnis: Kursi duplikat & daftar kosong
    proses_pemesanan(jadwal, sari, ["2A", "2A"])
    proses_pemesanan(jadwal, sari, [])

    # 6. Pemesanan ulang Sari yang valid (membuktikan 2A aman dari transaksi gagal sebelumnya)
    proses_pemesanan(jadwal, sari, ["2A"])

    # 7. Pengujian Setter & Classmethod dengan DataTidakValidError
    print("\n--- Pengujian Validasi Data ---")
    kasus_uji_data = [
        ("Tarif negatif", lambda: setattr(rute, "tarif_dasar", -5000)),
        ("Nomor HP huruf", lambda: setattr(sari, "no_hp", "abc123")),
        ("Format teks tanpa ';'", lambda: Penumpang.dari_teks("Andi Wijaya 081299887766")),
    ]

    for nama_uji, aksi in kasus_uji_data:
        try:
            aksi()
        except DataTidakValidError as e:
            print(f"[VALIDASI OK - {nama_uji}] Menangkap error: {e}")
        else:
            print(f"[PERINGATAN - {nama_uji}] Seharusnya gagal tetapi lolos!")
        finally:
            print(f"  Selesai mengecek: {nama_uji}")

    print("\nTotal pemesanan sah:", Pemesanan.jumlah_pemesanan)