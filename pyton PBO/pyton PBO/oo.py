from abc import ABC, abstractmethod


# ---------------------------------------------------------------
# KELAS TERHUBUNG: Engine (komponen milik Vehicle -> hubungan has-a)
# ---------------------------------------------------------------
class Engine:
    def __init__(self, type_="V6", horsepower=200):
        self.type = type_
        self.horsepower = horsepower

    def start(self):
        return "Mesin menyala"


# ---------------------------------------------------------------
# 1. ABSTRAKSI & ENKAPSULASI: Vehicle
# ---------------------------------------------------------------
class Vehicle(ABC):
    def __init__(self, name, fuel):
        self.name = name                # public
        self.__fuel = fuel              # private (name mangling)
        self.__max_fuel = fuel          # private
        self.engine = Engine()          # has-a

    # Getter (hanya baca)
    @property
    def fuel(self):
        return self.__fuel

    def get_fuel(self):
        return self.__fuel

    # Perubahan state hanya lewat method
    def consume_fuel(self, amount):
        self.__fuel = max(0, self.__fuel - amount)

    def add_fuel(self, amount):
        self.__fuel = min(self.__max_fuel, self.__fuel + amount)

    @abstractmethod
    def drive(self, distance):
        """Method abstrak: wajib di-override oleh kelas turunan."""


# ---------------------------------------------------------------
# 2. PEWARISAN & POLIMORFISME: Car dan HybridCar
# ---------------------------------------------------------------
class Car(Vehicle):
    def __init__(self, name, fuel):
        super().__init__(name, fuel)
        self.speed = 0

    def drive(self, distance):
        fuel_used = 5 + (self.speed * 0.5)
        self.speed += 10
        self.consume_fuel(fuel_used)
        return f"Mobil {self.name} melaju {distance} km! BBM terpakai: {fuel_used:.0f}"


class HybridCar(Vehicle):
    def __init__(self, name, fuel, battery):
        super().__init__(name, fuel)
        self.__battery = battery        # private

    def drive(self, distance):
        if self.__battery >= 10:
            self.__battery -= 10
            self.consume_fuel(2)
            return f"Hybrid {self.name} melaju {distance} km mode hemat!"
        return "Baterai tidak cukup!"


# ---------------------------------------------------------------
# 3. KELAS TERHUBUNG: Part, FuelCan, dan Garage
# ---------------------------------------------------------------
class Part(ABC):
    def __init__(self, part_name):
        self.part_name = part_name

    @abstractmethod
    def apply(self, target):
        """Mengubah state Vehicle target."""


class FuelCan(Part):
    def __init__(self, fuel_amount=50):
        super().__init__("Jerigen BBM")
        self.fuel_amount = fuel_amount

    def apply(self, target):
        target.add_fuel(self.fuel_amount)   # lewat method, bukan akses langsung
        return f"BBM bertambah {self.fuel_amount}"


class Garage:
    """Menyimpan banyak Vehicle dan memanfaatkan polimorfisme."""

    def __init__(self):
        self.vehicles = []

    def add(self, vehicle):
        self.vehicles.append(vehicle)

    def drive_all(self, distance):
        for v in self.vehicles:
            print(" -", v.drive(distance))   # satu panggilan, perilaku berbeda

    def show_all(self):
        for v in self.vehicles:
            print(f" - {v.name:<10} BBM: {v.fuel:.0f}")


# ---------------------------------------------------------------
# DEMO: simulasi perubahan state
# ---------------------------------------------------------------
if __name__ == "__main__":
    avanza = Car("Avanza", 100)
    prius = HybridCar("Prius", 100, battery=15)
    can = FuelCan(50)

    print("== Mesin ==")
    print(avanza.engine.start())

    print("\n== Simulasi state Car ==")
    print("BBM awal      :", avanza.fuel)
    print(avanza.drive(10), "| sisa:", avanza.fuel, "| speed:", avanza.speed)
    print(avanza.drive(10), "| sisa:", avanza.fuel, "| speed:", avanza.speed)
    print(can.apply(avanza), "| sisa:", avanza.fuel, "(dibatasi tangki penuh)")

    print("\n== Polimorfisme lewat Garage ==")
    garage = Garage()
    garage.add(avanza)
    garage.add(prius)
    garage.drive_all(10)
    garage.drive_all(10)   # baterai Prius habis di sini
    print("\nStatus akhir:")
    garage.show_all()

    print("\n== Enkapsulasi ==")
    try:
        avanza.fuel = 999   # property read-only
    except AttributeError:
        print("fuel tidak bisa diubah langsung, hanya lewat add_fuel()/consume_fuel()")