# OrangeFox Recovery Builder untuk Redmi 4X (santoni / mi8937)

Repositori ini dikonfigurasi untuk melakukan kompilasi (**build**) otomatis **OrangeFox Recovery** menggunakan **GitHub Actions**, lengkap dengan dukungan fitur **WiFi** dan **App Manager**.

---

## 🚀 Cara Menjalankan Build (One-Click)

1. Buka repositori ini di GitHub.
2. Klik tab **Actions** di bagian atas menu.
3. Di panel sebelah kiri, pilih workflow **OrangeFox - Build**.
4. Klik tombol dropdown **Run workflow** di sebelah kanan.
5. Periksa input parameter (default sudah disesuaikan untuk `santoni`):
   * **OrangeFox Manifest Branch:** `12.1` (atau `11.0`)
   * **OrangeFox / TWRP Device Tree:** URL repositori device tree perangkatmu.
   * **Device Tree Branch:** Cabang/branch yang digunakan (misal: `fox_9.0`, `android-12.1`).
   * **Device Path:** `device/xiaomi/santoni`
   * **Device Codename:** `santoni`
   * **Aktifkan Dukungan WiFi:** `true` (Mencentang `TW_INCLUDE_WIFI`)
   * **Aktifkan Fitur App Manager:** `true` (`OF_DISABLE_EXTRA_EXTRACTING=0`)
6. Klik tombol hijau **Run workflow**.

---

## 📦 Mengunduh Hasil Build

Setelah proses kompilasi selesai (sekitar 1 - 2 jam tergantung server GitHub):
1. Buka tab **Releases** di halaman utama repositori GitHub kamu.
2. Temukan rilis terbaru.
3. Download file biner:
   * **`OrangeFox-*.zip`** (untuk di-flash langsung via recovery yang ada)
   * **`OrangeFox-*.img`** (untuk di-flash via fastboot: `fastboot flash recovery OrangeFox-*.img`)

---

## 🛠️ Catatan Penting
* Workflow ini menggunakan *slimhub actions* dan swap 24GB untuk memastikan server GitHub memiliki ruang harddisk dan RAM virtual yang cukup untuk proses *compile*.
* Dukungan WiFi membutuhkan *driver* wlan pada kernel perangkat yang bersangkutan.
