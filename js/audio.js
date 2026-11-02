/**
 * Retro 8-bit Audio Synthesizer & Adaptive BGM Director
 * Using standard Web Audio API with zero external dependencies.
 * Also supports custom high-fidelity audio files (MP3/OGG) in assets/audio/ if provided.
 */

const NOTE_FREQS = {
  // Octave 2
  C2: 65.41, Cs2: 69.30, D2: 73.42, Ds2: 77.78, Eb2: 77.78, E2: 82.41, F2: 87.31, Fs2: 92.50, G2: 98.00, Ab2: 103.83, A2: 110.00, Bb2: 116.54, B2: 123.47,
  // Octave 3
  C3: 130.81, Cs3: 138.59, D3: 146.83, Ds3: 155.56, Eb3: 155.56, E3: 164.81, F3: 174.61, Fs3: 185.00, G3: 196.00, Ab3: 207.65, A3: 220.00, Bb3: 233.08, B3: 246.94,
  // Octave 4
  C4: 261.63, Cs4: 277.18, D4: 293.66, Ds4: 311.13, Eb4: 311.13, E4: 329.63, F4: 349.23, Fs4: 369.99, G4: 392.00, Ab4: 415.30, A4: 440.00, Bb4: 466.16, B4: 493.88,
  // Octave 5
  C5: 523.25, Cs5: 554.37, D5: 587.33, Ds5: 622.25, Eb5: 622.25, E5: 659.25, F5: 698.46, Fs5: 739.99, G5: 783.99, Ab5: 830.61, A5: 880.00, Bb5: 932.33, B5: 987.77,
  // Octave 6
  C6: 1046.50, Cs6: 1108.73, D6: 1174.66, Ds6: 1244.51, Eb6: 1244.51, E6: 1318.51, F6: 1396.91, Fs6: 1479.98, G6: 1567.98
};

