CREATE TABLE karyawan (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_divisi INT UNSIGNED NOT NULL,

    nama VARCHAR(100) NOT NULL,
    no_telp VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    alamat VARCHAR(255) NOT NULL,

    posisi ENUM(
        'manager',
        'supervisor',
        'staff',
        'intern'
    ) NOT NULL,

    CONSTRAINT fk_karyawan_divisi
        FOREIGN KEY (id_divisi)
        REFERENCES divisi(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
