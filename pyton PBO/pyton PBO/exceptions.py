class TiketBusError(Exception):
    """Base exception untuk seluruh kesalahan pada sistem pemesanan tiket bus."""
    pass


class DataTidakValidError(TiketBusError):
    """Dilempar ketika data input atau atribut melanggar aturan validasi."""
    pass


class KursiTidakDitemukanError(TiketBusError):
    """Dilempar ketika label kursi tidak terdaftar pada jadwal/bus."""
    pass


class KursiSudahDipesanError(TiketBusError):
    """Dilempar ketika kursi yang dipilih sudah dipesan sebelumnya."""
    pass


class PemesananTidakValidError(TiketBusError):
    """Dilempar ketika transaksi pemesanan tidak valid (kosong atau duplikat)."""
    pass