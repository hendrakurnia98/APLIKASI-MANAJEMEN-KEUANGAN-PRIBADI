import csv
from datetime import datetime
from collections import defaultdict

# Struktur Data
transaksi_list = []
kategori_map = {}

# === LOAD FILE ===
def load_kategori():
    global kategori_map
    kategori_map = {}
    try:
        with open("kategori.csv", mode="r", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                kategori_map[row['nama']] = True
    except FileNotFoundError:
        print("File kategori.csv tidak ditemukan!")

def load_transaksi():
    global transaksi_list
    transaksi_list = []
    try:
        with open("transaksi.csv", mode="r", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaksi_list.append(row)
    except FileNotFoundError:
        print("File transaksi.csv tidak ditemukan!")

# === SIMPAN KE CSV ===
def simpan_transaksi():
    with open("transaksi.csv", mode="w", newline='') as file:
        fieldnames = ["tanggal", "jenis", "jumlah", "kategori"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transaksi_list)

# === FUNGSI TAMBAH TRANSAKSI ===
def tambah_transaksi():
    tanggal = input("Tanggal (YYYY-MM-DD): ")
    try:
        datetime.strptime(tanggal, "%Y-%m-%d")
    except ValueError:
        print("Format tanggal salah!")
        return

    jenis = input("Jenis (pemasukan/pengeluaran): ")
    if jenis not in ["pemasukan", "pengeluaran"]:
        print("Jenis tidak valid.")
        return

    try:
        jumlah = int(input("Jumlah: "))
    except ValueError:
        print("Jumlah harus berupa angka.")
        return

    kategori = input("Kategori: ")
    if kategori not in kategori_map:
        print("Kategori tidak tersedia.")
        return

    transaksi_list.append({
        "tanggal": tanggal,
        "jenis": jenis,
        "jumlah": jumlah,
        "kategori": kategori
    })
    simpan_transaksi()
    print("Transaksi berhasil ditambahkan!")

# === FUNGSI TAMPILKAN TRANSAKSI ===
def tampilkan_transaksi():
    if not transaksi_list:
        print("Belum ada transaksi.")
        return

    print("\n--- Daftar Transaksi ---")
    for idx, t in enumerate(transaksi_list):
        print(f"{idx+1}. {t['tanggal']} | {t['jenis']} | Rp{t['jumlah']} | {t['kategori']}")

# === FUNGSI UPDATE ===
def update_transaksi():
    tampilkan_transaksi()
    try:
        idx = int(input("Pilih nomor transaksi yang akan diubah: ")) - 1
        if idx < 0 or idx >= len(transaksi_list):
            print("Indeks tidak valid.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    print("Biarkan kosong jika tidak ingin mengubah.")
    tanggal = input("Tanggal baru (YYYY-MM-DD): ")
    jenis = input("Jenis baru (pemasukan/pengeluaran): ")
    jumlah = input("Jumlah baru: ")
    kategori = input("Kategori baru: ")

    if tanggal:
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            transaksi_list[idx]["tanggal"] = tanggal
        except ValueError:
            print("Format tanggal salah!")

    if jenis in ["pemasukan", "pengeluaran"]:
        transaksi_list[idx]["jenis"] = jenis

    if jumlah.isdigit():
        transaksi_list[idx]["jumlah"] = jumlah

    if kategori and kategori in kategori_map:
        transaksi_list[idx]["kategori"] = kategori

    simpan_transaksi()
    print("Transaksi berhasil diubah.")

# === FUNGSI HAPUS ===
def hapus_transaksi():
    tampilkan_transaksi()
    try:
        idx = int(input("Pilih nomor transaksi yang akan dihapus: ")) - 1
        if idx < 0 or idx >= len(transaksi_list):
            print("Indeks tidak valid.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    transaksi_list.pop(idx)
    simpan_transaksi()
    print("Transaksi berhasil dihapus.")

# === LAPORAN BULANAN ===
def laporan_bulanan():
    bulan = input("Masukkan bulan (MM): ")
    tahun = input("Masukkan tahun (YYYY): ")

    pemasukan, pengeluaran = 0, 0

    for t in transaksi_list:
        try:
            tgl = datetime.strptime(t["tanggal"], "%Y-%m-%d")
            if tgl.month == int(bulan) and tgl.year == int(tahun):
                jumlah = int(t["jumlah"])
                if t["jenis"] == "pemasukan":
                    pemasukan += jumlah
                else:
                    pengeluaran += jumlah
        except:
            continue

    print(f"\nLaporan Bulan {bulan}-{tahun}")
    print(f"Pemasukan  : Rp{pemasukan}")
    print(f"Pengeluaran: Rp{pengeluaran}")
    print(f"Saldo      : Rp{pemasukan - pengeluaran}")

# === LAPORAN TAHUNAN ===
def laporan_tahunan():
    tahun = input("Masukkan tahun (YYYY): ")
    bulanan = defaultdict(lambda: {"pemasukan": 0, "pengeluaran": 0})

    for t in transaksi_list:
        try:
            tgl = datetime.strptime(t["tanggal"], "%Y-%m-%d")
            if tgl.year == int(tahun):
                jumlah = int(t["jumlah"])
                if t["jenis"] == "pemasukan":
                    bulanan[tgl.month]["pemasukan"] += jumlah
                else:
                    bulanan[tgl.month]["pengeluaran"] += jumlah
        except:
            continue

    print(f"\nLaporan Tahunan {tahun}")
    for bulan in range(1, 13):
        p = bulanan[bulan]["pemasukan"]
        q = bulanan[bulan]["pengeluaran"]
        print(f"Bulan {bulan:02d}: Pemasukan Rp{p}, Pengeluaran Rp{q}, Saldo Rp{p - q}")

# === MENU UTAMA ===
def main():
    load_kategori()
    load_transaksi()

    while True:
        print("\n=== MENU APLIKASI MANAJEMEN KEUANGAN ===")
        print("1. Tambah Transaksi")
        print("2. Lihat Transaksi")
        print("3. Ubah Transaksi")
        print("4. Hapus Transaksi")
        print("5. Laporan Bulanan")
        print("6. Laporan Tahunan")
        print("7. Keluar")

        pilihan = input("Pilih menu (1-7): ")
        if pilihan == "1":
            tambah_transaksi()
        elif pilihan == "2":
            tampilkan_transaksi()
        elif pilihan == "3":
            update_transaksi()
        elif pilihan == "4":
            hapus_transaksi()
        elif pilihan == "5":
            laporan_bulanan()
        elif pilihan == "6":
            laporan_tahunan()
        elif pilihan == "7":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
    