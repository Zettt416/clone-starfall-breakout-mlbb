# Starfall Breakout: Retro Space Runner

Game arkade **Horizontal Side-Scroller / Space Runner** bergaya retro 8-bit yang ringan, cepat, dan adiktif layaknya *The Dinosaur Game*.

* ⚡ **Zero Dependencies & Zero Bloat**: 100% Native HTML5 Canvas + Vanilla JavaScript.
* 📦 **Offline-First & Portable**: Cukup buka `index.html` langsung di browser tanpa perlu `npm install`, bundler, atau backend server.
* 🤖 **100% Original Gemini AI Assets**: Seluruh aset dalam game (kapal pemain, asteroid biasa & lapis baja, energi bintang, nyawa *cyber heart*, ikon nova *ultimate*, dan *sprite sheet power-up*) dibuat secara eksklusif menggunakan subagent AI Gemini tanpa keterikatan hak cipta pihak ketiga.
* ⏱️ **Survival Timer**: Menghitung lama waktu bertahan hidup (menit & detik: `mm:ss`) lengkap dengan penyimpanan rekor waktu terbaik di `localStorage`.
* 🎵 **Built-in 8-bit Audio Synthesizer**: Efek suara retro (laser, ledakan, power-up chime, ultimate roar) di-generate secara matematis melalui Web Audio API tanpa perlu file audio eksternal.
* 📱 **Cross-Platform Responsive**: Mendukung kontrol keyboard di PC, mouse drag, serta D-Pad virtual dan tombol Ult di layar sentuh HP / Mobile.

---

## 🎮 Kontrol Game

| Aksi | Keyboard (Desktop) | Sentuh (Mobile / Mouse) |
|---|---|---|
| **Naik / Turun** | `W` / `S` atau `Panah Atas` / `Panah Bawah` | D-Pad `▲` / `▼` atau geser layar |
| **Mundur / Maju** | `A` / `D` atau `Panah Kiri` / `Panah Kanan` | D-Pad `◀` / `▶` atau geser layar |
| **Tembakan Utama** | Otomatis meluncur ke arah **Kanan** | Otomatis meluncur ke arah **Kanan** |
| **Stellar Blaster (Ult)** | `SPACE`, `SHIFT`, `E` | Tombol `⚡ ULT` di kanan layar (saat bar 100%) |
| **Mulai / Restart** | `SPACE`, `ENTER`, atau `R` | Ketuk tombol di layar |
| **Jeda (Pause)** | `P` atau `ESC` | Tombol ikon `⏸️` |
| **Mute / Unmute Audio** | - | Tombol ikon `🔊` |

---

## 🌟 Fitur & Mekanik Game

1. **Starfighter Ship (Stella Nova)**:
   - Pesawat tempur cyber meluncur dari sisi kiri menghadap ke kanan menembakkan laser otomatis.
   - Dilengkapi 3 Nyawa (Hearts) dan efek kebal sesaat (*i-frames*) jika tertabrak asteroid.
2. **Hitungan Waktu Bertahan (Survival Time)**:
   - Timer `SURVIVED` ditampilkan di HUD utama dalam format menit & detik (`mm:ss`).
   - Waktu bertahan hidup terbaik tersimpan otomatis di `localStorage`.
3. **Variasi Asteroid & Rintangan (Datang dari Kanan)**:
   - **Normal Asteroid**: Cepat, 1 HP.
   - **Medium Asteroid**: 3 HP, pecah menjadi 2 serpihan pecahan atas-bawah saat hancur.
   - **Armored Asteroid**: 7 HP, tebal, memberikan poin tinggi & guncangan layar.
   - **Star Asteroid**: Berkilau emas, menjatuhkan energi bintang / power-up 100%.
   - **Asteroid Wall Barrier**: Formasi dinding vertikal yang bergerak dari kanan ke kiri, menuntut pemain bermanuver mencari celah atau menembus dengan Ultimate.
