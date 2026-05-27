from conn import db, get_cursor


def tambah_divisi(nama):
    cursor = get_cursor()

    query = """
    INSERT INTO divisi (nama)
    VALUES (%s)
    """

    data = (nama,)

    cursor.execute(query, data)
    db.commit()

    print("Divisi berhasil ditambahkan")


def tampil_divisi():
    cursor = get_cursor()

    query = "SELECT * FROM divisi"

    cursor.execute(query)
    hasil = cursor.fetchall()

    return hasil


def update_divisi(id_divisi, nama_baru):
    cursor = get_cursor()

    query = """
    UPDATE divisi
    SET nama=%s
    WHERE id=%s
    """

    data = (nama_baru, id_divisi)

    cursor.execute(query, data)
    db.commit()

    print("Divisi berhasil diupdate")


def delete_divisi(id_divisi):
    cursor = get_cursor()

    query = "DELETE FROM divisi WHERE id=%s"

    cursor.execute(query, (id_divisi,))
    db.commit()

    print("Divisi berhasil dihapus")
