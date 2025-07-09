# APLIKASI-MANAJEMEN-KEUANGAN-PRIBADI
- Project Pertemuan 15-16
- Aplikasi ini dibuat menggunakan Python untuk membantu pengguna mencatat transaksi keuangan secara sederhana melalui antarmuka terminal (Command-Line Interface).
- Aplikasi ini menyimpan data transaksi dan kategori ke file CSV dan menghasilkan laporan bulanan dan tahunan.

# Import Library
![image](https://github.com/user-attachments/assets/9b3b1a7f-2677-486a-aa2d-9017e28dde60)
- Penjelasan Kode
1. import csv
 - Modul standar Python untuk membaca dan menulis file .csv.
 - Dalam proyek ini digunakan untuk memproses file transaksi.csv dan kategori.csv.
2. from datetime import datetime
  - Mengimpor kelas datetime untuk menangani data tanggal.
  - Berguna untuk: Validasi format tanggal (YYYY-MM-DD) & Menyaring transaksi berdasarkan bulan dan tahun
3. from collections import defaultdict
  - Mengimpor defaultdict, sebuah jenis dictionary yang memberikan nilai default otomatis.
  - Digunakan dalam pembuatan laporan tahunan agar data tiap bulan bisa langsung diakses dan dijumlahkan tanpa inisialisasi  manual.

# Struktur Data
![image](https://github.com/user-attachments/assets/61eae737-12cb-4129-a18f-0a5d13d4a910)
- Penjelasan Kode
1. transaksi_list = []
   - Ini adalah sebuah list kosong ([]) yang digunakan untuk menyimpan seluruh data transaksi keuangan selama program berjalan.
   - Dalam konteks aplikasi manajemen keuangan, setiap transaksi (baik pemasukan maupun pengeluaran) akan disimpan sebagai dictionary, lalu dimasukkan ke dalam list ini.

   - Contoh isi list setelah program digunakan:
transaksi_list = [
{"tanggal": "2025-07-01", "jenis": "pemasukan", "jumlah": "500000", "kategori": "gaji"},
{"tanggal": "2025-07-02", "jenis": "pengeluaran", "jumlah": "150000", "kategori": "makan"}
]
  - List ini berfungsi sebagai penyimpanan sementara (di dalam memori) sebelum data disimpan ke file transaksi.csv.
    
2. kategori_map = {}
   - Ini adalah dictionary kosong ({}) atau bisa disebut juga hashmap dalam konsep struktur data.
   - Digunakan untuk menyimpan daftar kategori transaksi yang valid, yang dibaca dari file kategori.csv.
   - Key dari dictionary ini adalah nama kategori (string), dan nilainya bisa berupa boolean (True) atau nilai lain, tergantung kebutuhan (dalam kode ini: hanya digunakan untuk validasi).
   - kategori_map = {
    "makan": True,
    "gaji": True,
    "transportasi": True,
    "hiburan": True
}
   - Fungsi utama: memvalidasi input kategori ketika pengguna menambahkan transaksi baru.


# LOAD FILE
![image](https://github.com/user-attachments/assets/7c2976eb-79ad-4454-8eb2-2402ad07075d)
- Penjelasan Kode
1. load_kategori()
- global kategori_map Digunakan untuk memastikan fungsi ini dapat mengakses dan mengubah variabel global kategori_map.
- kategori_map = {} Mengosongkan isi kategori_map sebelum mengisi ulang dari file.
- with open("kategori.csv", mode="r") Membuka file kategori.csv dalam mode baca (r). Jika file tidak ditemukan, akan masuk ke blok except.
- csv.DictReader(file) Membaca isi CSV sebagai baris dictionary (misalnya: { 'nama': 'makan' }).
- kategori_map[row['nama']] = True Menyimpan kategori ke dalam dictionary kategori_map dengan key = nama kategori, dan value = True. Ini memungkinkan validasi kategori secara cepat saat pengguna memasukkan data transaksi.
- Jika file tidak ditemukan, program akan mencetak pesan error, namun tetap berjalan.

2. load_transaksi()
- global transaksi_list Mengizinkan fungsi ini mengakses variabel global transaksi_list.
- transaksi_list = [] Mengosongkan list sebelum mengisi ulang dari file.
- open("transaksi.csv", mode="r") Membuka file transaksi.csv untuk dibaca. Jika file belum ada, maka tampilkan pesan error.
- csv.DictReader(file) Mengubah setiap baris CSV menjadi dictionary dengan kolom tanggal, jenis, jumlah, dan kategori.
- transaksi_list.append(row) Menambahkan setiap transaksi yang dibaca dari file ke dalam transaksi_list.
- Jika file tidak ditemukan, akan muncul pesan "File transaksi.csv tidak ditemukan!", tapi program tetap bisa lanjut tanpa crash.

# SIMPAN KE CSV
![image](https://github.com/user-attachments/assets/de8e9dd3-5248-4272-92eb-578e8948653e)
- Penjelasan Kode
1. with open("transaksi.csv", mode="w", newline='') as file:
- Membuka (atau membuat) file transaksi.csv dalam mode tulis (w).
- Setiap pemanggilan fungsi ini akan menimpa isi file dengan isi baru dari transaksi_list.
- newline='' digunakan agar tidak terjadi baris kosong ganda di sistem Windows saat menulis CSV.
2. fieldnames = ["tanggal", "jenis", "jumlah", "kategori"]
- Mendefinisikan nama-nama kolom yang akan digunakan sebagai header dalam file CSV.
- Harus sesuai dengan key pada dictionary di transaksi_list.
3. writer = csv.DictWriter(file, fieldnames=fieldnames)
- Membuat objek penulis CSV (DictWriter) yang akan menulis dictionary ke file sesuai kolom yang sudah ditentukan.
4. writer.writeheader()
- Menulis baris pertama pada file CSV, yaitu nama kolom sesuai dengan fieldnames.
5. writer.writerows(transaksi_list)
- Menulis seluruh transaksi ke file CSV dalam bentuk baris-baris data.
- Setiap item di transaksi_list adalah dictionary, yang cocok dengan kolom yang didefinisikan.

# FUNGSI TAMBAH TRANSAKSI
![image](https://github.com/user-attachments/assets/b01e2eda-7996-4086-a068-bd057780be96)
- Penjelasan Kode
1. Input Tanggal dan Validasi
   tanggal = input("Tanggal (YYYY-MM-DD): ")
   datetime.strptime(tanggal, "%Y-%m-%d")
   * Pengguna diminta menginput tanggal transaksi.
   * Fungsi `datetime.strptime()` digunakan untuk mengecek apakah format tanggal valid (`YYYY-MM-DD`).
   * Jika format salah, program menampilkan error dan keluar dari fungsi.

2. Input Jenis Transaksi
   jenis = input("Jenis (pemasukan/pengeluaran): ")
   if jenis not in ["pemasukan", "pengeluaran"]:
       print("Jenis tidak valid.")
       return
   * Validasi jenis transaksi agar hanya bisa menerima dua nilai: `pemasukan` atau `pengeluaran`.

3. Input Jumlah
   jumlah = int(input("Jumlah: "))
   * Pengguna diminta menginput nominal uang.
   * Konversi ke `int`. Jika input bukan angka, akan menampilkan pesan error.

4. Input Kategori dan Validasi
   kategori = input("Kategori: ")
   if kategori not in kategori_map:
       print("Kategori tidak tersedia.")
       return
   * Kategori harus cocok dengan yang ada di `kategori_map`.
   * Jika tidak ditemukan, input dianggap tidak valid.

5. Simpan Transaksi ke List
   transaksi_list.append({...})
   * Transaksi yang valid ditambahkan ke dalam list `transaksi_list` sebagai dictionary.

6. Simpan ke File dan Konfirmasi
   simpan_transaksi()
   print("Transaksi berhasil ditambahkan!")
   * Memanggil fungsi `simpan_transaksi()` untuk menyimpan ke `transaksi.csv`.
   * Memberikan umpan balik ke pengguna bahwa transaksi berhasil.

# FUNGSI TAMPILKAN TRANSAKSI
![image](https://github.com/user-attachments/assets/55018e0e-9ff3-484b-b090-2f6b2cdd333d)
- Penjelasan Kode
1. Cek Apakah Data Kosong
   if not transaksi_list:
       print("Belum ada transaksi.")
       return
   * Mengecek apakah `transaksi_list` kosong.
   * Jika belum ada transaksi yang tercatat, program akan mencetak pesan dan keluar dari fungsi.

2. Menampilkan Header
   print("\n--- Daftar Transaksi ---")
   * Memberikan judul tampilan daftar transaksi agar antarmuka CLI lebih terstruktur.

3. Menampilkan Setiap Transaksi
   for idx, t in enumerate(transaksi_list):
       print(f"{idx+1}. {t['tanggal']} | {t['jenis']} | Rp{t['jumlah']} | {t['kategori']}")
   * Melakukan iterasi terhadap `transaksi_list`.
   * Menggunakan `enumerate()` untuk menambahkan nomor urut (1, 2, 3, …).
   * Menampilkan data transaksi berupa:
     * Tanggal
     * Jenis transaksi (`pemasukan` / `pengeluaran`)
     * Jumlah uang (`Rp`)
     * Kategori transaksi

# FUNGSI UPDATE
![image](https://github.com/user-attachments/assets/0be2ac5e-bbba-4fb1-95d0-dad1fedb076d)
- Penjelasan Kode
1. Menampilkan Transaksi
   tampilkan_transaksi()
   * Menampilkan semua transaksi agar pengguna tahu nomor transaksi mana yang akan diubah.

2. Input Nomor Transaksi
   idx = int(input("Pilih nomor transaksi...")) - 1
   * Mengubah input ke indeks list (dimulai dari 0).
   * Validasi agar tidak di luar batas list (`IndexError`).

3. Input Data Baru
   print("Biarkan kosong jika tidak ingin mengubah.")
   tanggal = input(...)
   jenis = input(...)
   jumlah = input(...)
   kategori = input(...)
   * Pengguna dapat mengisi ulang data yang ingin diubah.
   * Jika dibiarkan kosong, data lama tetap digunakan.

4. Validasi dan Update
   * Jika tanggal baru diisi, dilakukan validasi format:
     datetime.strptime(tanggal, "%Y-%m-%d")
   * Jenis transaksi harus `pemasukan` atau `pengeluaran`.
   * Jumlah harus angka (`isdigit()`).
   * Kategori dicek apakah ada di `kategori_map`.

5. Simpan dan Konfirmasi
   simpan_transaksi()
   print("Transaksi berhasil diubah.")
   * Menyimpan perubahan ke file `transaksi.csv`.
   * Memberikan notifikasi ke pengguna bahwa update berhasil.

# FUNGSI HAPUS
![image](https://github.com/user-attachments/assets/a19594a1-6986-4f6a-9285-74abb59b8fa7)
- Penjelasan Kode
1. Tampilkan Semua Transaksi
   tampilkan_transaksi()
   * Menampilkan semua transaksi yang tersimpan agar pengguna bisa melihat dan memilih mana yang akan dihapus.

2. Input Nomor Transaksi
   idx = int(input(...)) - 1
   * Mengubah input dari pengguna menjadi indeks list Python (yang dimulai dari 0).
   * Jika nomor tidak valid (di luar batas list), maka muncul pesan error.

3. Validasi Input
   if idx < 0 or idx >= len(transaksi_list):
       print("Indeks tidak valid.")
   * Menjamin bahwa hanya transaksi yang ada yang bisa dihapus.

4. Hapus Data

   transaksi_list.pop(idx)
   * Menghapus transaksi pada indeks yang dipilih.

5. Simpan Perubahan
   simpan_transaksi()
   print("Transaksi berhasil dihapus.")
   * Setelah penghapusan, data baru disimpan kembali ke `transaksi.csv`.
   * Menampilkan konfirmasi ke pengguna.

# LAPORAN BULANAN
![image](https://github.com/user-attachments/assets/ef4a7a81-6411-4c17-bd5e-7345d7de76fa)
- Penjelasan Kode
1. Input Bulan dan Tahun
   bulan = input("Masukkan bulan (MM): ")
   tahun = input("Masukkan tahun (YYYY): ")
   * Pengguna diminta untuk menentukan bulan (`01`–`12`) dan tahun (`YYYY`) yang ingin dilihat laporannya.

2. Inisialisasi Total
   pemasukan, pengeluaran = 0, 0
   * Dua variabel digunakan untuk menghitung total pemasukan dan pengeluaran.

3. Loop dan Filter Transaksi
   for t in transaksi_list:
       tgl = datetime.strptime(t["tanggal"], "%Y-%m-%d")
       if tgl.month == int(bulan) and tgl.year == int(tahun):
   * Setiap transaksi diubah dari string menjadi objek tanggal (`datetime`).
   * Dicek apakah bulan dan tahun transaksi sama dengan yang diminta.

4. Hitung Pemasukan dan Pengeluaran
   if t["jenis"] == "pemasukan":
       pemasukan += jumlah
   else:
       pengeluaran += jumlah
   * Menambahkan nominal transaksi ke total pemasukan atau pengeluaran.

5. Tampilkan Hasil Laporan
   print(f"Laporan Bulan {bulan}-{tahun}")
   print(f"Pemasukan  : Rp{pemasukan}")
   print(f"Pengeluaran: Rp{pengeluaran}")
   print(f"Saldo      : Rp{pemasukan - pengeluaran}")

# LAPORAN TAHUNAN
![image](https://github.com/user-attachments/assets/84a8aedb-aa6f-4218-b208-7bff162e2b2b)
- Penjelasan Kode
1. Input Tahun
   tahun = input("Masukkan tahun (YYYY): ")
   * Pengguna memasukkan tahun yang ingin dilihat laporannya, misalnya `2025`.

2. Inisialisasi Struktur Data Bulanan
   bulanan = defaultdict(lambda: {"pemasukan": 0, "pengeluaran": 0})
   * Membuat dictionary untuk setiap bulan, otomatis berisi 0 untuk pemasukan dan pengeluaran.
   * Gunakan `defaultdict` agar tidak perlu inisialisasi manual untuk setiap bulan.

3. Filter dan Akumulasi Data
   for t in transaksi_list:
       tgl = datetime.strptime(t["tanggal"], "%Y-%m-%d")
       if tgl.year == int(tahun):
   * Looping semua transaksi, ubah tanggal dari string ke objek `datetime`.
   * Jika tahun transaksi cocok dengan input, lanjutkan proses.

4. Akumulasi Pemasukan dan Pengeluaran
   if t["jenis"] == "pemasukan":
       bulanan[tgl.month]["pemasukan"] += jumlah
   else:
       bulanan[tgl.month]["pengeluaran"] += jumlah
   * Menambahkan jumlah ke bulan yang sesuai, berdasarkan jenis transaksinya.

5. Tampilkan Laporan
   for bulan in range(1, 13):
   * Loop dari Januari sampai Desember (1–12).
   * Tampilkan total pemasukan, pengeluaran, dan saldo tiap bulan.
  
# MENU UTAMA
![image](https://github.com/user-attachments/assets/d5ce4711-3265-4936-8931-7c1cee7a9510)
- Penjelasan Kode
1. Inisialisasi Data
load_kategori()
load_transaksi()
* Memuat data dari file CSV:
  * Kategori ke dalam `kategori_map`
  * Transaksi ke dalam `transaksi_list`

2. Loop Menu Utama
while True:
    print(...)  # Tampilkan menu
    pilihan = input(...)
* Menampilkan daftar pilihan fitur aplikasi.
* Menunggu input dari pengguna (angka 1–7).

3. Menjalankan Fitur
if pilihan == "1":
    tambah_transaksi()
* Menyesuaikan input pengguna dengan fungsi yang sesuai:
  * Tambah, lihat, ubah, hapus transaksi
  * Laporan bulanan dan tahunan

4. Keluar dari Program
elif pilihan == "7":
    print("Terima kasih!")
    break

* Keluar dari loop dan mengakhiri program secara elegan.

5. Validasi Pilihan**
else:
    print("Pilihan tidak valid!")
* Jika pengguna memasukkan angka selain 1–7, akan muncul pesan peringatan.

- Penjelasan `if __name__ == "__main__":`
* Baris ini adalah **standar Python** untuk menentukan titik masuk program.
* Saat file `main.py` dijalankan secara langsung (`python main.py`), fungsi `main()` akan dipanggil.
* Jika file ini diimpor dari file lain, maka `main()` **tidak akan dijalankan otomatis**, yang penting untuk modularitas kode.
