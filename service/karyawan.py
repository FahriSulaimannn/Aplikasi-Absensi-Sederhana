from conn import db, get_cursor


def tambah_karyawan(id_divisi, nama, no_telp, email, alamat, posisi):
    cursor = get_cursor()
    sql = """
        INSERT INTO karyawan (id_divisi, nama, no_telp, email, alamat, posisi)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (id_divisi, nama, no_telp, email, alamat, posisi))
    db.commit()
    cursor.close()


def tampil_karyawan():
    cursor = get_cursor()
    sql = """
        SELECT k.id, k.nama, k.no_telp, k.email, k.alamat,
               k.posisi, k.id_divisi, d.nama AS nama_divisi
        FROM karyawan k
        LEFT JOIN divisi d ON k.id_divisi = d.id
        ORDER BY k.id
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result


def update_karyawan(id_karyawan, id_divisi, nama, no_telp, email, alamat, posisi):
    cursor = get_cursor()
    sql = """
        UPDATE karyawan
        SET id_divisi=%s, nama=%s, no_telp=%s, email=%s, alamat=%s, posisi=%s
        WHERE id=%s
    """
    cursor.execute(sql, (id_divisi, nama, no_telp, email, alamat, posisi, id_karyawan))
    db.commit()
    cursor.close()


def hapus_karyawan(id_karyawan):
    cursor = get_cursor()
    cursor.execute("DELETE FROM karyawan WHERE id=%s", (id_karyawan,))
    db.commit()
    cursor.close()