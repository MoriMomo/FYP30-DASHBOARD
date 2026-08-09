# Setup Guide - FYP B30 Progress Dashboard (versi manual upload)

## Cara jalanin lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

Setelah terbuka di browser:
1. Klik tombol upload
2. Pilih file Excel kamu (yang punya banyak sheet, 1 sheet = 1 kelas)
3. Dashboard otomatis baca semua sheet dan gabungin

## Cara update data harian

Tiap hari, tinggal upload ulang file Excel terbaru ke dashboard yang sama —
tidak perlu ubah kode apapun.

## Cara deploy (biar bisa diakses tim tanpa install apa-apa)

1. Push folder ini ke GitHub (public atau private repo)
2. Buka https://share.streamlit.io/ → login dengan GitHub
3. Pilih repo ini → Deploy
4. Share link ke tim FYPL — mereka tinggal buka browser & upload file

## Catatan nama kolom

Pastikan nama kolom di semua sheet **persis sama**:
`Kelas`, `NIM FRESHMEN LEADER`, `NAMA FRESHMEN LEADER`, `NIM FRESHMEN`,
`NAMA FRESHMEN`, `prediksi point`, `point apps`, `selisih`, `Sesi yang 0`,
`Sesi yang Kosong`.

Kalau ada sheet dengan nama kolom beda (misal ada spasi tambahan atau typo),
baris tersebut bisa muncul kosong (NaN) di dashboard. App ini sudah otomatis
strip spasi di awal/akhir nama kolom, tapi typo di tengah tetap harus
konsisten manual di file Excel-nya.

## Upgrade ke auto-update (nanti kalau udah nyaman)

Kalau suatu saat capek upload manual tiap hari, versi Google Sheets
(auto-read tanpa upload) udah pernah aku buatin sebelumnya — tinggal minta
lagi kalau mau switch, struktur dashboard-nya sama persis, cuma bagian
`load_data()` yang diganti dari `file_uploader` jadi koneksi ke Google Sheets API.
