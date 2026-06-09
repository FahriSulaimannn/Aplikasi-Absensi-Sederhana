from conn import db, get_cursor


def laporan_perdivisi():
    q = """
    SELECT
        d.nama AS nama_divisi,
        k.nama AS nama_karyawan,
        k.email,
        kh.status,
        kh.dibuat_pada,
        kh.jam_masuk,
        kh.jam_keluar
    FROM divisi d
    JOIN karyawan k
        ON d.id = k.id_divisi
    JOIN kehadiran kh
        ON k.id = kh.id_karyawan
    WHERE kh.dibuat_pada = CURRENT_DATE()
    ORDER BY d.nama, k.nama, kh.dibuat_pada DESC
    """

    cur = get_cursor()
    cur.execute(q)
    data = cur.fetchall()
    cur.close()

    return data


def statistik_kehadiran():
    q = """
    SELECT
        d.nama AS nama_divisi,
        COUNT(*) AS total,
        SUM(kh.status = 'hadir') AS hadir,
        SUM(kh.status = 'izin') AS izin,
        SUM(kh.status = 'sakit') AS sakit,
        SUM(kh.status = 'alpha') AS alpha
    FROM divisi d
    JOIN karyawan k
        ON d.id = k.id_divisi
    JOIN kehadiran kh
        ON k.id = kh.id_karyawan
    WHERE kh.dibuat_pada = CURRENT_DATE()
    GROUP BY d.id, d.nama
    ORDER BY d.nama
    """

    cur = get_cursor()
    cur.execute(q)
    data = cur.fetchall()
    cur.close()

    return data

