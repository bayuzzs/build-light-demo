# Build Light Demo — Store Checkout

Contoh project Python untuk demo CI sungguhan: keranjang beberapa barang,
quantity, voucher HEMAT10 / HEMAT20, ongkir, dan rincian total belanja.
Semua nominal memakai integer rupiah; pecahan diskon dibulatkan ke bawah.
Gratis ongkir untuk belanja minimal Rp100.000 SETELAH diskon; selain itu Rp15.000.
Tanpa dependency tambahan. Jalankan contoh dengan `python3 calculator.py`.

## 1. Push versi benar → Success

Buka terminal di folder repo `build-light-demo`.
Kode awal sudah benar, jadi tidak perlu mengubah apa pun untuk tahap pertama.

```bash
git add calculator.py test_calculator.py README.md .github/workflows/ci.yml .gitignore
git commit -m "feat: add store checkout with vouchers and shipping"
git push -u origin main
```

Perintah push mengasumsikan branch kamu `main` dan remote `origin` sudah terpasang.
Jika belum ada remote, buat repository kosong `build-light-demo` di GitHub tanpa
README tambahan, lalu jalankan sebelum push (ganti USERNAME):

```bash
git remote add origin https://github.com/USERNAME/build-light-demo.git
```

Buka tab Actions → CI Pipeline. Tunggu run pertama selesai: **Success**.

## 2. Ubah SATU baris → push → Failure

Buka `calculator.py`, cari baris di fungsi `checkout`:

```python
discounted_subtotal = subtotal - discount
```

Ganti tanda minus menjadi plus:

```python
discounted_subtotal = subtotal + discount
```

Jangan mengubah test atau baris lain. Simpan, lalu:

```bash
git add calculator.py
git commit -m "refactor: update discounted subtotal calculation"
git push
```

Tunggu run terbaru di Actions selesai: **Failure**.
Bug ini membuat diskon justru menambah tagihan. Pada test voucher HEMAT10,
subtotal Rp120.000 dengan diskon Rp12.000 seharusnya menjadi Rp108.000,
tetapi kode bug menghasilkan Rp132.000. Test ongkir setelah diskon juga gagal.
Ini kegagalan test asli, bukan status gagal yang dipaksakan di workflow.

## 3. Kembalikan SATU baris → push → Success

Perbaiki baris yang sama menjadi:

```python
discounted_subtotal = subtotal - discount
```

Simpan, lalu:

```bash
git add calculator.py
git commit -m "fix: subtract voucher discount from subtotal"
git push
```

Tunggu run terbaru selesai: **Success**. Selesaikan setiap run sebelum push
tahap berikutnya agar urutan hasil mudah diikuti.

## Loading dan kontrol alat

Workflow mempertahankan `sleep 3` sebelum test di SETIAP run, termasuk yang
berhasil dan gagal. Total durasi bisa lebih lama karena antrean, setup, dan
checkout runner GitHub. CI ini menjalankan test, belum melakukan deployment.

ESP32 tetap menggunakan Demo Mode dan tidak otomatis tersambung ke repo ini.
Atur Queued → Running → Passed / Failed secara manual melalui web alat.
Frame manual ditahan sampai diganti. Jangan memasukkan token GitHub ke kode.

Test lokal: `python3 -m unittest -v`.
