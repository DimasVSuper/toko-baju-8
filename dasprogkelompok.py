from pymongo import MongoClient
import getpass
import pandas as pd
from datetime import datetime

# Koneksi ke MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["tokobaju8"]
collection_baju = db["baju"]
collection_membership = db["membership"]
collection_transactions = db["transaction"]  # Koleksi untuk riwayat transaksi

# Konstanta
BIAYA_TAMBAHAN_XL = 3000
DISKON_MEMBER = 10  # dalam persen

# Fungsi untuk membuat garis
def garis():
    print("=" * 50)

# Fungsi menghitung diskon
def hitung_diskon(total_harga, persentase_diskon):
    """Menghitung diskon berdasarkan persentase."""
    return total_harga * (persentase_diskon / 100)

# Fungsi untuk login membership
def login_membership():
    """Login dengan username dan password membership."""
    while True:
        username = input("Masukkan username: ").strip()
        password = getpass.getpass("Masukkan password: ").strip()
        user = collection_membership.find_one({"username": username, "password": password})

        if user:
            print("Login berhasil! Anda mendapatkan diskon.")
            return user  # Kembalikan data pengguna untuk keperluan riwayat transaksi
        else:
            print("Username atau password salah.")
            if input("Coba lagi? (Y/N): ").strip().upper() != "Y":
                return None

# Fungsi untuk mendaftar akun baru
def daftar_akun_baru():
    """Mendaftarkan akun membership baru."""
    print("\nPendaftaran Akun Baru")
    username = input("Masukkan username: ").strip()
    password = getpass.getpass("Masukkan password: ").strip()

    if collection_membership.find_one({"username": username}):
        print("Username sudah terdaftar.")
        return None

    user_id = collection_membership.insert_one({"username": username, "password": password}).inserted_id
    print("Akun berhasil dibuat!")
    return collection_membership.find_one({"_id": user_id})

# Fungsi untuk memilih produk
def pilih_produk(produk_list):
    while True:
        try:
            pilihan_produk = int(input("Pilih nomor produk: ")) - 1
            if 0 <= pilihan_produk < len(produk_list):
                return produk_list[pilihan_produk]
            else:
                print("Nomor produk tidak valid.")
        except ValueError:
            print("Masukan harus berupa angka.")

# Fungsi untuk memilih ukuran
def pilih_ukuran():
    while True:
        ukuran = input("Masukkan ukuran (L/M/XL): ").strip().upper()
        if ukuran in ["L", "M", "XL"]:
            return ukuran
        print("Pilihan ukuran tidak valid.")

# Fungsi memilih produk dan menghitung total harga
def hitung_total_harga(jumlahproduk):
    total_harga = 0
    produk_list = list(collection_baju.find())

    if not produk_list:
        print("Tidak ada produk yang tersedia.")
        return 0, []

    pembelian = []
    for i in range(jumlahproduk):
        print(f"\nProduk ke-{i + 1}:\n--- Daftar Produk ---")
        for idx, produk in enumerate(produk_list):
            print(f"{idx + 1}. {produk['name']} (Rp {produk['harga']:,})")

        produk_terpilih = pilih_produk(produk_list)
        ukuran = pilih_ukuran()
        biaya_tambahan = BIAYA_TAMBAHAN_XL if ukuran == "XL" else 0
        harga_total_produk = produk_terpilih['harga'] + biaya_tambahan
        total_harga += harga_total_produk

        pembelian.append({
            "name": produk_terpilih['name'],
            "ukuran": ukuran,
            "harga": harga_total_produk
        })

        print(f"Harga produk dengan ukuran {ukuran}: Rp {harga_total_produk:,}")

    return total_harga, pembelian

# Fungsi untuk menyimpan transaksi ke database
def simpan_transaksi(username, pembelian, total_harga, potongan, total_setelah_diskon):
    transaksi = {
        "username": username,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pembelian": pembelian,
        "total_harga": total_harga,
        "potongan": potongan,
        "total_setelah_diskon": total_setelah_diskon
    }
    collection_transactions.insert_one(transaksi)
    print("Transaksi berhasil disimpan ke riwayat.")

