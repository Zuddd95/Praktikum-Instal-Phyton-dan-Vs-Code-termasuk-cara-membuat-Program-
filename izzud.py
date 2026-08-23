import json
import os
from statistics import mean

FILE_NAME = "data_mahasiswa.json"


# =========================
# DATA MANAGEMENT
# =========================

def load_data():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# =========================
# PERHITUNGAN NILAI
# =========================

def hitung_nilai(uts, uas, tugas, kehadiran):
    nilai_akhir = (
        uts * 0.25 +
        uas * 0.35 +
        tugas * 0.25 +
        kehadiran * 0.15
    )

    if nilai_akhir >= 85:
        grade = "A"
    elif nilai_akhir >= 75:
        grade = "B"
    elif nilai_akhir >= 65:
        grade = "C"
    elif nilai_akhir >= 50:
        grade = "D"
    else:
        grade = "E"

    status = "LULUS" if nilai_akhir >= 60 else "TIDAK LULUS"

    return round(nilai_akhir, 2), grade, status


# =========================
# TAMBAH MAHASISWA
# =========================

def tambah_mahasiswa(data):
    print("\n=== TAMBAH DATA MAHASISWA ===")

    nim = input("NIM       : ")

    if any(m["nim"] == nim for m in data):
        print("NIM sudah terdaftar!")
        return

    nama = input("Nama      : ")
    kelas = input("Kelas     : ")

    try:
        uts = float(input("Nilai UTS  : "))
        uas = float(input("Nilai UAS  : "))
        tugas = float(input("Nilai Tugas: "))
        kehadiran = float(input("Kehadiran  : "))

        nilai_akhir, grade, status = hitung_nilai(
            uts, uas, tugas, kehadiran
        )

        mahasiswa = {
            "nim": nim,
            "nama": nama,
            "kelas": kelas,
            "uts": uts,
            "uas": uas,
            "tugas": tugas,
            "kehadiran": kehadiran,
            "nilai_akhir": nilai_akhir,
            "grade": grade,
            "status": status
        }

        data.append(mahasiswa)
        save_data(data)

        print("\nData berhasil ditambahkan!")
        print(f"Nilai Akhir : {nilai_akhir}")
        print(f"Grade       : {grade}")
        print(f"Status      : {status}")

    except ValueError:
        print("Input nilai harus berupa angka!")


# =========================
# TAMPILKAN DATA
# =========================

def tampilkan_data(data):
    print("\n=== DATA MAHASISWA ===")

    if not data:
        print("Belum ada data.")
        return

    print("-" * 85)
    print(
        f"{'NIM':<15}"
        f"{'Nama':<20}"
        f"{'Kelas':<10}"
        f"{'Akhir':<10}"
        f"{'Grade':<8}"
        f"{'Status':<15}"
    )
    print("-" * 85)

    for m in data:
        print(
            f"{m['nim']:<15}"
            f"{m['nama']:<20}"
            f"{m['kelas']:<10}"
            f"{m['nilai_akhir']:<10}"
            f"{m['grade']:<8}"
            f"{m['status']:<15}"
        )

    print("-" * 85)


# =========================
# PENCARIAN
# =========================

def cari_mahasiswa(data):
    keyword = input("\nMasukkan NIM/Nama: ").lower()

    hasil = [
        m for m in data
        if keyword in m["nim"].lower()
        or keyword in m["nama"].lower()
    ]

    if not hasil:
        print("Data tidak ditemukan.")
        return

    print("\n=== HASIL PENCARIAN ===")

    for m in hasil:
        print(f"""
NIM          : {m['nim']}
Nama         : {m['nama']}
Kelas        : {m['kelas']}
UTS          : {m['uts']}
UAS          : {m['uas']}
Tugas        : {m['tugas']}
Kehadiran    : {m['kehadiran']}
Nilai Akhir  : {m['nilai_akhir']}
Grade        : {m['grade']}
Status       : {m['status']}
""")


