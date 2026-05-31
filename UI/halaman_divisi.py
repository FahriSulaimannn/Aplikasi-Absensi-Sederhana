import tkinter as tk
from tkinter import ttk, messagebox

try:
    from service.divisi import tampil_divisi, tambah_divisi, update_divisi, delete_divisi
    DB_OK = True
except Exception:
    DB_OK = False

class HalamanDivisi(ttk.Frame):
    def __init__(self, parent, kembali_fn):
        super().__init__(parent, padding=15)
        self.kembali_fn = kembali_fn
        self.build_ui()
        self.muat_data()

    def build_ui(self):
        # 1. Header & Tombol Aksi
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))
        
        ttk.Button(header, text="← Kembali", command=self.kembali_fn).pack(side="left")
        ttk.Label(header, text="🏬 Kelola Divisi", font=("Arial", 14, "bold")).pack(side="left", padx=15)

        aksi = ttk.Frame(self)
        aksi.pack(fill="x", pady=5)
        ttk.Button(aksi, text="➕ Tambah", command=lambda: self.buka_form(is_edit=False)).pack(side="left", padx=2)
        ttk.Button(aksi, text="✏️ Edit", command=lambda: self.buka_form(is_edit=True)).pack(side="left", padx=2)
        ttk.Button(aksi, text="🗑️ Hapus", command=self.hapus_data).pack(side="left", padx=2)

        # 2. Tabel Data Divisi
        kolom = ("ID", "Nama Divisi")
        self.tree = ttk.Treeview(self, columns=kolom, show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=60, anchor="center")
        
        self.tree.heading("Nama Divisi", text="Nama Divisi")
        self.tree.column("Nama Divisi", width=350, anchor="w")
            
        self.tree.pack(fill="both", expand=True, pady=5)

    # --- LOGIKA DATABASE & TABEL ---
    def muat_data(self):
        self.tree.delete(*self.tree.get_children()) # Bersihkan tabel
        if not DB_OK: return
        
        try:
            for r in tampil_divisi():
                # r urutan dari DB: (id, nama)
                self.tree.insert("", "end", iid=str(r[0]), values=(r[0], r[1]))
        except Exception as e:
            messagebox.showerror("Error DB", f"Gagal memuat divisi: {e}")

    def get_id(self):
        sel = self.tree.selection()
        if not sel: 
            messagebox.showwarning("Pilih Data", "Pilih divisi di tabel terlebih dahulu!")
        return int(sel[0]) if sel else None

    # --- LOGIKA FORMULIR (TAMBAH & EDIT) ---
    def buka_form(self, is_edit):
        id_divisi = self.get_id() if is_edit else None
        if is_edit and not id_divisi: return

        pop = tk.Toplevel(self)
        pop.title("Edit Divisi" if is_edit else "Tambah Divisi")
        pop.geometry("320x150")
        pop.resizable(False, False)
        pop.grab_set()

        # Input Lapangan Nama Divisi
        ttk.Label(pop, text="Nama Divisi").grid(row=0, column=0, sticky="w", padx=15, pady=20)
        ent_nama = ttk.Entry(pop, width=25)
        ent_nama.grid(row=0, column=1, padx=10, pady=20)

        # Jika mode Edit, ambil data nama lama dari DB
        if is_edit:
            try:
                data_lama = next((r for r in tampil_divisi() if r[0] == id_divisi), None)
                if data_lama:
                    ent_nama.insert(0, data_lama[1])
            except Exception:
                pass

        # Fungsi Simpan di dalam Pop Up
        def simpan():
            nama_baru = ent_nama.get().strip()
            if not nama_baru:
                messagebox.showwarning("Peringatan", "Nama divisi tidak boleh kosong!", parent=pop)
                return
            
            try:
                if is_edit:
                    update_divisi(id_divisi, nama_baru)
                else:
                    tambah_divisi(nama_baru)
                
                self.muat_data() # Refresh tabel halaman utama
                pop.destroy()    # Tutup popup
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan: {e}", parent=pop)

        ttk.Button(pop, text="Simpan", command=simpan).grid(row=1, column=1, sticky="e", padx=10, pady=10)

    def hapus_data(self):
        id_divisi = self.get_id()
        if not id_divisi: return
        
        # Mengambil nama divisi untuk pesan konfirmasi
        item = self.tree.item(str(id_divisi))
        nama_divisi = item["values"][1] if item["values"] else f"ID {id_divisi}"

        if messagebox.askyesno("Hapus", f"Yakin ingin menghapus divisi '{nama_divisi}'?"):
            try:
                delete_divisi(id_divisi)
                self.muat_data()
                messagebox.showinfo("Berhasil", f"Divisi '{nama_divisi}' berhasil dihapus.")
            except Exception as e:
                # Menangani error jika divisi masih digunakan oleh data karyawan (Foreign Key Restriction)
                messagebox.showerror("Error DB", f"Gagal menghapus data.\nPastikan tidak ada karyawan yang terdaftar di divisi ini.\n\nDetail: {e}")