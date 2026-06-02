import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    from service.kehadiran import select_all_kehadiran, create_kehadiran, update_jam_keluar
    from service.karyawan import tampil_karyawan
    DB_OK = True
except Exception:
    DB_OK = False

class HalamanPresensi(ttk.Frame):
    def __init__(self, parent, kembali_fn):
        super().__init__(parent, padding=15)
        self.kembali_fn = kembali_fn
        self.list_karyawan = []
        
        self.build_ui()
        self.muat_data()

    def build_ui(self):
        # 1. Header & Tombol Aksi
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))
        
        ttk.Button(header, text="← Kembali", command=self.kembali_fn).pack(side="left")
        ttk.Label(header, text="✅ Catat Presensi", font=("Arial", 14, "bold")).pack(side="left", padx=15)

        aksi = ttk.Frame(self)
        aksi.pack(fill="x", pady=5)
        ttk.Button(aksi, text="➕ Catat Masuk / Izin", command=self.buka_form_masuk).pack(side="left", padx=2)
        ttk.Button(aksi, text="🕒 Catat Jam Keluar", command=self.catat_keluar).pack(side="left", padx=2)

        # 2. Tabel Data Presensi
        kolom = ("ID", "Nama Karyawan", "Posisi", "Status", "Jam Masuk", "Jam Keluar", "Tanggal", "ID_K")
        self.tree = ttk.Treeview(self, columns=kolom, show="headings")
        
        pengaturan = [
            ("ID", 40), ("Nama Karyawan", 140), ("Posisi", 80),
            ("Status", 70), ("Jam Masuk", 130), ("Jam Keluar", 130), ("Tanggal", 90)
        ]
        for col, width in pengaturan:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center" if col != "Nama Karyawan" else "w")
            
        # Sembunyikan kolom ID Karyawan (hanya untuk sistem update jam keluar)
        self.tree.heading("ID_K", text="")
        self.tree.column("ID_K", width=0, stretch=tk.NO)

        self.tree.pack(fill="both", expand=True, pady=5)

    # --- LOGIKA DATABASE & TABEL ---
    def muat_data(self):
        self.tree.delete(*self.tree.get_children())
        if not DB_OK: return
        
        # Ambil data karyawan untuk combobox di form presensi
        try:
            self.list_karyawan = [{"id": r[0], "nama": r[1]} for r in tampil_karyawan()]
        except Exception:
            pass

        # Ambil data riwayat presensi ke tabel
        try:
            for r in select_all_kehadiran():
                # r urutan: id, nama, posisi, status, jam_masuk, jam_keluar, dibuat_pada, id_karyawan
                self.tree.insert("", "end", iid=str(r[0]), values=(
                    r[0], r[1], r[2].capitalize(), r[3].upper(), 
                    r[4] or "-", r[5] or "-", r[6], r[7]
                ))
        except Exception as e:
            messagebox.showerror("Error DB", f"Gagal memuat data presensi: {e}")

    # --- LOGIKA FORMULIR ---
    def buka_form_masuk(self):
        pop = tk.Toplevel(self)
        pop.title("Catat Kehadiran Baru")
        pop.geometry("340x220")
        pop.grab_set()

        # Input Karyawan (Combobox)
        ttk.Label(pop, text="Karyawan").grid(row=0, column=0, sticky="w", padx=15, pady=15)
        nama_list = [k["nama"] for k in self.list_karyawan]
        cb_karyawan = ttk.Combobox(pop, values=nama_list, state="readonly", width=25)
        cb_karyawan.grid(row=0, column=1, padx=10, pady=15)
        if nama_list: cb_karyawan.current(0)

        # Input Status (Combobox)
        ttk.Label(pop, text="Status").grid(row=1, column=0, sticky="w", padx=15, pady=5)
        cb_status = ttk.Combobox(pop, values=["hadir", "izin", "sakit", "alpha"], state="readonly", width=25)
        cb_status.grid(row=1, column=1, padx=10, pady=5)
        cb_status.current(0)

        # Input Catatan
        ttk.Label(pop, text="Catatan (Opsional)").grid(row=2, column=0, sticky="w", padx=15, pady=15)
        ent_catatan = ttk.Entry(pop, width=28)
        ent_catatan.grid(row=2, column=1, padx=10, pady=15)

        def simpan():
            nama = cb_karyawan.get()
            status = cb_status.get()
            catatan = ent_catatan.get().strip() or None

            # Ambil ID Karyawan dari nama yang dipilih
            id_k = next((k["id"] for k in self.list_karyawan if k["nama"] == nama), None)
            if not id_k:
                messagebox.showwarning("Error", "Pilih karyawan yang valid!", parent=pop)
                return

            try:
                create_kehadiran(id_k, status, catatan)
                self.muat_data()
                pop.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan data: {e}", parent=pop)

        ttk.Button(pop, text="Simpan", command=simpan).grid(row=3, column=1, sticky="e", padx=10, pady=15)

    def catat_keluar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Pilih Data", "Pilih data presensi di tabel terlebih dahulu!")
            return

        item = self.tree.item(sel[0])["values"]
        # Index Item: 0=ID, 1=Nama, 2=Posisi, 3=Status, 4=Masuk, 5=Keluar, 6=Tanggal, 7=ID_Karyawan

        if str(item[3]).lower() != "hadir":
            messagebox.showwarning("Perhatian", "Hanya status 'Hadir' yang bisa mencatat jam keluar.")
            return

        if item[5] != "-":
            messagebox.showinfo("Perhatian", "Jam keluar sudah tercatat untuk baris ini.")
            return

        id_karyawan = item[7]
        tanggal = item[6]

        if messagebox.askyesno("Catat Keluar", f"Catat jam keluar sekarang untuk '{item[1]}'?"):
            try:
                update_jam_keluar(id_karyawan, tanggal)
                self.muat_data()
                messagebox.showinfo("Berhasil", "Jam keluar berhasil dicatat.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mencatat jam keluar: {e}")