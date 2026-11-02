import sys

with open('js/game.js', 'r', encoding='utf-8') as f:
    text = f.read()

target_block = '''    drawOrganicAppendages(ctx) {
      const halfW = this.width / 2;
      const halfH = this.height / 2;

      ctx.save();
      if (this.archetype === 'monster' || this.archetype === 'alien') {
        // Undulating Bioluminescent Tendrils / Tentacles
        const tendrilCount = this.archetype === 'alien' ? 5 : 4;
        const rootX = halfW * 0.65;
        const segmentCount = 6;
        const segLen = 14;

        ctx.lineWidth = 3.5;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        for (let t = 0; t < tendrilCount; t++) {
          const rootY = -halfH * 0.4 + (t / (tendrilCount - 1)) * (halfH * 0.8);
          const phaseOffset = t * 1.35;
          const tendrilGrad = ctx.createLinearGradient(rootX, rootY, rootX + 90, rootY);
          tendrilGrad.addColorStop(0, this.color || '#00f3ff');
          tendrilGrad.addColorStop(0.6, '#9d4edd');
          tendrilGrad.addColorStop(1, 'transparent');
          ctx.strokeStyle = tendrilGrad;

          ctx.beginPath();
          ctx.moveTo(rootX, rootY);
          let cx = rootX;
          let cy = rootY;
          for (let s = 1; s <= segmentCount; s++) {
            const wave = Math.sin(this.time * 5.2 + phaseOffset + s * 0.75) * (8 + s * 2.5);
            cx += segLen;
            cy += wave * 0.35;
            ctx.lineTo(cx, cy);
          }
          ctx.stroke();

          ctx.fillStyle = this.color || '#00f3ff';
          ctx.beginPath();
          ctx.arc(cx, cy, 2.5, 0, Math.PI * 2);
          ctx.fill();
        }
      } else if (this.archetype === 'humanoid') {
        // Flowing Neon Energy Halo & Wings
        const wingPulse = Math.sin(this.time * 4) * 8;
        ctx.strokeStyle = this.color || '#ff00aa';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.arc(halfW * 0.1, -halfH * 0.2, 28 + wingPulse, 0, Math.PI * 2);
        ctx.stroke();

        ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(halfW * 0.1, -halfH * 0.2, 14, 0, Math.PI * 2);
        ctx.stroke();
      } else {
        // Spaceship & Mecha: Roaring Plasma Exhaust Jets
        const thrusterCount = this.archetype === 'spaceship' ? 2 : 3;
        const rootX = halfW * 0.8;
        for (let i = 0; i < thrusterCount; i++) {
          const thrusterY = -halfH * 0.35 + i * (halfH * 0.7 / Math.max(1, thrusterCount - 1));
          const flameLen = 28 + Math.sin(this.time * 18 + i * 2) * 14 + Math.random() * 8;
          const flameGrad = ctx.createLinearGradient(rootX, thrusterY, rootX + flameLen, thrusterY);
          flameGrad.addColorStop(0, '#ffffff');
          flameGrad.addColorStop(0.3, this.color || '#00f3ff');
          flameGrad.addColorStop(0.7, '#ff0055');
          flameGrad.addColorStop(1, 'transparent');
          ctx.fillStyle = flameGrad;
          ctx.beginPath();
          ctx.moveTo(rootX, thrusterY - 6);
          ctx.lineTo(rootX + flameLen, thrusterY);
          ctx.lineTo(rootX, thrusterY + 6);
          ctx.closePath();
          ctx.fill();
        }
      }
      ctx.restore();
    }

    draw(ctx) {
      ctx.save();

      // Telegraphed Signature Skill Charging Animation
      if (this.isCastingSkill) {
        this.drawSkillTelegraph(ctx);
      }

      // Active Firing Beam (Lance of Longinus or Hyper Railgun)
      if (this.isFiringLaser) {
        if (this.archetype === 'humanoid') {
          drawValkyrieCelestialLanceBeam(ctx, this);
        } else {
          drawBossHyperRailgunBeam(ctx, this);
        }
      }

      // Draw Boss with dynamic tilt and natural breathing pulse
      ctx.translate(this.currentX || this.x, this.y);
      ctx.rotate(this.tilt || 0);

      const breathFreq = this.type === 'bigboss' ? 2.2 : 3.4;
      const breathMag = this.type === 'bigboss' ? 0.025 : 0.04;
      const pulseX = 1 + Math.sin(this.time * breathFreq) * breathMag;
      const pulseY = 1 - Math.sin(this.time * breathFreq) * (breathMag * 0.8);
      ctx.scale(pulseX, pulseY);

      this.drawOrganicAppendages(ctx);

      if (this.type === 'miniboss') {
        this.drawMinibossShip(ctx);
      } else {
        this.drawBigbossShip(ctx);
      }

      ctx.restore();
    }'''

