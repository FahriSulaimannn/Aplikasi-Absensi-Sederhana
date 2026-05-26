from connect import db, cursor

#insert
def tambah_divisi():
    nama = input("Masukkan nama divisi: ")

    query = """
    INSERT INTO divisi (nama)
    VALUES (%s)
    """

    data = (nama,)

    cursor.execute(query, data)
    db.commit()

    print("Divisi berhasil ditambahkan")

#select
def tampil_divisi():
    query = "SELECT * FROM divisi"

    cursor.execute(query)

    hasil = cursor.fetchall()

    print("\n=== DATA DIVISI ===")

    for data in hasil:
        print(data)

#update
def update_divisi():
    id_divisi = input("Masukkan ID divisi: ")
    nama = input("Masukkan nama divisi baru: ")

    query = """
    UPDATE divisi
    SET nama=%s
    WHERE id=%s
    """

    data = (nama, id_divisi)

    cursor.execute(query, data)
    db.commit()

    print("Divisi berhasil diupdate")

#delete
def delete_divisi():
    id_divisi = input("Masukkan ID divisi yang ingin dihapus: ")

    query = "DELETE FROM divisi WHERE id=%s"

    data = (id_divisi,)

    cursor.execute(query, data)
    db.commit()

    print("Divisi berhasil dihapus")