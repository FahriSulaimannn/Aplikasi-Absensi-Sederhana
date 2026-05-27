from conn import db, get_cursor


# insert
def tambah_divisi():
    cursor = get_cursor()
    nama = input("Masukkan nama divisi: ")

    query = """
    INSERT INTO divisi (nama)
    VALUES (%s)
    """

    data = (nama,)

    cursor.execute(query, data)
    db.commit()

    print("Divisi berhasil ditambahkan")


# select
def tampil_divisi():
    cursor = get_cursor()

    query = "SELECT * FROM divisi"

    cursor.execute(query)

    hasil = cursor.fetchall()

    print("\n=== DATA DIVISI ===")

    for data in hasil:
        print(data)


# update
def update_divisi():
    cursor = get_cursor()

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


# delete
def delete_divisi():
    cursor = get_cursor()

    id_divisi = input("Masukkan ID divisi yang ingin dihapus: ")

    query = "DELETE FROM divisi WHERE id=%s"

    data = (id_divisi,)

    cursor.execute(query, data)
    db.commit()

    print("Divisi berhasil dihapus")
