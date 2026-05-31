import tkinter as tk
from tkinter import ttk
from UI.halaman_karyawan import HalamanKaryawan

class AplikasiAbsensi:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplikasi Absensi")
        self.root.geometry("550x450")
        
        # Aktifkan tema modern bawaan Tkinter
        ttk.Style().theme_use('clam')

        # Container untuk menampung halaman
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Dictionary untuk menyimpan Frame halaman
        self.frames = {}
        self.buat_halaman()
        self.tampil_halaman("Dashboard")

        self.root.mainloop()

    def buat_halaman(self):
        # --- HALAMAN DASHBOARD ---
        dash = ttk.Frame(self.container, padding=20)
        
        ttk.Label(dash, text="Dashboard Absensi", font=("Arial", 18, "bold")).pack(pady=20)
        ttk.Button(dash, text="✅ Catat Presensi").pack(pady=10, ipadx=20, ipady=10)

        # Menu Navigasi Tengah
        menu_frame = ttk.Frame(dash)
        menu_frame.pack(pady=40)

        ttk.Button(menu_frame, text="👥 Kelola Karyawan", command=lambda: self.tampil_halaman("Karyawan")).grid(row=0, column=0, padx=5, ipady=5)
        ttk.Button(menu_frame, text="🏬 Kelola Divisi").grid(row=0, column=1, padx=5, ipady=5)
        ttk.Button(menu_frame, text="📊 Laporan").grid(row=0, column=2, padx=5, ipady=5)

        self.frames["Dashboard"] = dash

        # --- HALAMAN KARYAWAN ---
        self.frames["Karyawan"] = HalamanKaryawan(self.container, kembali_fn=lambda: self.tampil_halaman("Dashboard"))

    def tampil_halaman(self, nama):
        # Sembunyikan semua halaman, lalu tampilkan yang dipilih
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[nama].pack(fill="both", expand=True)

if __name__ == "__main__":
    AplikasiAbsensi()