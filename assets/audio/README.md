# Starfall Breakout - Custom BGM Audio Folder

Folder ini disiapkan untuk file musik latar (BGM) jika Anda ingin menggunakan musik hasil rekaman sendiri, DAW (FL Studio, Ableton), atau AI generator (seperti **Google MusicFX / Google Flow**, **Suno**, **Udio**).

### Nama File yang Otomatis Dikenali:
Game akan **otomatis** memutar file MP3 ini secara dinamis dan seamless:
1. `bgm_stage.mp3` - Lagu petualangan luar angkasa biasa (Stage Theme).
2. `bgm_miniboss.mp3` - Lagu pertempuran mini-boss Void Destroyer (Tense Battle Theme).
3. `bgm_boss.mp3` - Lagu pertempuran big boss Titan Apex Starfall (Epic Final Boss Theme).

### Sistem Fallback Otomatis (Sudah Aktif!):
Jika folder ini tidak diisi file MP3, game **tidak akan hening**! Game langsung menjalankan **Web Audio Chiptune Synthesizer** native bawaan:
- **Stage**: Cosmic Retro Groove 128 BPM (A Minor).
- **Miniboss**: Fast & Driving 144 BPM (D Phrygian).
- **Boss**: Epic Danmaku Battle 156 BPM (E Minor).
Lagu akan otomatis berganti sendiri saat Miniboss atau Big Boss muncul, dan kembali ke lagu Stage saat boss dikalahkan.

---

### Contoh Prompt Siap Pakai untuk Google Flow / MusicFX / Suno:
Jika Anda ingin men-generate audio MP3 berkualitas studio, Anda bisa salin prompt ini:

#### 1. Untuk `bgm_stage.mp3` (Stage Theme)
> *"Upbeat retro 16-bit arcade synthwave, 128 BPM, funky slap bassline, cosmic arpeggio synth leads, driving electronic 4-on-the-floor drums, nostalgic 90s space shooter groove, Gradius and Outrun vibe, seamless loop, instrumental only, no vocals"*

#### 2. Untuk `bgm_miniboss.mp3` (Void Destroyer Miniboss)
> *"Fast aggressive darksynth cyber-industrial battle theme, 144 BPM, D Phrygian mode, distorted sawtooth bass, urgent high-tempo chiptune arpeggios, intense snare rolls, menacing alien menace tension, Mega Man X boss vibe, seamless loop, instrumental only"*

#### 3. Untuk `bgm_boss.mp3` (Titan Apex Starfall Big Boss)
> *"Epic high-energy symphonic metal and chiptune fusion, 156 BPM, Touhou danmaku boss style, lightning-fast electric guitar and hyper synth melodies, grand orchestral brass hits, furious double-kick drums, climactic galactic showdown, seamless loop, instrumental only"*