// 3 Dynamic Adaptive BGM Compositions (64 16th-note steps = 4 bars per track)
const BGM_TRACKS = {
  // Track 1: Normal Exploration Stage (Cosmic Retro Arcade Groove, 128 BPM, A Minor)
  stage: {
    tempo: 128,
    bass: [
      'A2','A2','A2','A2', 'A2','A2','C3','E3',  'A2','A2','A2','A2', 'A2','A2','C3','E3',
      'F2','F2','F2','F2', 'F2','F2','A2','C3',  'F2','F2','F2','F2', 'F2','F2','A2','C3',
      'C3','C3','C3','C3', 'C3','C3','E3','G3',  'C3','C3','C3','C3', 'C3','C3','E3','G3',
      'G2','G2','G2','G2', 'G2','G2','B2','D3',  'E2','E2','E2','E2', 'E2','E2','G2','B2'
    ],
    lead: [
      'A4',null,'C5',null, 'E5',null,'A5','G5',  null,'E5',null,'D5', 'E5',null,'G5',null,
      'F5',null,'E5',null, 'D5',null,'C5','B4',  null,'C5',null,'D5', 'E5',null,null,null,
      'G5',null,'E5',null, 'C5',null,'D5','E5',  null,'G5',null,'A5', 'B5',null,'C6',null,
      'B5',null,'A5',null, 'G5',null,'E5','D5',  null,'C5',null,'B4', 'A4',null,null,null
    ],
    drums: [
      'kh',null,'h',null,  'sh',null,'h',null,   'kh',null,'h',null,  'sh',null,'h','h',
      'kh',null,'h',null,  'sh',null,'h',null,   'kh',null,'h',null,  'sh',null,'h','o',
      'kh',null,'h',null,  'sh',null,'h',null,   'kh',null,'h',null,  'sh',null,'h','h',
      'kh',null,'h',null,  'sh',null,'h',null,   'kh',null,'h','k',   'sh','s','s','s'
    ]
  },

  // Track 2: Mini-Boss Encounter: Void Destroyer (Fast, Tense & Driving, 144 BPM, D Phrygian)
  miniboss: {
    tempo: 144,
    bass: [
      'D2','D2','D2','Eb2', 'D2','D2','F2','D2',  'D2','D2','D2','Eb2', 'D2','D2','G2','D2',
      'Eb2','Eb2','Eb2','D2', 'Eb2','Eb2','G2','Eb2', 'Eb2','Eb2','Eb2','D2', 'Eb2','Eb2','A2','Eb2',
      'D2','D2','D2','Eb2', 'D2','D2','F2','D2',  'D2','D2','D2','Eb2', 'D2','D2','Bb2','D2',
      'F2','F2','F2','G2', 'A2','A2','G2','F2',  'G2','G2','G2','A2', 'Bb2','Bb2','C3','Cs3'
    ],
    lead: [
      'D5',null,'F5',null, 'A5',null,'D6','C6',  null,'Bb5',null,'A5', 'G5',null,'A5',null,
      'Bb5',null,'A5',null, 'G5',null,'F5','Eb5', null,'F5',null,'G5', 'A5',null,'Bb5',null,
      'A5',null,'D6',null, 'C6',null,'Bb5','A5', null,'G5',null,'F5', 'E5',null,'F5',null,
      'D5',null,'F5',null, 'A5',null,'Bb5','C6', null,'D6',null,'E6', 'F6',null,'E6','Cs6'
    ],
    drums: [
      'kh','h','h','h',   'sh','h','h','h',    'kh','h','h','k',   'sh','h','k','h',
      'kh','h','h','h',   'sh','h','h','h',    'kh','k','h','k',   'sh','s','h','o',
      'kh','h','h','h',   'sh','h','h','h',    'kh','h','h','k',   'sh','h','k','h',
      'kh','k','sh','k',  'kh','k','sh','k',   'kh','s','kh','s',  's','s','s','s'
    ]
  },

  // Track 3: Final Boss Encounter: Titan Apex Starfall (Epic, Melodic Danmaku Battle, 156 BPM, E Minor)
  boss: {
    tempo: 156,
    bass: [
      'E2','E2','G2','E2', 'B2','E2','G2','E2',  'E2','E2','G2','E2', 'D3','E2','B2','E2',
      'C3','C3','E3','C3', 'G2','C3','E3','C3',  'C3','C3','E3','C3', 'B2','C3','G2','C3',
      'A2','A2','C3','A2', 'E2','A2','C3','A2',  'A2','A2','C3','A2', 'G2','A2','E2','A2',
      'B2','B2','Ds3','B2', 'Fs2','B2','Ds3','B2', 'B2','B2','Ds3','B2', 'A2','B2','Ds3','Fs3'
    ],
    lead: [
      'E5',null,'G5',null, 'B5',null,'C6','B5',  null,'A5',null,'G5', 'Fs5',null,'G5','A5',
      'G5',null,'A5',null, 'B5',null,'C6','D6',  null,'C6',null,'B5', 'A5',null,'B5','C6',
      'C6',null,'B5',null, 'A5',null,'G5','Fs5', null,'G5',null,'A5', 'B5',null,'C6','D6',
      'B5',null,'Ds6',null, 'Fs6',null,'E6','Ds6', null,'B5',null,'A5', 'G5',null,'Fs5','Ds5'
    ],
    drums: [
      'kh','k','h','h',   'sh','h','h','k',    'kh','k','h','h',   'sh','h','k','h',
      'kh','k','h','h',   'sh','h','h','k',    'kh','k','h','h',   'sh','s','k','o',
      'kh','k','h','h',   'sh','h','h','k',    'kh','k','h','h',   'sh','h','k','h',
      'kh','k','kh','k',  'sh','k','kh','k',   'kh','s','kh','s',  's','s','s','s'
    ]
  }
};