4. **Power-Up Orbs**:
   - ⚡ **Rapid (R)**: Menggandakan kecepatan tembak.
   - ✦ **Multi (M)**: Tembakan menyebar 3 arah (*triple spread*).
   - ➤ **Pierce (P)**: Peluru menembus beberapa asteroid sekaligus.
   - 💥 **Burst (B)**: Memicu ledakan area (AoE) saat asteroid dihancurkan.
   - ❤️ **Heart (+)**: Memulihkan 1 nyawa (maksimal 3).
   - ⭐ **Stellar Star**: Mengisi energi Ultimate instan dan bonus skor.
5. **Stellar Blaster (Ultimate Laser)**:
   - Terisi saat menghancurkan asteroid dan mengambil energi bintang.
   - Menembakkan laser horizontal raksasa berkekuatan penuh dari moncong kapal ke ujung kanan layar yang melenyapkan seluruh rintangan seketika.
6. **Pertempuran Bos Checkpoint (Mini-Boss & Big Boss)**:
   - **Setiap 60 Detik Waktu Bertahan**: Sirine klaxon darurat berbunyi bersama *warning banner* di layar sebelum bos masuk dari arah kanan.
   - **Mini-Boss (Void Destroyer - 60s, 180s, dst.)**:
     - Pesawat tempur siluman dengan meriam plasma kembar terarah ke posisi pemain.
     - Menyebarkan asteroid lapis baja (*armored escorts*) sebagai tameng hidup.
   - **Big Boss (Titan Apex Starfall - 120s, 240s, dst.)**:
     - *Dreadnought* raksasa berlapis baja tebal dengan *health bar* boss real-time di bagian atas layar.
     - Menembakkan sebaran peluru plasma 5 arah (*5-way spread fan*).
     - **Telegraphed Railgun Laser**: Menampilkan garis bidik merah berkedip selama 1,2 detik sebagai peringatan sebelum menembakkan laser partikel horizontal dahsyat ke sepanjang layar!
   - **Loot Shower & Hadiah**: Mengalahkan bos memicu rentetan ledakan kosmik, ribuan poin bonus skor, serta menjatuhkan hujan Power-Up dan bintang energi Ultimate.
7. **Global High Score Leaderboard (Vercel Serverless Ready)**:
   - **Papan Skor Global**: Pemain bisa saling adu skor tinggi dan waktu bertahan hidup dari berbagai perangkat.
   - **Form Kirim Skor Pilot**: Saat Game Over, pemain dapat mencatat *Call-sign* (nama pilot) ke Hall of Fame.
   - **Offline-Safe & Zero Dependencies**: Menggunakan native fetch di endpoint `/api/leaderboard.js`. Jika dijalankan offline atau database belum tersambung, game otomatis menampilkan ranking demo atau rekor lokal tanpa crash.

---

## 🚀 Cara Menjalankan & Deploy ke Vercel

### 1. Jalankan Lokal (Offline)
Cukup buka file `index.html` langsung di browser, atau jalankan local server:
```powershell
python -m http.server 8000
```
Lalu buka `http://localhost:8000`.

### 2. Deploy ke Vercel dengan Global Leaderboard (Supabase / Vercel KV)
1. Push repositori ini ke GitHub / GitLab.
2. Buka [Vercel](https://vercel.com) ➔ **Add New Project** ➔ pilih repositori ini ➔ klik **Deploy**.
3. **Penyimpanan Skor Online via Supabase (Rekomendasi)**:
   - Buat Project baru gratis di [Supabase Dashboard](https://supabase.com).
   - Masuk ke menu **SQL Editor**, buka file `supabase_setup.sql` dari repositori ini (atau copy-paste isinya), lalu klik **Run**.
   - Masuk ke **Project Settings ➔ API** di Supabase, lalu salin:
     - Project URL ➔ masukkan ke Vercel Environment Variables: `SUPABASE_URL`
     - anon/public key ➔ masukkan ke Vercel Environment Variables: `SUPABASE_ANON_KEY`
4. *(Opsi Cadangan)* Jika memakai **Vercel KV / Upstash Redis**:
   - Di dashboard project Vercel ➔ klik tab **Storage** ➔ connect KV / Upstash.
5. Selesai! Seluruh pemain dari berbagai tempat sekarang bisa saling bersaing mencetak rekor tertinggi.
