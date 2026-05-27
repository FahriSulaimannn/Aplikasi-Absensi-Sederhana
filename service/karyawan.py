from conn import db, get_cursor


def tambah_karyawan(id_divisi, nama, no_telp, email, alamat):
    cursor = get_cursor()

    sql = """INSERT INTO karyawan (id_divisi, nama, no_telp, email, alamat) 
            VALUES (%s, %s, %s, %s, %s)"""
    val = (id_divisi, nama, no_telp, email, alamat)
    cursor.execute(sql, val)
    db.commit()
    print("Data berhasil ditambahkan")

    cursor.close()
    db.close()


def tampil_karyawan():
    cursor = get_cursor()

    sql = "SELECT * FROM karyawan"
    cursor.execute(sql)
    result = cursor.fetchall()
    for x in result:
        print(x)

    cursor.close()
    db.close()


def update_karyawan(id_karyawan, id_divisi, nama, no_telp, email, alamat):
    cursor = get_cursor()

    sql = """UPDATE karyawan SET id_divisi = %s, nama = %s, no_telp = %s, email = %s, alamat = %s 
            WHERE id_karyawan = %s OR nama = %s"""
    val = (id_divisi, nama, no_telp, email, alamat, id_karyawan, nama)
    cursor.execute(sql, val)
    db.commit()
    print("Data berhasil diupdate")

    cursor.close()


def hapus_karyawan(id_karyawan, nama):
    cursor = get_cursor()

    sql = """DELETE FROM karyawan WHERE id_karyawan = %s OR nama = %s"""
    val = (id_karyawan, nama)
    cursor.execute(sql, val)
    db.commit()
    print("Data berhasil dihapus")

    cursor.close()

