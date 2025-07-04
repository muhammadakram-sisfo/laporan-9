from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# koneksi database
DB_URL = "sqlite:///toko_elektronik.db"
engine = create_engine(DB_URL, echo=False)         
Base   = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# model/table
class Elektronik(Base):
    __tablename__ = "elektronik"                   
    id    = Column(Integer, primary_key=True, autoincrement=True)
    nama  = Column(String(100), nullable=False)     
    merek = Column(String(50),  nullable=False)
    tipe  = Column(String(50),  nullable=False)
    harga = Column(Float,       nullable=False)
    stok  = Column(Integer,     nullable=False)

Base.metadata.create_all(engine)

# fungsi crud
def tambah_elektronik():
    nama  = input("Nama barang elektronik : ")
    merek = input("Merek                : ")
    tipe  = input("Tipe/Model           : ")
    harga = float(input("Harga               : "))
    stok  = int(input("Stok                : "))
    barang = Elektronik(nama=nama, merek=merek, tipe=tipe, harga=harga, stok=stok)
    session.add(barang)
    session.commit()
    print("Barang elektronik berhasil ditambahkan.\n")

def tampilkan_elektronik():
    data = session.query(Elektronik).all()
    if not data:
        print("\n( belum ada data )\n")
        return
    print("\n=== Daftar Barang Elektronik ===")
    for b in data:
        print(f"{b.id}. {b.nama} | Merek: {b.merek} | Tipe: {b.tipe} | "
              f"Harga: {b.harga:,.0f} | Stok: {b.stok}")
    print()

def update_elektronik():
    tampilkan_elektronik()
    try:
        id_barang = int(input("Masukkan ID barang yang ingin diubah: "))
    except ValueError:
        print("ID harus angka.\n"); return

    barang = session.get(Elektronik, id_barang)     
    if not barang:
        print("Barang tidak ditemukan.\n"); return

    print("(kosongkan jika tidak diubah)")
    nama  = input(f"Nama baru   [{barang.nama}] : ") or barang.nama
    merek = input(f"Merek baru  [{barang.merek}]: ") or barang.merek
    tipe  = input(f"Tipe baru   [{barang.tipe}] : ") or barang.tipe
    harga = input(f"Harga baru  [{barang.harga}]: ") or barang.harga
    stok  = input(f"Stok baru   [{barang.stok}] : ") or barang.stok

    barang.nama  = nama
    barang.merek = merek
    barang.tipe  = tipe
    barang.harga = float(harga)
    barang.stok  = int(stok)
    session.commit()
    print("Barang berhasil diperbarui.\n")

def hapus_elektronik():
    tampilkan_elektronik()
    try:
        id_barang = int(input("Masukkan ID barang yang ingin dihapus: "))
    except ValueError:
        print("ID harus angka.\n"); return

    barang = session.get(Elektronik, id_barang)
    if not barang:
        print("Barang tidak ditemukan.\n"); return

    session.delete(barang)
    session.commit()
    print("Barang berhasil dihapus.\n")

# menu utama
def menu():
    while True:
        print("===MENU TOKO ELEKTRONIK===")
        print("1. Tambah Barang Elektronik")
        print("2. Tampilkan Barang")
        print("3. Update Barang")
        print("4. Hapus Barang")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ")
        if   pilihan == "1": tambah_elektronik()
        elif pilihan == "2": tampilkan_elektronik()
        elif pilihan == "3": update_elektronik()
        elif pilihan == "4": hapus_elektronik()
        elif pilihan == "5":
            print("Program selesai. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.\n")

# Jalankan program
if __name__ == "__main__":
    menu()
