# FYP B30 - Freshman Progress Dashboard

Dashboard interaktif berbasis Streamlit untuk memantau progress poin Freshman (FM) di program FYP B30. Upload file Excel hasil monitoring (multi-sheet, 1 sheet = 1 kelas), dan dashboard otomatis menggabungkan semua data serta menampilkan visualisasi Freshman yang poinnya **belum sesuai** antara File Monitoring FL dan Logbook.

## Fitur

- **Upload manual** file Excel (`.xlsx`/`.xls`) dengan format 1 sheet = 1 kelas.
- Deteksi otomatis status **"Sesuai"** vs **"Belum Sesuai"** (berdasarkan `prediksi point` vs `point apps`).
- Mapping otomatis **PIC per kelas**.
- Filter interaktif di sidebar: Kelas, Status, dan PIC.
- Ringkasan jumlah total Freshman yang belum sesuai.
- Grafik bar jumlah "Belum Sesuai" per kelas.
- Tabel statistik per PIC (jumlah kelas & total Freshman yang di-handle).
- Leaderboard ranking FL berdasarkan jumlah Freshman yang belum sesuai.
- Tabel detail seluruh Freshman dengan highlight warna untuk status "Belum Sesuai".
- Link langsung ke Google Drive kumpulan bukti Logbook.

## Requirements

- Python 3.8+
- Library: `streamlit`, `pandas`, `plotly`, `openpyxl`

```bash
pip install streamlit pandas plotly openpyxl
```

## Cara Pakai

1. Clone repo ini:
   ```bash
   git clone https://github.com/username/fyp-b30-progress-dashboard.git
   cd fyp-b30-progress-dashboard
   ```
2. Install dependency (lihat di atas).
3. Jalankan dashboard:
   ```bash
   streamlit run app.py
   ```
4. Browser akan otomatis kebuka (biasanya di `http://localhost:8501`).
5. Upload file Excel hasil monitoring lewat tombol upload di halaman utama.
6. Dashboard otomatis menampilkan grafik, statistik, dan tabel detail.

## Format Input Excel

File Excel harus **multi-sheet**, dengan **1 sheet = 1 kelas** (nama sheet akan otomatis dipakai sebagai nilai kolom `Kelas`). Setiap sheet minimal harus punya kolom berikut:

| Kolom | Keterangan |
|---|---|
| `NAMA FRESHMEN LEADER` | Nama FL |
| `NAMA FRESHMEN` | Nama FP/Freshman |
| `prediksi point` | Poin yang seharusnya didapat |
| `point apps` | Poin aktual di aplikasi |
| `selisih` *(opsional)* | Selisih poin, ditampilkan di tabel detail kalau ada |
| `Sesi yang 0`, `Sesi yang Kosong` *(opsional)* | Ditampilkan di tabel detail kalau ada |

> File hasil export dari [`fyp-logbook-cleaner`](../fyp-logbook-cleaner) (`logbook_mismatch_per_kelas.xlsx`) sudah kompatibel langsung dengan format ini.

## Mapping PIC

Dashboard ini punya mapping kelas → PIC yang sudah ditulis langsung di kode (`PIC_MAPPING` di `app.py`). Kalau ada penambahan/perubahan kelas atau PIC di periode selanjutnya, edit langsung dictionary tersebut sebelum menjalankan dashboard.

## Catatan

- Dashboard tidak menyimpan data secara permanen — setiap kali dibuka ulang, file Excel harus di-upload lagi.
- Kelas yang belum ada di `PIC_MAPPING` otomatis akan ditandai sebagai **"Belum ada PIC"**.
- Link Google Drive di dashboard ini mengarah ke folder internal FYP B30 — pastikan hanya dibagikan ke pihak yang relevan.
