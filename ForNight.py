# ============================
#   MOUNT GOOGLE DRIVE
# ============================
from google.colab import drive
drive.mount('/content/gdrive', force_remount=True)

import json
import os

# ============================
#   PATH DATABASE
# ============================
FOLDER = "/content/gdrive/MyDrive/ForNight_DB"
data_file = f"{FOLDER}/fornight_menu.json"

# Buat folder jika belum ada
if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)
    print("📁 Folder database dibuat:", FOLDER)

menu = []  # Database menu


# ============================
#   LOAD & SAVE DATA
# ============================
def load_data():
    global menu
    print("\n🔄 Loading database ForNight...")
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as f:
                menu = json.load(f)
            print("✅ Database berhasil dimuat!")
        except:
            print("⚠ Database rusak → membuat baru…")
            menu = []
            save_data()
    else:
        print("⚠ File belum ada → membuat file baru…")
        menu = []
        save_data()


def save_data():
    try:
        with open(data_file, "w") as f:
            json.dump(menu, f, indent=4)
        print("💾 Data TerUpdate!")
    except Exception as e:
        print("❌ Error saat menyimpan:", e)


# ============================
#   1. CREATE
# ============================
def create_menu():
    print("\n🍽️ === Tambah Menu Baru ===")
    nama = input("🍜 Nama makanan/minuman : ")
    harga = int(input("💰 Harga : "))
    stok = int(input("📦 Stok : "))

    menu.append({
        "nama": nama,
        "harga": harga,
        "stok": stok
    })

    save_data()
    print("🎉 Menu berhasil ditambahkan!")


# ============================
#   2. READ
# ============================
def read_menu():
    print("\n📋 === Daftar Menu Restoran ForNight ===")
    if not menu:
        print("😢 Menu masih kosong!")
        return

    for i, item in enumerate(menu, start=1):
        print(f"{i}. 🍽️ {item['nama']} — 💰 Rp{item['harga']} — 📦 Stok: {item['stok']}")


# ============================
#   3. UPDATE
# ============================
def update_menu():
    read_menu()
    print("\n✏️ Edit Data Menu")
    idx = int(input("➡ Pilih nomor menu yang ingin diubah: ")) - 1

    if 0 <= idx < len(menu):
        menu[idx]["nama"] = input("🆕 Nama baru: ")
        menu[idx]["harga"] = int(input("💰 Harga baru: "))
        menu[idx]["stok"] = int(input("📦 Stok baru: "))
        save_data()
        print("✔ Data berhasil diperbarui!")
    else:
        print("❌ Nomor tidak valid!")


# ============================
#   4. DELETE
# ============================
def delete_menu():
    read_menu()
    print("\n🗑️ Hapus Data Menu")
    idx = int(input("➡ Pilih nomor menu yang ingin dihapus: ")) - 1

    if 0 <= idx < len(menu):
        menu.pop(idx)
        save_data()
        print("🗑️✔ Menu berhasil dihapus!")
    else:
        print("❌ Nomor tidak valid!")


# ============================
#   5. SEARCH
# ============================
def search_menu():
    keyword = input("\n🔍 Cari menu berdasarkan nama: ").lower()
    results = [item for item in menu if keyword in item["nama"].lower()]

    print("\n📌 Hasil Pencarian:")
    if results:
        for item in results:
            print(f"🍽️ {item['nama']} — 💰 Rp{item['harga']} — 📦 Stok: {item['stok']}")
    else:
        print("❌ Tidak ditemukan.")


# ============================
#   6. SORT
# ============================
def sort_menu():
    print("\n📊 Urutkan berdasarkan:")
    print("1. Nama (A-Z)")
    print("2. Harga termurah")
    print("3. Harga termahal")
    pilih = input("➡ Pilih (1/2/3): ")

    if pilih == "1":
        sorted_list = sorted(menu, key=lambda x: x["nama"])
    elif pilih == "2":
        sorted_list = sorted(menu, key=lambda x: x["harga"])
    elif pilih == "3":
        sorted_list = sorted(menu, key=lambda x: x["harga"], reverse=True)
    else:
        print("❌ Pilihan tidak valid!")
        return

    print("\n📊 Hasil Sorting:")
    for item in sorted_list:
        print(f"🍽️ {item['nama']} — 💰 Rp{item['harga']} — 📦 Stok: {item['stok']}")


# ============================
#   7. KASIR + DISKON
# ============================
def kasir():
    if not menu:
        print("😢 Menu kosong!")
        return

    read_menu()
    idx = int(input("\n➡ Pilih nomor menu: ")) - 1

    if not (0 <= idx < len(menu)):
        print("❌ Pilihan tidak valid!")
        return

    jumlah = int(input("🛒 Jumlah pembelian: "))
    if jumlah > menu[idx]["stok"]:
        print("⚠ Stok tidak cukup!")
        return

    harga = menu[idx]["harga"]
    subtotal = harga * jumlah

    print("\n🏷️ Diskon tersedia!")
    diskon = int(input("Masukkan diskon (%): "))
    potongan = subtotal * (diskon / 100)
    total = subtotal - potongan

    print(f"\n💳 Total yang harus dibayar: Rp{int(total)}")

    # Uang bayar + kembalian
    uang = int(input("💵 Masukkan uang bayar: "))

    if uang < total:
        print("❌ Uang tidak cukup! Transaksi dibatalkan.")
        return

    kembalian = uang - total

    # Output sederhana tanpa struk
    print("\n✅ Transaksi Berhasil!")
    print(f"💰 Total Bayar : Rp{int(total)}")
    print(f"💵 Uang Bayar  : Rp{uang}")
    print(f"💸 Kembalian   : Rp{int(kembalian)}\n")

    # Kurangi stok
    menu[idx]["stok"] -= jumlah
    save_data()


# ============================
#       MAIN MENU
# ============================
def main():
    load_data()

    while True:
        print("\n🌙✨ ===============================")
        print("     SISTEM RESTORAN FORNIGHT")
        print("===================================")
        print("1. ➕ Tambah Menu ")
        print("2. 📋 Lihat Menu ")
        print("3. ✏️ Edit Menu ")
        print("4. 🗑️ Hapus Menu ")
        print("5. 🔍 Cari Menu ")
        print("6. 📊 Urutkan Menu ")
        print("7. 💵 Kasir ")
        print("0. 🚪 Keluar")
        print("===================================")

        pilih = input("➡ Pilih menu: ")

        if pilih == "1":
            create_menu()
        elif pilih == "2":
            read_menu()
        elif pilih == "3":
            update_menu()
        elif pilih == "4":
            delete_menu()
        elif pilih == "5":
            search_menu()
        elif pilih == "6":
            sort_menu()
        elif pilih == "7":
            kasir()
        elif pilih == "0":
            print("👋 Terima kasih telah menggunakan sistem ForNight!")
            break
        else:
            print("❌ Input tidak valid!")


main()