# Fungsi untuk menampilkan riwayat transaksi
def lihat_riwayat_transaksi(username):
    transaksi_list = list(collection_transactions.find({"username": username}))
    if not transaksi_list:
        print("Tidak ada riwayat transaksi.")
        while True:
            pilihan = input("Apa yang ingin Anda lakukan selanjutnya? (1: Lanjutkan Belanja, 2: Keluar): ").strip()
            if pilihan == "1":
                return  # Kembali ke proses berbelanja
            elif pilihan == "2":
                print("Terima kasih telah berbelanja! Sampai jumpa!")
                exit()  # Keluar dari program
            else:
                print("Pilihan tidak valid. Silakan pilih 1 atau 2.")
    else:
        garis()
        print("RIWAYAT TRANSAKSI".center(50))
        garis()
        for idx, transaksi in enumerate(transaksi_list):
            print(f"Transaksi ke-{idx + 1} ({transaksi['tanggal']}):")
            for pembelian in transaksi["pembelian"]:
                print(f"  - {pembelian['name']} ({pembelian['ukuran']}): Rp {pembelian['harga']:,}")
            print(f"Subtotal: Rp {transaksi['total_harga']:,}")
            print(f"Diskon: Rp {transaksi['potongan']:,}")
            print(f"Total Setelah Diskon: Rp {transaksi['total_setelah_diskon']:,}")
            garis()

        while True:
            pilihan = input("Apa yang ingin Anda lakukan selanjutnya? (1: Lanjutkan Belanja, 2: Keluar): ").strip()
            if pilihan == "1":
                return  # Kembali ke proses berbelanja
            elif pilihan == "2":
                print("Terima kasih telah berbelanja! Sampai jumpa!")
                exit()  # Keluar dari program
            else:
                print("Pilihan tidak valid. Silakan pilih 1 atau 2.")

# Fungsi untuk menampilkan ringkasan pembelian
def tampilkan_ringkasan(jumlahproduk, potongan, total_harga):
    data = {
        "Deskripsi": ["Jumlah Produk", "Potongan Harga", "Total Setelah Diskon"],
        "Nilai": [jumlahproduk, f"Rp {potongan:,}", f"Rp {total_harga:,}"]
    }
    df_ringkasan = pd.DataFrame(data)

    garis()
    print("RINGKASAN PEMBELIAN".center(50))
    garis()
    print(df_ringkasan.to_string(index=False))
    garis()

# Fungsi utama
def main():
    garis()
    print("SELAMAT DATANG DI TOKO BAJU 8!".center(50))
    garis()

    user = None
    if input("Apakah kamu memiliki Akun Membership? (Y/N): ").strip().upper() == "Y":
        user = login_membership()
    elif input("Apakah Anda ingin mendaftar? (Y/N): ").strip().upper() == "Y":
        user = daftar_akun_baru()

    if user:
        if input("Apakah Anda ingin melihat riwayat transaksi? (Y/N): ").strip().upper() == "Y":
            lihat_riwayat_transaksi(user["username"])

    while True:
        try:
            jumlahproduk = int(input("Berapa jumlah baju yang akan dibeli? : "))
            if jumlahproduk > 0:
                break
        except ValueError:
            print("Masukan tidak valid. Silakan masukkan angka.")

    total_harga, pembelian = hitung_total_harga(jumlahproduk)
    potongan = hitung_diskon(total_harga, DISKON_MEMBER) if user else 0
    total_setelah_diskon = total_harga - potongan

    if user:
        simpan_transaksi(user["username"], pembelian, total_harga, potongan, total_setelah_diskon)

    tampilkan_ringkasan(jumlahproduk, potongan, total_setelah_diskon)
    print("Terima kasih telah berbelanja di Toko Baju 8!")

# Jalankan program
if __name__ == "__main__":
    main()