class SoundFX {
  constructor() {
    this.ctx = null;
    this.isMuted = false;

    // Adaptive BGM System
    this.currentBgm = null; // 'stage' | 'miniboss' | 'boss' | null
    this.bgmGain = null;
    this.bgmVolume = 0.22;
    this.bgmStep = 0;
    this.nextNoteTime = 0;
    this.currentTempo = 128;
    this.schedulerTimer = null;

    // Custom Audio File Variations (Generated via Google Flow Music)
    this.customAudioSets = {
      setA: {
        id: 'setA',
        name: 'Pack 1: Cosmic Arcade • Cyber Threat • Danmaku Nova',
        stage: 'assets/audio/Cosmic Arcade (Take 1).mp3',
        miniboss: 'assets/audio/Cyber Threat (Take 1).mp3',
        boss: 'assets/audio/Danmaku Nova (Take 2).mp3'
      },
      setB: {
        id: 'setB',
        name: 'Pack 2: Starlight Circuit • Mega Overdrive • Galactic Showdown',
        stage: 'assets/audio/Starlight Circuit (Take 2).mp3',
        miniboss: 'assets/audio/Mega Overdrive (Take 2).mp3',
        boss: 'assets/audio/Galactic Showdown (Take 1).mp3'
      }
    };
    this.activeSetKey = 'setA';
    this.autoRotateSets = true;

    // Custom Audio File Fallback Support
    this.customAudio = {};
    this.activeCustomAudio = null;
  }

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioCtx();
      this.bgmGain = this.ctx.createGain();
      this.bgmGain.gain.setValueAtTime(this.isMuted ? 0 : this.bgmVolume, this.ctx.currentTime);
      this.bgmGain.connect(this.ctx.destination);

      this.probeCustomAudioFiles();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  // Probe if custom audio files exist in assets/audio/
  probeCustomAudioFiles() {
    const fileList = [
      'assets/audio/bgm_stage.mp3',
      'assets/audio/bgm_miniboss.mp3',
      'assets/audio/bgm_boss.mp3',
      'assets/audio/Cosmic Arcade (Take 1).mp3',
      'assets/audio/Starlight Circuit (Take 2).mp3',
      'assets/audio/Cyber Threat (Take 1).mp3',
      'assets/audio/Mega Overdrive (Take 2).mp3',
      'assets/audio/Danmaku Nova (Take 2).mp3',
      'assets/audio/Galactic Showdown (Take 1).mp3'
    ];

    fileList.forEach(src => {
      const audio = new Audio();
      audio.loop = true;
      audio.preload = 'metadata';
      audio.src = encodeURI(src);
      audio.addEventListener('canplaythrough', () => {
        this.customAudio[src] = audio;
      }, { once: true });
      audio.addEventListener('error', () => {
        delete this.customAudio[src];
      }, { once: true });
    });
  }

  getActiveCustomAudio(trackName) {
    if (this.activeSetKey === 'chiptune') return null;
    const currentSet = this.customAudioSets[this.activeSetKey] || this.customAudioSets.setA;
    const specificPath = currentSet[trackName];
    if (specificPath && this.customAudio[specificPath]) {
      return this.customAudio[specificPath];
    }
    const standardPath = `assets/audio/bgm_${trackName}.mp3`;
    if (this.customAudio[standardPath]) {
      return this.customAudio[standardPath];
    }
    return null;
  }

  rotateTrackIfEnabled() {
    if (!this.autoRotateSets) return;
    this.activeSetKey = (this.activeSetKey === 'setA') ? 'setB' : 'setA';
  }

  setBgmPack(packKey) {
    if (packKey === 'setA' || packKey === 'setB' || packKey === 'chiptune') {
      this.activeSetKey = packKey;
      this.autoRotateSets = false;
      if (this.currentBgm) {
        const trk = this.currentBgm;
        this.currentBgm = null;
        this.playBGM(trk);
      }
    }
  }

  toggleMute() {
    this.isMuted = !this.isMuted;
    if (this.bgmGain && this.ctx) {
      this.bgmGain.gain.setValueAtTime(this.isMuted ? 0 : this.bgmVolume, this.ctx.currentTime);
    }
    if (this.activeCustomAudio) {
      this.activeCustomAudio.muted = this.isMuted;
    }
    return this.isMuted;
  }

  // ==========================================================
  // ADAPTIVE BGM DIRECTOR
  // ==========================================================

  playBGM(trackName) {
    if (!BGM_TRACKS[trackName]) return;
    if (this.currentBgm === trackName) return; // already playing this track

    this.init();
    this.currentBgm = trackName;

    // Check if custom audio file is loaded for this track
    const customAudio = this.getActiveCustomAudio(trackName);
    if (customAudio) {
      this.stopProceduralBGM();
      this.playCustomAudioTrack(customAudio);
      return;
    }

    // Otherwise use procedural Web Audio synthesizer
    this.stopCustomAudioTrack();
    this.startProceduralBGM(trackName);
  }

