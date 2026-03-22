/**
 * Hypnotic Consciousness Background
 * Infinity spirals, sacred geometry, pulsing neural networks
 * Once you start reading, you cannot look away.
 */

(function () {
    'use strict';

    const canvas = document.getElementById('consciousness-bg');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height, centerX, centerY;
    let time = 0;
    let animId;

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        centerX = width / 2;
        centerY = height / 2;
    }

    // ── Sacred Geometry: Concentric Infinity Rings ──
    function drawInfinityRings() {
        const ringCount = 12;
        const maxRadius = Math.min(width, height) * 0.45;

        for (let i = 0; i < ringCount; i++) {
            const progress = i / ringCount;
            const radius = maxRadius * (0.15 + progress * 0.85);
            const breathe = Math.sin(time * 0.3 + i * 0.5) * 0.08 + 1;
            const r = radius * breathe;

            // Rotation per ring — creates hypnotic spiral
            const rotation = time * 0.1 * (i % 2 === 0 ? 1 : -1) + i * 0.26;

            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(rotation);

            // Ring glow
            const alpha = 0.03 + Math.sin(time * 0.4 + i * 0.7) * 0.02;
            const hue = (time * 10 + i * 30) % 360;
            ctx.strokeStyle = `hsla(${hue}, 60%, 65%, ${alpha})`;
            ctx.lineWidth = 1 + Math.sin(time * 0.5 + i) * 0.5;

            // Draw elliptical ring (infinity-like)
            ctx.beginPath();
            ctx.ellipse(0, 0, r, r * 0.6, 0, 0, Math.PI * 2);
            ctx.stroke();

            // Second perpendicular ellipse — creates the flower of life look
            ctx.beginPath();
            ctx.ellipse(0, 0, r * 0.6, r, 0, 0, Math.PI * 2);
            ctx.stroke();

            ctx.restore();
        }
    }

    // ── Neural Consciousness Particles ──
    const PARTICLE_COUNT = 80;
    let particles = [];

    function createParticles() {
        particles = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            const angle = Math.random() * Math.PI * 2;
            const dist = Math.random() * Math.min(width, height) * 0.4 + 50;
            particles.push({
                angle: angle,
                dist: dist,
                baseDist: dist,
                radius: Math.random() * 2 + 0.5,
                speed: (Math.random() - 0.5) * 0.003,
                orbitSpeed: (Math.random() * 0.002 + 0.001) * (Math.random() > 0.5 ? 1 : -1),
                hue: Math.random() * 60 + 240, // violet to cyan range
                pulseSpeed: Math.random() * 0.02 + 0.01,
                pulseOffset: Math.random() * Math.PI * 2,
            });
        }
    }

    function drawParticles() {
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];

            // Orbit
            p.angle += p.orbitSpeed;
            p.dist = p.baseDist + Math.sin(time * 0.3 + p.pulseOffset) * 30;

            const x = centerX + Math.cos(p.angle) * p.dist;
            const y = centerY + Math.sin(p.angle) * p.dist * 0.7; // slight vertical squash

            // Pulse alpha
            const alpha = 0.15 + Math.sin(time * p.pulseSpeed + p.pulseOffset) * 0.12;

            // Particle
            ctx.beginPath();
            ctx.arc(x, y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `hsla(${p.hue + time * 5}, 70%, 70%, ${alpha})`;
            ctx.fill();

            // Glow
            if (p.radius > 1.2) {
                ctx.beginPath();
                ctx.arc(x, y, p.radius * 4, 0, Math.PI * 2);
                ctx.fillStyle = `hsla(${p.hue + time * 5}, 70%, 70%, ${alpha * 0.15})`;
                ctx.fill();
            }

            // Connect nearby particles (neural web)
            for (let j = i + 1; j < particles.length; j++) {
                const q = particles[j];
                const qx = centerX + Math.cos(q.angle) * q.dist;
                const qy = centerY + Math.sin(q.angle) * q.dist * 0.7;
                const dx = x - qx;
                const dy = y - qy;
                const distSq = dx * dx + dy * dy;

                if (distSq < 12000) {
                    const lineAlpha = (1 - distSq / 12000) * 0.06;
                    ctx.beginPath();
                    ctx.moveTo(x, y);
                    ctx.lineTo(qx, qy);
                    ctx.strokeStyle = `hsla(${(p.hue + q.hue) / 2 + time * 3}, 50%, 60%, ${lineAlpha})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
    }

    // ── Central Eye / Third Eye Glow ──
    function drawThirdEye() {
        const breathe = Math.sin(time * 0.25) * 0.3 + 1;
        const radius = 40 * breathe;

        // Outer aura
        const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius * 4);
        gradient.addColorStop(0, `hsla(${45 + Math.sin(time * 0.2) * 15}, 80%, 60%, 0.04)`);
        gradient.addColorStop(0.5, `hsla(${270 + Math.sin(time * 0.15) * 20}, 60%, 50%, 0.02)`);
        gradient.addColorStop(1, 'hsla(0, 0%, 0%, 0)');
        ctx.fillStyle = gradient;
        ctx.fillRect(centerX - radius * 4, centerY - radius * 4, radius * 8, radius * 8);

        // Inner core
        const coreGrad = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
        const coreHue = (time * 15) % 360;
        coreGrad.addColorStop(0, `hsla(${coreHue}, 70%, 70%, 0.06)`);
        coreGrad.addColorStop(0.6, `hsla(${coreHue + 40}, 60%, 50%, 0.02)`);
        coreGrad.addColorStop(1, 'hsla(0, 0%, 0%, 0)');
        ctx.fillStyle = coreGrad;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        ctx.fill();
    }

    // ── Floating Sanskrit-like Symbols (subtle) ──
    const symbols = ['\u0950', '\u2622', '\u2300', '\u221E', '\u25CB', '\u2609', '\u2638'];
    let floatingSymbols = [];

    function createFloatingSymbols() {
        floatingSymbols = [];
        for (let i = 0; i < 8; i++) {
            floatingSymbols.push({
                x: Math.random() * width,
                y: Math.random() * height,
                symbol: symbols[Math.floor(Math.random() * symbols.length)],
                size: Math.random() * 18 + 14,
                alpha: 0,
                targetAlpha: Math.random() * 0.06 + 0.02,
                drift: (Math.random() - 0.5) * 0.2,
                driftX: (Math.random() - 0.5) * 0.15,
                fadeSpeed: Math.random() * 0.003 + 0.001,
                fadeDir: 1,
            });
        }
    }

    function drawFloatingSymbols() {
        ctx.font = '400 normal';
        for (const s of floatingSymbols) {
            s.alpha += s.fadeSpeed * s.fadeDir;
            if (s.alpha >= s.targetAlpha) s.fadeDir = -1;
            if (s.alpha <= 0) {
                s.fadeDir = 1;
                s.x = Math.random() * width;
                s.y = Math.random() * height;
                s.symbol = symbols[Math.floor(Math.random() * symbols.length)];
            }

            s.y += s.drift;
            s.x += s.driftX;

            if (s.alpha > 0) {
                ctx.font = `${s.size}px 'Space Grotesk', sans-serif`;
                ctx.fillStyle = `rgba(240, 192, 64, ${s.alpha})`;
                ctx.textAlign = 'center';
                ctx.fillText(s.symbol, s.x, s.y);
            }
        }
    }

    // ── Main Animation Loop ──
    function animate() {
        ctx.clearRect(0, 0, width, height);

        // Deep void base
        ctx.fillStyle = 'rgba(5, 5, 16, 0.08)';
        ctx.fillRect(0, 0, width, height);

        drawThirdEye();
        drawInfinityRings();
        drawParticles();
        drawFloatingSymbols();

        time += 0.016;
        animId = requestAnimationFrame(animate);
    }

    // Initialize
    resize();
    createParticles();
    createFloatingSymbols();
    animate();

    window.addEventListener('resize', function () {
        resize();
        createParticles();
        createFloatingSymbols();
    });

    document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
            cancelAnimationFrame(animId);
        } else {
            animate();
        }
    });


    // ── Scroll Progress Bar ──
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    progressBar.style.width = '0%';
    document.body.appendChild(progressBar);

    // ── Reading Focus Vignette ──
    const vignette = document.createElement('div');
    vignette.className = 'reading-vignette';
    document.body.appendChild(vignette);

    window.addEventListener('scroll', function () {
        // Progress bar
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        progressBar.style.width = progress + '%';

        // Activate vignette when reading (scrolled past hero)
        if (scrollTop > 400) {
            vignette.classList.add('active');
        } else {
            vignette.classList.remove('active');
        }
    });


    // ── Scroll Reveal for Prose Elements ──
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('prose-visible');
            }
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

    // Observe all prose children after a brief delay (let initial animations play)
    setTimeout(function () {
        document.querySelectorAll('.prose > *').forEach(function (el) {
            // Reset animation for scroll-based reveal
            el.style.animation = 'none';
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            observer.observe(el);
        });
    }, 500);

})();
