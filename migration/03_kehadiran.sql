CREATE TABLE kehadiran (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_karyawan INT NOT NULL,
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