replacement_block = '''    drawBackAppendages(ctx) {
      const halfW = this.width / 2;
      const halfH = this.height / 2;

      ctx.save();
      if (this.archetype === 'humanoid') {
        // --- 1. Celestial Valkyrie: 3-Layered Radiant Angelic Starlight Wings ---
        const wingFlap = Math.sin(this.time * 3.8);
        const wingSpread = 0.85 + wingFlap * 0.18;
        const wingCount = 3;

        for (let side = -1; side <= 1; side += 2) {
          for (let w = 0; w < wingCount; w++) {
            const wingAngle = (-0.45 + w * 0.35 + wingFlap * 0.12) * side;
            const wingLen = (halfW * 0.72 + w * 18) * wingSpread;
            const wingOriginX = halfW * 0.08;
            const wingOriginY = -halfH * 0.22 + side * (w * 10);

            ctx.save();
            ctx.translate(wingOriginX, wingOriginY);
            ctx.rotate(wingAngle);

            const wingGrad = ctx.createLinearGradient(0, 0, wingLen, 0);
            wingGrad.addColorStop(0, '#ffffff');
            wingGrad.addColorStop(0.3, this.color || '#ff00aa');
            wingGrad.addColorStop(0.7, '#9d4edd');
            wingGrad.addColorStop(1, 'transparent');

            ctx.fillStyle = wingGrad;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.quadraticCurveTo(wingLen * 0.5, -14 * side, wingLen, 0);
            ctx.quadraticCurveTo(wingLen * 0.6, 12 * side, 0, 0);
            ctx.fill();

            // Luminous Feather Spine
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1.4;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(wingLen * 0.85, 0);
            ctx.stroke();

            ctx.restore();
          }
        }

        // Sacred Revolving Halo Ring behind head
        const haloX = halfW * 0.08;
        const haloY = -halfH * 0.24;
        const haloR = 26 + Math.sin(this.time * 3) * 3;
        ctx.save();
        ctx.translate(haloX, haloY);
        ctx.rotate(this.time * 0.85);
        ctx.strokeStyle = '#ffd000';
        ctx.lineWidth = 2.2;
        ctx.shadowColor = '#ffd000';
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.arc(0, 0, haloR, 0, Math.PI * 2);
        ctx.stroke();
        // Halo Runes
        for (let r = 0; r < 6; r++) {
          const a = (r / 6) * Math.PI * 2;
          ctx.beginPath();
          ctx.moveTo(Math.cos(a) * (haloR - 4), Math.sin(a) * (haloR - 4));
          ctx.lineTo(Math.cos(a) * (haloR + 4), Math.sin(a) * (haloR + 4));
          ctx.stroke();
        }
        ctx.restore();

      } else if (this.archetype === 'mecha') {
        // --- 2. Mecha Titan: Heavy Supersonic Rocket Thrusters with Shock Diamonds ---
        const thrusterOrigins = [
          { x: halfW * 0.52, y: -halfH * 0.38 },
          { x: halfW * 0.55, y: halfH * 0.35 }
        ];

        thrusterOrigins.forEach((th, idx) => {
          const flameLen = 38 + Math.sin(this.time * 22 + idx * 2.5) * 16 + Math.random() * 8;
          const flameW = 12;

          const flameGrad = ctx.createLinearGradient(th.x, th.y, th.x + flameLen, th.y);
          flameGrad.addColorStop(0, '#ffffff');
          flameGrad.addColorStop(0.2, '#00f3ff');
          flameGrad.addColorStop(0.65, '#0066ff');
          flameGrad.addColorStop(1, 'transparent');

          ctx.fillStyle = flameGrad;
          ctx.beginPath();
          ctx.moveTo(th.x, th.y - flameW);
          ctx.lineTo(th.x + flameLen, th.y);
          ctx.lineTo(th.x, th.y + flameW);
          ctx.closePath();
          ctx.fill();

          // Shock Diamonds
          ctx.fillStyle = '#ffffff';
          for (let d = 1; d <= 3; d++) {
            const dx = th.x + d * (flameLen * 0.22);
            ctx.beginPath();
            ctx.arc(dx, th.y, 2.5, 0, Math.PI * 2);
            ctx.fill();
          }
        });

      } else if (this.archetype === 'monster' || this.archetype === 'alien') {
        // --- 3. Monster / Alien: Deep Background Undulating Bioluminescent Tentacles ---
        const tendrilCount = this.archetype === 'alien' ? 6 : 5;
        const rootX = halfW * 0.65;
        const segmentCount = 7;
        const segLen = 15;

        ctx.lineWidth = 3.5;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        for (let t = 0; t < tendrilCount; t++) {
          const rootY = -halfH * 0.45 + (t / (tendrilCount - 1)) * (halfH * 0.9);
          const phaseOffset = t * 1.35;
          const tendrilGrad = ctx.createLinearGradient(rootX, rootY, rootX + 110, rootY);
          tendrilGrad.addColorStop(0, this.color || '#00f3ff');
          tendrilGrad.addColorStop(0.6, '#9d4edd');
          tendrilGrad.addColorStop(1, 'transparent');
          ctx.strokeStyle = tendrilGrad;

          ctx.beginPath();
          ctx.moveTo(rootX, rootY);
          let cx = rootX;
          let cy = rootY;
          for (let s = 1; s <= segmentCount; s++) {
            const wave = Math.sin(this.time * 5.2 + phaseOffset + s * 0.72) * (9 + s * 2.8);
            cx += segLen;
            cy += wave * 0.35;
            ctx.lineTo(cx, cy);
          }
          ctx.stroke();

          ctx.fillStyle = this.color || '#00f3ff';
          ctx.beginPath();
          ctx.arc(cx, cy, 3.0, 0, Math.PI * 2);
          ctx.fill();
        }
      } else {
        // --- 4. Spaceship: High-Output Twin Plasma Thruster Jets ---
        const thrusterCount = 2;
        const rootX = halfW * 0.82;
        for (let i = 0; i < thrusterCount; i++) {
          const thrusterY = -halfH * 0.3 + i * (halfH * 0.6);
          const flameLen = 32 + Math.sin(this.time * 20 + i * 3) * 16 + Math.random() * 8;
          const flameGrad = ctx.createLinearGradient(rootX, thrusterY, rootX + flameLen, thrusterY);
          flameGrad.addColorStop(0, '#ffffff');
          flameGrad.addColorStop(0.3, this.color || '#00f3ff');
          flameGrad.addColorStop(0.7, '#ff0055');
          flameGrad.addColorStop(1, 'transparent');
          ctx.fillStyle = flameGrad;
          ctx.beginPath();
          ctx.moveTo(rootX, thrusterY - 7);
          ctx.lineTo(rootX + flameLen, thrusterY);
          ctx.lineTo(rootX, thrusterY + 7);
          ctx.closePath();
          ctx.fill();
        }
      }
      ctx.restore();
    }

    drawFrontAppendages(ctx) {
      const halfW = this.width / 2;
      const halfH = this.height / 2;

      ctx.save();
      if (this.archetype === 'humanoid') {
        // =========================================================================
        // VALKYRIE: ANIMASI PUTAR TONGKAT / CELESTIAL LANCE SPIN & HAND ARTICULATION
        // =========================================================================
        const handBaseX = -halfW * 0.28;
        const handBaseY = halfH * 0.05;
        // Natural arm/hand floating breathing sway
        const handSwayX = Math.cos(this.time * 3.2) * 5;
        const handSwayY = Math.sin(this.time * 3.2) * 5;
        const hx = handBaseX + handSwayX;
        const hy = handBaseY + handSwayY;

        ctx.save();
        ctx.translate(hx, hy);

        // Staff Spin Speed & Angle:
        // Idle: elegant continuous spin (3.8 rad/s)
        // Charging Skill / Laser: Blazing kinetic propeller whirl (26 rad/s)
        // Firing Beam: Locked horizontal thrusting forward
        let spinAngle = (this.time * 3.8);
        const isCharging = (this.isCastingSkill || this.isChargingLaser);
        const isFiring = this.isFiringLaser;

        if (isCharging) {
          spinAngle = this.time * 26.0;
        } else if (isFiring) {
          spinAngle = Math.PI; // Locked aiming forward
        }

        ctx.rotate(spinAngle);

        const staffLen = 110;
        const halfStaff = staffLen / 2;

        // 1. Kinetic Motion Blur Disc / Energy Trail during fast twirl
        if (isCharging) {
          const vortexGrad = ctx.createRadialGradient(0, 0, 10, 0, 0, halfStaff + 12);
          vortexGrad.addColorStop(0, 'rgba(255, 255, 255, 0.4)');
          vortexGrad.addColorStop(0.45, `${this.color || '#ff00aa'}44`);
          vortexGrad.addColorStop(0.85, 'rgba(255, 220, 100, 0.55)');
          vortexGrad.addColorStop(1, 'transparent');
          ctx.fillStyle = vortexGrad;
          ctx.beginPath();
          ctx.arc(0, 0, halfStaff + 10, 0, Math.PI * 2);
          ctx.fill();

          // High-speed whirling speed arcs
          ctx.strokeStyle = '#ffd000';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.arc(0, 0, halfStaff + 2, 0, Math.PI * 0.85);
          ctx.stroke();
          ctx.beginPath();
          ctx.arc(0, 0, halfStaff + 2, Math.PI, Math.PI * 1.85);
          ctx.stroke();
        }

        // 2. Staff Shaft (Gold & Crystalline Core)
        const shaftGrad = ctx.createLinearGradient(-halfStaff, 0, halfStaff, 0);
        shaftGrad.addColorStop(0, '#ffd000');
        shaftGrad.addColorStop(0.5, '#ffffff');
        shaftGrad.addColorStop(1, '#ffd000');
        ctx.strokeStyle = shaftGrad;
        ctx.lineWidth = 3.5;
        ctx.beginPath();
        ctx.moveTo(-halfStaff, 0);
        ctx.lineTo(halfStaff, 0);
        ctx.stroke();

        // 3. Ornate Double-Ended Celestial Spear Tips
        [-1, 1].forEach(dir => {
          const tipX = dir * halfStaff;
          ctx.save();
          ctx.translate(tipX, 0);
          ctx.rotate(dir === 1 ? 0 : Math.PI);

          // Diamond Spear Head
          ctx.fillStyle = '#ffffff';
          ctx.shadowColor = this.color || '#ff00aa';
          ctx.shadowBlur = 10;
          ctx.beginPath();
          ctx.moveTo(0, 0);
          ctx.lineTo(-14, -6);
          ctx.lineTo(16, 0);
          ctx.lineTo(-14, 6);
          ctx.closePath();
          ctx.fill();

          // Mini Angelic Winglets on Spearhead
          ctx.strokeStyle = '#ffd000';
          ctx.lineWidth = 1.8;
          ctx.beginPath();
          ctx.moveTo(-8, -5);
          ctx.lineTo(-16, -11);
          ctx.lineTo(-12, -2);
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(-8, 5);
          ctx.lineTo(-16, 11);
          ctx.lineTo(-12, 2);
          ctx.stroke();

          // Blazing Starlight Flare at Tip
          ctx.fillStyle = '#ffd000';
          ctx.beginPath();
          ctx.arc(16, 0, 3.5, 0, Math.PI * 2);
          ctx.fill();

          ctx.restore();
        });

        // 4. Center Celestial Gripping Jewel & Hand Rune
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = '#00f3ff';
        ctx.shadowBlur = 14;
        ctx.beginPath();
        ctx.arc(0, 0, 5, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();

        // Floating Rune Circle in Hand Palm
        ctx.save();
        ctx.translate(hx, hy);
        ctx.rotate(-this.time * 2.0);
        ctx.strokeStyle = `${this.color || '#ff00aa'}aa`;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.arc(0, 0, 18, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();

      } else if (this.archetype === 'mecha') {
        // =========================================================================
        // MECHA TITAN: AIMING HEAVY RAILGUN CANNON ARM & RECOIL PISTON SYSTEM
        // =========================================================================
        const shoulderX = -halfW * 0.18;
        const shoulderY = -halfH * 0.05;

        // Dynamic Aim Tracking toward Player Ship!
        const targetY = player ? player.y : (CANVAS_HEIGHT / 2);
        const targetX = player ? player.x : 80;
        const rawAim = Math.atan2(targetY - (this.y + shoulderY), targetX - ((this.currentX || this.x) + shoulderX));
        // Clamp elevation between -22 deg and +22 deg
        const aimAngle = Math.max(-0.38, Math.min(0.38, rawAim + Math.PI)); // Relative to facing left

        // Hydraulic Recoil displacement when firing
        const isRecoil = (this.shootTimer < 0.22) || this.isFiringLaser;
        const recoilDist = isRecoil ? Math.sin(this.time * 30) * 8 : 0;

        ctx.save();
        ctx.translate(shoulderX, shoulderY);
        ctx.rotate(-aimAngle); // Aim towards player

        // 1. Arm Hydraulic Upper Bracket & Piston
        ctx.fillStyle = '#1e2433';
        ctx.strokeStyle = '#4a5568';
        ctx.lineWidth = 2.0;
        ctx.fillRect(-10, -8, 22, 16);
        ctx.strokeRect(-10, -8, 22, 16);

        // Chrome Hydraulic Piston Shaft
        ctx.fillStyle = '#e2e8f0';
        ctx.fillRect(-22 + recoilDist, -4, 14, 8);

        // 2. Forearm Dual Heavy Railgun Barrels (Sliding on Recoil)
        const barrelX = -36 + recoilDist;
        ctx.fillStyle = '#2d3748';
        ctx.strokeStyle = '#ffd000';
        ctx.lineWidth = 1.5;
        // Upper Barrel
        ctx.fillRect(barrelX, -10, 32, 6);
        ctx.strokeRect(barrelX, -10, 32, 6);
        // Lower Barrel
        ctx.fillRect(barrelX, 4, 32, 6);
        ctx.strokeRect(barrelX, 4, 32, 6);

        // Glowing Rail Accelerator Coils
        ctx.fillStyle = this.color || '#00f3ff';
        for (let c = 0; c < 3; c++) {
          const cx = barrelX + 6 + c * 8;
          ctx.fillRect(cx, -11, 3, 8);
          ctx.fillRect(cx, 3, 3, 8);
        }

        // Muzzle Heat Glow / Smoke
        if (isRecoil) {
          ctx.fillStyle = '#ff7700';
          ctx.shadowColor = '#ff2200';
          ctx.shadowBlur = 12;
          ctx.beginPath();
          ctx.arc(barrelX - 3, -7, 5, 0, Math.PI * 2);
          ctx.arc(barrelX - 3, 7, 5, 0, Math.PI * 2);
          ctx.fill();
        }

        ctx.restore();

        // 3. Center Chest Overdrive Arc Reactor (Turbine Core & Lightning Arcs)
        const coreX = -halfW * 0.02;
        const coreY = halfH * 0.04;
        const coreR = 18;

        ctx.save();
        ctx.translate(coreX, coreY);

        // Radiant Core Plasma Aura
        const coreAura = ctx.createRadialGradient(0, 0, 4, 0, 0, coreR * 1.8);
        coreAura.addColorStop(0, '#ffffff');
        coreAura.addColorStop(0.35, this.color || '#00f3ff');
        coreAura.addColorStop(0.8, 'rgba(0, 100, 255, 0.25)');
        coreAura.addColorStop(1, 'transparent');
        ctx.fillStyle = coreAura;
        ctx.beginPath();
        ctx.arc(0, 0, coreR * 1.8, 0, Math.PI * 2);
        ctx.fill();

        // Rotating Turbine Aperture Blades
        ctx.rotate(this.time * 5.5);
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2.0;
        for (let b = 0; b < 6; b++) {
          const a = (b / 6) * Math.PI * 2;
          ctx.beginPath();
          ctx.moveTo(Math.cos(a) * 3, Math.sin(a) * 3);
          ctx.lineTo(Math.cos(a + 0.3) * (coreR - 3), Math.sin(a + 0.3) * (coreR - 3));
          ctx.stroke();
        }

        // Outer Titanium Armored Core Ring
        ctx.strokeStyle = '#ffd000';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.arc(0, 0, coreR, 0, Math.PI * 2);
        ctx.stroke();

        ctx.restore();

        // Crackling Electrical Lightning Filament to Shoulders
        if (Math.random() < 0.45) {
          ctx.strokeStyle = '#00f3ff';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(coreX, coreY);
          const midX = (coreX + shoulderX) * 0.5 + (Math.random() - 0.5) * 8;
          const midY = (coreY + shoulderY) * 0.5 + (Math.random() - 0.5) * 8;
          ctx.lineTo(midX, midY);
          ctx.lineTo(shoulderX, shoulderY);
          ctx.stroke();
        }

      } else if (this.archetype === 'alien') {
        // =========================================================================
        // ALIEN ELDRITCH EYE: LIVING TRACKING PUPIL & SMOOTH EYELID BLINK
        // =========================================================================
        const eyeX = -halfW * 0.12;
        const eyeY = -halfH * 0.04;
        const eyeR = 22;

        // Player tracking angle
        const targetY = player ? player.y : (CANVAS_HEIGHT / 2);
        const targetX = player ? player.x : 80;
        const pAngle = Math.atan2(targetY - (this.y + eyeY), targetX - ((this.currentX || this.x) + eyeX));
        const pupilDist = 6.0;

        // Eyelid Blinking every 4.0 seconds for 0.25s
        const blinkCycle = (this.time % 4.0);
        const isBlinking = blinkCycle > 3.75;
        const blinkAmount = isBlinking ? Math.sin((blinkCycle - 3.75) / 0.25 * Math.PI) : 0;

        ctx.save();
        ctx.translate(eyeX, eyeY);

        // Clip eye area
        ctx.beginPath();
        ctx.ellipse(0, 0, eyeR, eyeR * (1 - blinkAmount * 0.95), 0, 0, Math.PI * 2);
        ctx.clip();

        // Sclera with pulsing void veins
        const eyeGrad = ctx.createRadialGradient(0, 0, 2, 0, 0, eyeR);
        eyeGrad.addColorStop(0, '#ffffff');
        eyeGrad.addColorStop(0.5, '#ffd000');
        eyeGrad.addColorStop(0.85, '#ff0055');
        eyeGrad.addColorStop(1, '#140024');
        ctx.fillStyle = eyeGrad;
        ctx.fillRect(-eyeR - 2, -eyeR - 2, (eyeR + 2) * 2, (eyeR + 2) * 2);

        // Tracking Cyclopean Pupil (Slit / Eldritch Diamond)
        const relPupilX = Math.cos(pAngle) * pupilDist;
        const relPupilY = Math.sin(pAngle) * (pupilDist * 0.65);
        ctx.fillStyle = '#05000a';
        ctx.shadowColor = '#00f3ff';
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.ellipse(relPupilX, relPupilY, 3.5, 9, 0, 0, Math.PI * 2);
        ctx.fill();

        // Eye Cornea Light Reflection Spark
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(relPupilX - 2.5, relPupilY - 3, 2.0, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();

        // Eyelid Outlines & Creases
        ctx.strokeStyle = '#2b0938';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.ellipse(eyeX, eyeY, eyeR + 1, (eyeR + 1) * (1 - blinkAmount * 0.95), 0, 0, Math.PI * 2);
        ctx.stroke();

      } else if (this.archetype === 'spaceship') {
        // --- 4. Spaceship: Shield Matrix Shimmer & Bow Armor Shimmer ---
        const shieldPulse = Math.sin(this.time * 4) * 0.2 + 0.35;
        ctx.strokeStyle = `rgba(0, 243, 255, ${shieldPulse})`;
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.arc(-halfW * 0.35, 0, halfH * 0.85, Math.PI * 0.55, Math.PI * 1.45);
        ctx.stroke();
      }
      ctx.restore();
    }

    draw(ctx) {
      ctx.save();

      // Telegraphed Signature Skill Charging Animation
      if (this.isCastingSkill) {
        this.drawSkillTelegraph(ctx);
      }

      // Active Firing Beam (Lance of Longinus or Hyper Railgun)
      if (this.isFiringLaser) {
        if (this.archetype === 'humanoid') {
          drawValkyrieCelestialLanceBeam(ctx, this);
        } else {
          drawBossHyperRailgunBeam(ctx, this);
        }
      }

      // Draw Boss with dynamic tilt and natural breathing pulse
      ctx.translate(this.currentX || this.x, this.y);
      ctx.rotate(this.tilt || 0);

      const breathFreq = this.type === 'bigboss' ? 2.2 : 3.4;
      const breathMag = this.type === 'bigboss' ? 0.025 : 0.04;
      const pulseX = 1 + Math.sin(this.time * breathFreq) * breathMag;
      const pulseY = 1 - Math.sin(this.time * breathFreq) * (breathMag * 0.8);
      ctx.scale(pulseX, pulseY);

      // Back Layer: Flapping wings, halo, vector thruster plumes, rear tentacles
      this.drawBackAppendages(ctx);

      // Middle Layer: Boss sprite with dynamic hue-rotation & 22-slice undulation
      if (this.type === 'miniboss') {
        this.drawMinibossShip(ctx);
      } else {
        this.drawBigbossShip(ctx);
      }

      // Front Layer: Valkyrie spinning lance/staff, Mecha aiming & recoiling cannon arm, Alien pupil & eyelids
      this.drawFrontAppendages(ctx);

      ctx.restore();
    }'''

assert target_block in text, 'target_block not found!'
text = text.replace(target_block, replacement_block, 1)

with open('js/game.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully applied natural boss animations!')