  playCustomAudioTrack(audio) {
    if (!audio) return;
    const prevAudio = this.activeCustomAudio;

    if (prevAudio && prevAudio !== audio) {
      const fadeStep = 0.04;
      const fadeTimer = setInterval(() => {
        if (prevAudio.volume > fadeStep) {
          prevAudio.volume = Math.max(0, prevAudio.volume - fadeStep);
        } else {
          clearInterval(fadeTimer);
          prevAudio.pause();
          prevAudio.currentTime = 0;
        }
      }, 30);
    }

    audio.volume = this.isMuted ? 0 : this.bgmVolume;
    audio.muted = this.isMuted;
    audio.currentTime = 0;
    audio.play().catch(() => {});
    this.activeCustomAudio = audio;
  }

  stopCustomAudioTrack() {
    if (this.activeCustomAudio) {
      this.activeCustomAudio.pause();
      this.activeCustomAudio.currentTime = 0;
      this.activeCustomAudio = null;
    }
  }

  startProceduralBGM(trackName) {
    const track = BGM_TRACKS[trackName];
    if (!track) return;

    this.currentTempo = track.tempo;
    this.bgmStep = 0;
    this.nextNoteTime = this.ctx.currentTime + 0.05;

    if (!this.schedulerTimer) {
      this.schedulerTimer = setInterval(() => this.scheduleBGM(), 25);
    }
  }

  stopProceduralBGM() {
    if (this.schedulerTimer) {
      clearInterval(this.schedulerTimer);
      this.schedulerTimer = null;
    }
  }

  pauseBGM() {
    if (this.activeCustomAudio) {
      this.activeCustomAudio.pause();
    }
    this.stopProceduralBGM();
  }

  resumeBGM() {
    if (this.activeCustomAudio && this.currentBgm) {
      this.activeCustomAudio.play().catch(() => {});
    } else if (this.currentBgm) {
      this.startProceduralBGM(this.currentBgm);
    }
  }

  stopBGM() {
    this.currentBgm = null;
    this.stopCustomAudioTrack();
    this.stopProceduralBGM();
  }

  scheduleBGM() {
    if (!this.ctx || !this.currentBgm || this.isMuted) return;
    const lookahead = 0.12; // 120ms lookahead
    const track = BGM_TRACKS[this.currentBgm];
    if (!track) return;

    while (this.nextNoteTime < this.ctx.currentTime + lookahead) {
      this.playStep(track, this.bgmStep, this.nextNoteTime);
      const stepDuration = 60 / track.tempo / 4; // 16th note
      this.nextNoteTime += stepDuration;
      this.bgmStep = (this.bgmStep + 1) % 64;
    }
  }

  playStep(track, step, time) {
    const stepDuration = 60 / track.tempo / 4;

    // 1. Bassline
    const bassNote = track.bass[step];
    if (bassNote && NOTE_FREQS[bassNote]) {
      this.playSynthBass(NOTE_FREQS[bassNote], time, stepDuration * 0.9);
    }

    // 2. Lead Melody
    const leadNote = track.lead[step];
    if (leadNote && NOTE_FREQS[leadNote]) {
      this.playSynthLead(NOTE_FREQS[leadNote], time, stepDuration * 1.15);
    }

    // 3. Chiptune Percussion
    const drumHit = track.drums[step];
    if (drumHit) {
      if (drumHit.includes('k')) this.playSynthKick(time);
      if (drumHit.includes('s')) this.playSynthSnare(time);
      if (drumHit.includes('h')) this.playSynthHat(time, 0.03);
      if (drumHit.includes('o')) this.playSynthHat(time, 0.12);
    }
  }

