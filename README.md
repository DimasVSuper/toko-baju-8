# 🛍️ Toko Baju 8 - Sistem Kasir Digital

**Tugas Akhir Dasar Pemrograman Semester 1**

Aplikasi sistem kasir digital untuk toko baju dengan fitur membership, manajemen produk, dan riwayat transaksi menggunakan Python dan MongoDB.

## 📋 Deskripsi Project

Toko Baju 8 adalah aplikasi console-based yang mensimulasikan sistem point of sale (POS) untuk toko pakaian. Aplikasi ini memungkinkan pelanggan untuk berbelanja, mendaftar membership untuk mendapatkan diskon, dan melihat riwayat transaksi mereka.

## ✨ Fitur Utama

### 👥 Sistem Membership
- **Login & Registrasi**: Pengguna dapat membuat akun baru atau login dengan akun yang sudah ada
- **Diskon Member**: Member mendapatkan diskon 10% untuk setiap pembelian
- **Keamanan**: Password tersembunyi saat input menggunakan library `getpass`

### 🛒 Sistem Belanja
- **Katalog Produk**: Menampilkan daftar baju dengan harga
- **Pilihan Ukuran**: Tersedia ukuran L, M, dan XL
- **Biaya Tambahan**: Ukuran XL dikenakan biaya tambahan Rp 3.000
- **Multiple Items**: Dapat membeli beberapa produk dalam satu transaksi

### 💰 Sistem Pembayaran
- **Kalkulasi Otomatis**: Menghitung total harga secara otomatis
- **Aplikasi Diskon**: Diskon member diterapkan secara otomatis
- **Ringkasan Pembelian**: Menampilkan detail pembelian dalam format tabel

### 📊 Manajemen Data
- **Database MongoDB**: Menyimpan data produk, member, dan transaksi
- **Riwayat Transaksi**: Menyimpan dan menampilkan riwayat pembelian
- **Data Persistence**: Semua data tersimpan permanen di database

## 🛠️ Teknologi yang Digunakan

- **Python 3.x** - Bahasa pemrograman utama
- **MongoDB** - Database NoSQL untuk penyimpanan data
- **PyMongo** - Driver MongoDB untuk Python
- **Pandas** - Library untuk manipulasi dan analisis data
- **getpass** - Library untuk input password yang aman

## 📦 Instalasi dan Setup

### 1. Clone Repository
```bash
git clone https://github.com/DimasVSuper/toko-baju-8.git
cd toko-baju-8
```

### 2. Install Dependencies
```bash
pip install pymongo pandas
```

### 3. Setup MongoDB
- Install MongoDB di sistem Anda
- Pastikan MongoDB berjalan di `localhost:27017`
- Database akan otomatis dibuat saat pertama kali menjalankan aplikasi

### 4. Jalankan Aplikasi
```bash
python dasprogkelompok.py
```

## 🗃️ Struktur Database

### Collection: `baju`
```json
{
  "_id": ObjectId,
  "name": "string",
  "harga": number
}
```

### Collection: `membership`
```json
{
  "_id": ObjectId,
  "username": "string",
  "password": "string"
}
```

### Collection: `transaction`
```json
{
  "_id": ObjectId,
  "username": "string",
  "tanggal": "string",
  "pembelian": [
    {
      "name": "string",
      "ukuran": "string",
      "harga": number
    }
  ],
  "total_harga": number,
  "potongan": number,
  "total_setelah_diskon": number
}
```

## 🎯 Cara Penggunaan

1. **Jalankan Program**: Eksekusi file `dasprogkelompok.py`
2. **Pilih Membership**: 
   - Login jika sudah punya akun
   - Daftar akun baru untuk mendapat diskon
   - Skip jika tidak ingin menggunakan membership
3. **Lihat Riwayat** (opsional): Cek transaksi sebelumnya
4. **Berbelanja**:
   - Input jumlah baju yang ingin dibeli
   - Pilih produk dari katalog
   - Pilih ukuran untuk setiap produk
5. **Checkout**: Lihat ringkasan dan total pembayaran

## 📸 Screenshot/Demo

```
==================================================
        SELAMAT DATANG DI TOKO BAJU 8!
==================================================
Apakah kamu memiliki Akun Membership? (Y/N): Y
Masukkan username: dimas
Masukkan password: ****
Login berhasil! Anda mendapatkan diskon.

Berapa jumlah baju yang akan dibeli? : 2

Produk ke-1:
--- Daftar Produk ---
1. Kaos Polos (Rp 50,000)
2. Kemeja Formal (Rp 120,000)
3. Jaket Denim (Rp 200,000)

Pilih nomor produk: 1
Masukkan ukuran (L/M/XL): L
Harga produk dengan ukuran L: Rp 50,000
```

## 🤝 Kontribusi

Project ini merupakan tugas akhir untuk mata kuliah Dasar Pemrograman. Saran dan masukan sangat diterima untuk pengembangan lebih lanjut.

## 📝 Lisensi

Project ini dibuat untuk keperluan akademis - Tugas Akhir Dasar Pemrograman Semester 1.

## 👨‍💻 Author

**Dimas**
- GitHub: [@DimasVSuper](https://github.com/DimasVSuper)

---

⭐ **Star** repository ini jika Anda merasa terbantu!
