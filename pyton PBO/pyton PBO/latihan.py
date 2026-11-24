class lapotp:
    nama_toko = "toko jaya"
    jumlah_produk = 10

    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self.stok = stok
        lapotp.jumlah_produk += 1
    def sapa(self):
        return f"halo, saya {self.nama}"

a = lapotp("asus", 10000, 5)
b = lapotp("acer", 15000, 5)

print(a.sapa())
print(b.sapa())
print(lapotp.nama_toko)
print(lapotp.jumlah_produk)

