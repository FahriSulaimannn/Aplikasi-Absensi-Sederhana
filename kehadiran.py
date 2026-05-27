from conn import db, get_cursor


def select_all_kehadiran():
    cursor = get_cursor()

    q = """
    SELECT
        kehadiran.id,
        karyawan.nama,
        karyawan.posisi,
        kehadiran.status,
        kehadiran.jam_masuk,
        kehadiran.jam_keluar,
        kehadiran.dibuat_pada
    FROM kehadiran
    JOIN karyawan
        ON kehadiran.id_karyawan = karyawan.id
    ORDER BY kehadiran.dibuat_pada DESC;
    """

    cursor.execute(q)
    result = cursor.fetchall()

    for x in result:
        print(x)

    cursor.close()


def select_kehadiran_by_id(id):
    cursor = get_cursor()

    q = """
    SELECT
        kehadiran.id,
        karyawan.nama,
        kehadiran.status,
        kehadiran.jam_masuk,
        kehadiran.jam_keluar,
        kehadiran.catatan
    FROM kehadiran
    JOIN karyawan
        ON kehadiran.id_karyawan = karyawan.id
    WHERE kehadiran.id = %s;
    """

    cursor.execute(q, (id,))
    result = cursor.fetchone()

    print(result)

    cursor.close()


def select_kehadiran_by_id_karyawan(id):
    cursor = get_cursor()

    q = """
    SELECT
        kehadiran.id,
        karyawan.nama,
        kehadiran.status,
        kehadiran.jam_masuk,
        kehadiran.jam_keluar,
        kehadiran.catatan
    FROM kehadiran
    JOIN karyawan
        ON kehadiran.id_karyawan = karyawan.id
    WHERE kehadiran.id_karyawan = %s;
    """

    cursor.execute(q, (id,))
    result = cursor.fetchone()

    print(result)

    cursor.close()


def create_kehadiran(id_karyawan, status, catatan=None):
    cursor = get_cursor()

    q = """
    INSERT INTO kehadiran (
        id_karyawan,
        status,
        jam_masuk,
        catatan
    )
    VALUES (%s, %s, NOW(), %s);
    """

    values = (id_karyawan, status, catatan)

    cursor.execute(q, values)

    db.commit()
    cursor.close()


def update_jam_keluar(id_karyawan, dibuat_pada):
    cursor = get_cursor()

    q = """
    UPDATE kehadiran
    SET jam_keluar = NOW()
    WHERE id_karyawan = %s
    AND dibuat_pada = %s;
    """

    values = (id_karyawan, dibuat_pada)

    cursor.execute(q, values)

    db.commit()
    cursor.close()