# =========================
# RANKING
# =========================

def ranking_mahasiswa(data):
    if not data:
        print("Belum ada data.")
        return

    ranking = sorted(
        data,
        key=lambda x: x["nilai_akhir"],
        reverse=True
    )

    print("\n=== RANKING MAHASISWA ===")

    for i, m in enumerate(ranking, start=1):
        print(
            f"{i}. {m['nama']} "
            f"({m['nim']}) → "
            f"{m['nilai_akhir']} "
            f"[{m['grade']}]"
        )


# =========================
# STATISTIK
# =========================

def statistik(data):
    if not data:
        print("Belum ada data.")
        return

    nilai = [m["nilai_akhir"] for m in data]

    rata_rata = mean(nilai)
    tertinggi = max(data, key=lambda x: x["nilai_akhir"])
    terendah = min(data, key=lambda x: x["nilai_akhir"])

    lulus = sum(
        1 for m in data
        if m["status"] == "LULUS"
    )

    tidak_lulus = len(data) - lulus

    print("\n=== STATISTIK AKADEMIK ===")
    print(f"Jumlah Mahasiswa : {len(data)}")
    print(f"Rata-rata Nilai  : {rata_rata:.2f}")
    print(f"Nilai Tertinggi  : {tertinggi['nilai_akhir']}")
    print(f"Pemilik          : {tertinggi['nama']}")
    print(f"Nilai Terendah   : {terendah['nilai_akhir']}")
    print(f"Pemilik          : {terendah['nama']}")
    print(f"Jumlah Lulus     : {lulus}")
    print(f"Jumlah Tidak     : {tidak_lulus}")


# =========================
# HAPUS DATA
# =========================

def hapus_mahasiswa(data):
    nim = input("\nMasukkan NIM yang ingin dihapus: ")

    for mahasiswa in data:
        if mahasiswa["nim"] == nim:
            data.remove(mahasiswa)
            save_data(data)
            print("Data berhasil dihapus.")
            return

    print("Mahasiswa tidak ditemukan.")


# =========================
# LOGIN
# =========================

def login():
    username_benar = "admin"
    password_benar = "12345"

    print("=" * 45)
    print("      SISTEM AKADEMIK MAHASISWA")
    print("=" * 45)

    for percobaan in range(3):
        username = input("Username : ")
        password = input("Password : ")

        if username == username_benar and password == password_benar:
            print("\nLogin berhasil!")
            return True

        sisa = 2 - percobaan
        print(f"Login gagal! Sisa percobaan: {sisa}")

    print("\nAkses ditolak.")
    return False


# =========================
# MENU UTAMA
# =========================

def main():
    data = load_data()

    if not login():
        return

    while True:
        print("""
╔════════════════════════════════════╗
║       SISTEM AKADEMIK v1.0         ║
╠════════════════════════════════════╣
║ 1. Tambah Mahasiswa                ║
║ 2. Tampilkan Data                  ║
║ 3. Cari Mahasiswa                  ║
║ 4. Ranking Mahasiswa               ║
║ 5. Statistik Akademik              ║
║ 6. Hapus Mahasiswa                 ║
║ 7. Keluar                          ║
╚════════════════════════════════════╝
""")

        pilihan = input("Pilih menu [1-7]: ")

        if pilihan == "1":
            tambah_mahasiswa(data)

        elif pilihan == "2":
            tampilkan_data(data)

        elif pilihan == "3":
            cari_mahasiswa(data)

        elif pilihan == "4":
            ranking_mahasiswa(data)

        elif pilihan == "5":
            statistik(data)

        elif pilihan == "6":
            hapus_mahasiswa(data)

        elif pilihan == "7":
            print("\nProgram selesai. Goodbye 👋")
            break

        else:
            print("Pilihan tidak valid!")


# =========================
# PROGRAM START
# =========================

if __name__ == "_main_":
    main()