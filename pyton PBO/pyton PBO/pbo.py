class Mahasiswa:
    def __init__(self, nama, nim):
        self.nama = nama
        self.nim = nim


    def sapan(self):
        return f"halo, saya {self.nama}"

ayu = mahasiswa("2301", "ayu")
gede = mahasiswa("2302", "gede")

print(ayu.sapa())
