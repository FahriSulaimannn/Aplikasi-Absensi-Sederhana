import tkinter as tk
from tkinter import ttk, messagebox

try:
    from service.karyawan import tampil_karyawan, tambah_karyawan, update_karyawan, hapus_karyawan
    from service.divisi import tampil_divisi
    DB_OK = True
except Exception:
    DB_OK = False

class HalamanKaryawan(ttk.Frame):
    def __init__(self, parent, kembali_fn):
        super().__init__(parent, padding=15)
        self.kembali_fn = kembali_fn
        self.list_divisi = []
        
        self.build_ui()
        self.muat_data()

    def build_ui(self):
        # 1. Header & Tombol Aksi
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))
        
        ttk.Button(header, text="← Kembali", command=self.kembali_fn).pack(side="left")
        ttk.Label(header, text="👥 Kelola Karyawan", font=("Arial", 14, "bold")).pack(side="left", padx=15)

        aksi = ttk.Frame(self)
        aksi.pack(fill="x", pady=5)
        ttk.Button(aksi, text="➕ Tambah", command=lambda: self.buka_form(is_edit=False)).pack(side="left", padx=2)
        ttk.Button(aksi, text="✏️ Edit", command=lambda: self.buka_form(is_edit=True)).pack(side="left", padx=2)
        ttk.Button(aksi, text="🗑️ Hapus", command=self.hapus_data).pack(side="left", padx=2)

        # 2. Tabel Data
        kolom = ("ID", "Nama", "Telepon", "Email", "Posisi", "Divisi")
        self.tree = ttk.Treeview(self, columns=kolom, show="headings")
        
        pengaturan_kolom = [("ID", 40), ("Nama", 150), ("Telepon", 100), ("Email", 150), ("Posisi", 90), ("Divisi", 100)]
        for col, width in pengaturan_kolom:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
            
        self.tree.pack(fill="both", expand=True, pady=5)

    # --- LOGIKA DATABASE & TABEL ---
    def muat_data(self):
        self.tree.delete(*self.tree.get_children())
        if not DB_OK: return
        
        # Ambil data divisi untuk disimpan di memori (digunakan untuk combobox)
        try:
            self.list_divisi = [{"id": r[0], "nama": r[1]} for r in tampil_divisi()]
        except Exception:
            pass

        # Ambil data karyawan ke tabel
        for r in tampil_karyawan():
            # r urutan: (id, nama, telp, email, alamat, posisi, id_div, nama_div)
            self.tree.insert("", "end", iid=str(r[0]), values=(r[0], r[1], r[2], r[3], r[5].capitalize(), r[7] or "—"))

    def get_id(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("Pilih Data", "Pilih karyawan di tabel terlebih dahulu!")
        return int(sel[0]) if sel else None

    # --- LOGIKA FORMULIR (TAMBAH & EDIT) ---
    def buka_form(self, is_edit):
        id_karyawan = self.get_id() if is_edit else None
        if is_edit and not id_karyawan: return

        pop = tk.Toplevel(self)
        pop.title("Edit Karyawan" if is_edit else "Tambah Karyawan")
        pop.geometry("320x300")
        pop.grab_set()

        # Daftar untuk dropdown
        nama_divisi_list = [d["nama"] for d in self.list_divisi]
        posisi_list = ["manager", "supervisor", "staff", "intern"]

        fields = ["Divisi", "Nama", "Telepon", "Email", "Alamat", "Posisi"]
        entries = {}

        # Buat form secara otomatis
        for i, field in enumerate(fields):
            ttk.Label(pop, text=field).grid(row=i, column=0, sticky="w", padx=10, pady=8)
            
            # Pengkondisian khusus untuk Combobox
            if field == "Divisi":
                ent = ttk.Combobox(pop, values=nama_divisi_list, state="readonly", width=23)
                if nama_divisi_list: ent.current(0) # Set default item pertama
            elif field == "Posisi":
                ent = ttk.Combobox(pop, values=posisi_list, state="readonly", width=23)
                ent.current(2) # Set default 'staff'
            else:
                ent = ttk.Entry(pop, width=25)
                
            ent.grid(row=i, column=1, padx=10)
            entries[field] = ent

        # Jika mode edit, isi data lama ke dalam form
        if is_edit:
            data_lama = next((r for r in tampil_karyawan() if r[0] == id_karyawan), None)
            if data_lama:
                entries["Nama"].insert(0, data_lama[1])
                entries["Telepon"].insert(0, data_lama[2])
                entries["Email"].insert(0, data_lama[3])
                entries["Alamat"].insert(0, data_lama[4])
                entries["Posisi"].set(data_lama[5])
                entries["Divisi"].set(data_lama[7] if data_lama[7] else "")

        # Fungsi simpan di dalam pop up
        def simpan():
            v = {f: entries[f].get() for f in fields}
            
            # Cari ID (Integer) dari nama divisi yang diplih di combobox
            id_div = next((d["id"] for d in self.list_divisi if d["nama"] == v["Divisi"]), None)
            if not id_div:
                messagebox.showerror("Error", "Pilih divisi yang valid!", parent=pop)
                return

            try:
                if is_edit:
                    update_karyawan(id_karyawan, id_div, v["Nama"], v["Telepon"], v["Email"], v["Alamat"], v["Posisi"])
                else:
                    tambah_karyawan(id_div, v["Nama"], v["Telepon"], v["Email"], v["Alamat"], v["Posisi"])
                
                self.muat_data()
                pop.destroy()
            except Exception as e:
                messagebox.showerror("Error DB", f"Gagal menyimpan data: {e}", parent=pop)

        ttk.Button(pop, text="Simpan", command=simpan).grid(row=len(fields), column=1, sticky="e", padx=10, pady=15)

    def hapus_data(self):
        id_karyawan = self.get_id()
        if id_karyawan and messagebox.askyesno("Hapus", "Yakin hapus data ini?"):
            hapus_karyawan(id_karyawan)
            self.muat_data()