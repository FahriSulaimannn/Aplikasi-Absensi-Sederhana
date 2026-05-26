from divisi import *

menu = {
    "1": tambah_divisi,
    "2": tampil_divisi,
    "3": update_divisi,
    "4": delete_divisi
}

while True:
    print("""
Menu Divisi :
1. Tambah Divisi
2. Tampil Divisi
3. Update Divisi
4. Delete Divisi
5. Keluar
""")

    pilih = input("Pilih menu: ")

    if pilih == "5":
        print("Program selesai")
        break

    elif pilih in menu:
        menu[pilih]()

    else:
        print("Pilihan tidak valid")