  // Synthesizer Instruments
  playSynthBass(freq, time, dur) {
    if (!this.ctx || !this.bgmGain) return;
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const filter = this.ctx.createBiquadFilter();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(freq, time);

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(380, time);
      filter.frequency.exponentialRampToValueAtTime(140, time + dur);

      gain.gain.setValueAtTime(0.08, time);
      gain.gain.exponentialRampToValueAtTime(0.001, time + dur);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(this.bgmGain);

      osc.start(time);
      osc.stop(time + dur);
    } catch (_) {}
  }

  playSynthLead(freq, time, dur) {
    if (!this.ctx || !this.bgmGain) return;
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const filter = this.ctx.createBiquadFilter();

      osc.type = 'square';
      osc.frequency.setValueAtTime(freq, time);

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(2200, time);

      gain.gain.setValueAtTime(0.055, time);
      gain.gain.exponentialRampToValueAtTime(0.001, time + dur);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(this.bgmGain);

      osc.start(time);
      osc.stop(time + dur);
    } catch (_) {}
  }

  playSynthKick(time) {
    if (!this.ctx || !this.bgmGain) return;
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(130, time);
      osc.frequency.exponentialRampToValueAtTime(32, time + 0.08);

      gain.gain.setValueAtTime(0.12, time);
      gain.gain.exponentialRampToValueAtTime(0.001, time + 0.08);

      osc.connect(gain);
      gain.connect(this.bgmGain);

      osc.start(time);
      osc.stop(time + 0.08);
    } catch (_) {}
  }

  playSynthSnare(time) {
    if (!this.ctx || !this.bgmGain) return;
    try {
      // Noise component
      const bufferSize = Math.floor(this.ctx.sampleRate * 0.09);
      const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }
      const noise = this.ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = this.ctx.createBiquadFilter();
      filter.type = 'highpass';
      filter.frequency.setValueAtTime(1000, time);

      const gain = this.ctx.createGain();
      gain.gain.setValueAtTime(0.07, time);
      gain.gain.exponentialRampToValueAtTime(0.001, time + 0.09);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(this.bgmGain);
      noise.start(time);
    } catch (_) {}
  }

  playSynthHat(time, dur) {
    if (!this.ctx || !this.bgmGain) return;
    try {
      const bufferSize = Math.floor(this.ctx.sampleRate * dur);
      const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }
      const noise = this.ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = this.ctx.createBiquadFilter();
      filter.type = 'highpass';
      filter.frequency.setValueAtTime(7000, time);

      const gain = this.ctx.createGain();
      gain.gain.setValueAtTime(0.035, time);
      gain.gain.exponentialRampToValueAtTime(0.001, time + dur);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(this.bgmGain);
      noise.start(time);
    } catch (_) {}
  }

  // ==========================================================
  // RETRO SFX ONE-SHOTS
  // ==========================================================

  // Laser shot
  playShoot() {
    if (this.isMuted) return;
    this.init();
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'square';
      const now = this.ctx.currentTime;
      osc.frequency.setValueAtTime(880, now);
      osc.frequency.exponentialRampToValueAtTime(220, now + 0.08);

      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.08);
    } catch (_) {}
  }

  // Meteor impact hit
  playHit() {
    if (this.isMuted) return;
    this.init();
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(450, now);
      osc.frequency.exponentialRampToValueAtTime(90, now + 0.06);

      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.06);
    } catch (_) {}
  }

  // Boss heavy armor deflection / hit
  playBossHit() {
    if (this.isMuted) return;
    this.init();
    try {
      const now = this.ctx.currentTime;
      // Metallic dual-tone strike
      const osc1 = this.ctx.createOscillator();
      const osc2 = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc1.type = 'square';
      osc2.type = 'triangle';
      osc1.frequency.setValueAtTime(880, now);
      osc1.frequency.exponentialRampToValueAtTime(220, now + 0.08);
      osc2.frequency.setValueAtTime(1320, now);
      osc2.frequency.exponentialRampToValueAtTime(440, now + 0.08);

      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(this.ctx.destination);

      osc1.start(now);
      osc2.start(now);
      osc1.stop(now + 0.08);
      osc2.stop(now + 0.08);
    } catch (_) {}
  }

  // Meteor & enemy explosion (Visceral sub-bass drop + crunchy noise boom)
  playExplosion() {
    if (this.isMuted) return;
    this.init();
    try {
      const now = this.ctx.currentTime;

      // 1. White noise incendiary crackle
      const bufferSize = Math.floor(this.ctx.sampleRate * 0.35);
      const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.45));
      }

      const noise = this.ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = this.ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(1400, now);
      filter.frequency.exponentialRampToValueAtTime(60, now + 0.35);

      const nGain = this.ctx.createGain();
      nGain.gain.setValueAtTime(0.28, now);
      nGain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

      noise.connect(filter);
      filter.connect(nGain);
      nGain.connect(this.ctx.destination);

      // 2. Chest-thumping sub-bass drop (sine oscillator 160Hz -> 28Hz)
      const subOsc = this.ctx.createOscillator();
      const subGain = this.ctx.createGain();
      subOsc.type = 'sine';
      subOsc.frequency.setValueAtTime(160, now);
      subOsc.frequency.exponentialRampToValueAtTime(28, now + 0.32);

      subGain.gain.setValueAtTime(0.35, now);
      subGain.gain.exponentialRampToValueAtTime(0.001, now + 0.32);

      subOsc.connect(subGain);
      subGain.connect(this.ctx.destination);

      noise.start(now);
      subOsc.start(now);
      subOsc.stop(now + 0.32);
    } catch (_) {}
  }

  // Power-up collected (rising arpeggio)
  playPowerup() {
    if (this.isMuted) return;
    this.init();
    try {
      const notes = [440, 554, 659, 880]; // A4, C#5, E5, A5
      const now = this.ctx.currentTime;

      notes.forEach((freq, i) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + i * 0.05);

        gain.gain.setValueAtTime(0.1, now + i * 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, now + (i + 1) * 0.05);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now + i * 0.05);
        osc.stop(now + (i + 1) * 0.05);
      });
    } catch (_) {}
  }

  // Stellar Blaster (Ultimate Laser)
  playUltimate() {
    if (this.isMuted) return;
    this.init();
    try {
      const now = this.ctx.currentTime;

      // Deep rumble oscillator
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(180, now);
      osc.frequency.linearRampToValueAtTime(60, now + 0.8);

      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.8);

      // Noise layer for laser roar
      const bufferSize = this.ctx.sampleRate * 0.7;
      const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }
      const noise = this.ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = this.ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(1200, now);
      filter.frequency.exponentialRampToValueAtTime(200, now + 0.7);

      const nGain = this.ctx.createGain();
      nGain.gain.setValueAtTime(0.18, now);
      nGain.gain.exponentialRampToValueAtTime(0.001, now + 0.7);

      noise.connect(filter);
      filter.connect(nGain);
      nGain.connect(this.ctx.destination);
      noise.start(now);
    } catch (_) {}
  }

  // Player hurt (Visceral hull breach crunch + danger alert tone)
  playHurt() {
    if (this.isMuted) return;
    this.init();
    try {
      const now = this.ctx.currentTime;

      // 1. Dissonant dual-sawtooth hull crunch
      const osc1 = this.ctx.createOscillator();
      const osc2 = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc1.type = 'sawtooth';
      osc2.type = 'sawtooth';
      osc1.frequency.setValueAtTime(220, now);
      osc1.frequency.exponentialRampToValueAtTime(55, now + 0.28);
      osc2.frequency.setValueAtTime(155.56, now); // Eb3 (dissonant tritone)
      osc2.frequency.exponentialRampToValueAtTime(45, now + 0.28);

      gain.gain.setValueAtTime(0.32, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);

      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(this.ctx.destination);

      // 2. High-frequency digital alarm beep
      const beepOsc = this.ctx.createOscillator();
      const beepGain = this.ctx.createGain();
      beepOsc.type = 'square';
      beepOsc.frequency.setValueAtTime(880, now);
      beepOsc.frequency.setValueAtTime(440, now + 0.08);

      beepGain.gain.setValueAtTime(0.18, now);
      beepGain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);

      beepOsc.connect(beepGain);
      beepGain.connect(this.ctx.destination);

      osc1.start(now);
      osc2.start(now);
      beepOsc.start(now);
      osc1.stop(now + 0.28);
      osc2.stop(now + 0.28);
      beepOsc.stop(now + 0.2);
    } catch (_) {}
  }

  // Game over sound
  playGameOver() {
    if (this.isMuted) return;
    this.init();
    try {
      const notes = [330, 293, 261, 196]; // E4, D4, C4, G3
      const now = this.ctx.currentTime;

      notes.forEach((freq, i) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, now + i * 0.12);

        gain.gain.setValueAtTime(0.15, now + i * 0.12);
        gain.gain.exponentialRampToValueAtTime(0.001, now + (i + 1) * 0.14);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now + i * 0.12);
        osc.stop(now + (i + 1) * 0.14);
      });
    } catch (_) {}
  }

  // Boss Klaxon Warning Alarm
  playBossWarning() {
    if (this.isMuted) return;
    this.init();
    try {
      const now = this.ctx.currentTime;
      [0, 0.28, 0.56].forEach(delay => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(560, now + delay);
        osc.frequency.exponentialRampToValueAtTime(320, now + delay + 0.2);

        gain.gain.setValueAtTime(0.2, now + delay);
        gain.gain.exponentialRampToValueAtTime(0.001, now + delay + 0.24);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now + delay);
        osc.stop(now + delay + 0.24);
      });
    } catch (_) {}
  }

  // Boss plasma bullet
  playBossShoot() {
    if (this.isMuted) return;
    this.init();
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const now = this.ctx.currentTime;

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(360, now);
      osc.frequency.exponentialRampToValueAtTime(90, now + 0.12);

      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.12);
    } catch (_) {}
  }

  // Boss defeat massive explosion cascade
  playBossExplosion() {
    if (this.isMuted) return;
    this.init();
    try {
      const now = this.ctx.currentTime;

      // 3-stage staggered thunderous detonation
      [0, 0.18, 0.38].forEach((delay, idx) => {
        const subOsc = this.ctx.createOscillator();
        const subGain = this.ctx.createGain();
        subOsc.type = 'sine';
        subOsc.frequency.setValueAtTime(180 - idx * 30, now + delay);
        subOsc.frequency.exponentialRampToValueAtTime(22, now + delay + 0.6);

        subGain.gain.setValueAtTime(0.4 - idx * 0.05, now + delay);
        subGain.gain.exponentialRampToValueAtTime(0.001, now + delay + 0.6);

        subOsc.connect(subGain);
        subGain.connect(this.ctx.destination);

        subOsc.start(now + delay);
        subOsc.stop(now + delay + 0.6);
      });

      // Rushing shockwave noise wash
      const bufferSize = Math.floor(this.ctx.sampleRate * 1.2);
      const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.5));
      }
      const noise = this.ctx.createBufferSource();
      noise.buffer = buffer;
      const filter = this.ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(2000, now);
      filter.frequency.exponentialRampToValueAtTime(80, now + 1.2);

      const nGain = this.ctx.createGain();
      nGain.gain.setValueAtTime(0.35, now);
      nGain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);

      noise.connect(filter);
      filter.connect(nGain);
      nGain.connect(this.ctx.destination);
      noise.start(now);
    } catch (_) {}
  }

  // Cosmic Shield Deflection Barrier Sound (High-tech crystal harmonic ring)
  playShieldDeflect() {
    if (this.isMuted) return;
    this.init();
    try {
      const now = this.ctx.currentTime;
      // Resonant harmonic chime
      const osc1 = this.ctx.createOscillator();
      const osc2 = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc1.type = 'sine';
      osc1.frequency.setValueAtTime(1174.66, now); // D6
      osc1.frequency.exponentialRampToValueAtTime(1760.0, now + 0.08); // A6
      osc1.frequency.exponentialRampToValueAtTime(587.33, now + 0.35); // D5

      osc2.type = 'triangle';
      osc2.frequency.setValueAtTime(880.0, now);
      osc2.frequency.exponentialRampToValueAtTime(1318.51, now + 0.1);

      gain.gain.setValueAtTime(0.28, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(this.ctx.destination);

      osc1.start(now);
      osc2.start(now);
      osc1.stop(now + 0.35);
      osc2.stop(now + 0.35);
    } catch (_) {}
  }

  // Cosmic Shield Forcefield Activate
  playShieldPickup() {
    if (this.isMuted) return;
    this.init();
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(440, now);
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.15);
      osc.frequency.exponentialRampToValueAtTime(1320, now + 0.3);

      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + 0.3);
    } catch (_) {}
  }
}

window.soundFx = new SoundFX();

// Auto-unlock AudioContext on first user interaction (bypasses browser autoplay policy)
const unlockAudioOnGesture = () => {
  if (window.soundFx) {
    window.soundFx.init();
  }
};
['pointerdown', 'keydown', 'touchstart'].forEach(evt => {
  window.addEventListener(evt, unlockAudioOnGesture, { once: true, passive: true });
});
