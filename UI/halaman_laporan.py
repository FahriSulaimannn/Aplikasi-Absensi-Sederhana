import tkinter as tk
from tkinter import ttk, messagebox

try:
    from service.laporan import laporan_perdivisi, statistik_kehadiran
    DB_OK = True
except Exception:
    DB_OK = False

class HalamanLaporan(ttk.Frame):
    def __init__(self, parent, kembali_fn):
        super().__init__(parent, padding=15)
        self.kembali_fn = kembali_fn

        self.build_ui()
        self.muat_data()

    def build_ui(self):
        # 1. Header
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))

        ttk.Button(header, text="← Kembali", command=self.kembali_fn).pack(side="left")
        ttk.Label(header, text="📊 Laporan Hari Ini", font=("Arial", 14, "bold")).pack(side="left", padx=15)
        
        # Tombol Refresh diletakkan di kanan
        ttk.Button(header, text="🔄 Refresh", command=self.muat_data).pack(side="right")

        # 2. Sistem Tab (Notebook) yang jauh lebih ringkas dengan ttk
        tab_control = ttk.Notebook(self)
        tab_control.pack(fill="both", expand=True, pady=5)

        self.tab_detail = ttk.Frame(tab_control)
        self.tab_stat = ttk.Frame(tab_control)

        tab_control.add(self.tab_detail, text="📋 Detail Kehadiran")
        tab_control.add(self.tab_stat, text="📈 Statistik Divisi")

        # --- SETUP TAB 1: TABEL DETAIL ---
        kolom_detail = ("Divisi", "Karyawan", "Email", "Status", "Jam Masuk", "Jam Keluar")
        self.tree_detail = ttk.Treeview(self.tab_detail, columns=kolom_detail, show="headings")
        
        lebar_detail = [("Divisi", 100), ("Karyawan", 120), ("Email", 140), 
                        ("Status", 70), ("Jam Masuk", 120), ("Jam Keluar", 120)]
        for col, w in lebar_detail:
            self.tree_detail.heading(col, text=col)
            self.tree_detail.column(col, width=w, anchor="center" if col == "Status" else "w")
            
        self.tree_detail.pack(fill="both", expand=True, pady=10)

        # --- SETUP TAB 2: TABEL STATISTIK ---
        kolom_stat = ("Divisi", "Total Karyawan", "Hadir", "Izin", "Sakit", "Alpha")
        self.tree_stat = ttk.Treeview(self.tab_stat, columns=kolom_stat, show="headings")
        
        lebar_stat = [("Divisi", 150), ("Total Karyawan", 90), ("Hadir", 70), 
                      ("Izin", 70), ("Sakit", 70), ("Alpha", 70)]
        for col, w in lebar_stat:
            self.tree_stat.heading(col, text=col)
            self.tree_stat.column(col, width=w, anchor="center" if col != "Divisi" else "w")
            
        self.tree_stat.pack(fill="both", expand=True, pady=10)

    # --- LOGIKA DATABASE ---
    def muat_data(self):
        # Bersihkan tabel lama setiap kali direfresh
        self.tree_detail.delete(*self.tree_detail.get_children())
        self.tree_stat.delete(*self.tree_stat.get_children())

        if not DB_OK: return

        # Memasukkan data Detail ke tabel
        try:
            for r in laporan_perdivisi():
                # Urutan dari DB: divisi, karyawan, email, status, dibuat_pada, masuk, keluar
                self.tree_detail.insert("", "end", values=(r[0], r[1], r[2], str(r[3]).upper(), r[5] or "-", r[6] or "-"))
        except Exception as e:
            messagebox.showerror("Error Detail", f"Gagal memuat detail laporan: {e}")

        # Memasukkan data Statistik ke tabel
        try:
            for r in statistik_kehadiran():
                # Urutan dari DB: divisi, total, hadir, izin, sakit, alpha
                self.tree_stat.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], r[5]))
        except Exception as e:
            messagebox.showerror("Error Statistik", f"Gagal memuat statistik: {e}")