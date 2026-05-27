CREATE TABLE kehadiran (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_karyawan INT UNSIGNED NOT NULL,
    status ENUM('hadir', 'izin', 'sakit', 'alpha') NOT NULL,
    catatan VARCHAR(255),
    dibuat_pada DATE NOT NULL DEFAULT (CURRENT_DATE),
    jam_masuk DATETIME,
    jam_keluar DATETIME,

    CONSTRAINT fk_karyawan_kehadiran
        FOREIGN KEY (id_karyawan)
        REFERENCES karyawan(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
