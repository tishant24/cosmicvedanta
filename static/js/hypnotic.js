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


    // Content is always visible — no scroll-based hiding

})();


/* ============================================================
   INTERACTIVE READING FEATURES
   Page-Turn Mode, Keyword Animations, Text Effects
   ============================================================ */

(function () {
    'use strict';

    const prose = document.querySelector('.post-body.prose');
    if (!prose) return;

    // ── 1. PAGE-TURN / SWIPE READING MODE ──

    let pageMode = false;
    let currentPage = 0;
    let pages = [];
    let slideWrapper = null;
    let touchStartX = 0;
    let touchStartY = 0;
    let touchDeltaX = 0;
    let isSwiping = false;

    // Create toggle button
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'reading-mode-toggle';
    toggleBtn.innerHTML = '<span class="toggle-icon">&#9776;</span> <span class="toggle-label">Page Mode</span>';
    toggleBtn.title = 'Switch between scroll and page reading mode';
    document.body.appendChild(toggleBtn);

    // Create page counter
    const pageCounter = document.createElement('div');
    pageCounter.className = 'page-counter';
    document.body.appendChild(pageCounter);

    // Create nav arrows
    const navPrev = document.createElement('button');
    navPrev.className = 'page-nav-btn page-nav-prev disabled';
    navPrev.innerHTML = '&#8592;';
    navPrev.title = 'Previous page';
    document.body.appendChild(navPrev);

    const navNext = document.createElement('button');
    navNext.className = 'page-nav-btn page-nav-next';
    navNext.innerHTML = '&#8594;';
    navNext.title = 'Next page';
    document.body.appendChild(navNext);

    function splitIntoPages() {
        const children = Array.from(prose.children);
        pages = [];
        let currentGroup = [];
        let paraCount = 0;

        for (let i = 0; i < children.length; i++) {
            const el = children[i];
            const tag = el.tagName ? el.tagName.toUpperCase() : '';

            // Split at h2 headings or every ~3 paragraphs
            if (tag === 'H2' && currentGroup.length > 0) {
                pages.push(currentGroup);
                currentGroup = [];
                paraCount = 0;
            }

            currentGroup.push(el);

            if (tag === 'P' || tag === 'BLOCKQUOTE' || tag === 'PRE' || tag === 'UL' || tag === 'OL') {
                paraCount++;
            }

            if (paraCount >= 3 && i < children.length - 1) {
                // Check if next element is not an h2 (to avoid tiny pages)
                const nextTag = children[i + 1] && children[i + 1].tagName ? children[i + 1].tagName.toUpperCase() : '';
                if (nextTag !== 'H2' || paraCount >= 4) {
                    pages.push(currentGroup);
                    currentGroup = [];
                    paraCount = 0;
                }
            }
        }

        if (currentGroup.length > 0) {
            pages.push(currentGroup);
        }
    }

    function enablePageMode() {
        pageMode = true;
        currentPage = 0;
        document.body.classList.add('page-mode-active');
        toggleBtn.classList.add('active');
        toggleBtn.querySelector('.toggle-label').textContent = 'Scroll Mode';

        splitIntoPages();
        if (pages.length === 0) return;

        // Create slide wrapper
        slideWrapper = document.createElement('div');
        slideWrapper.className = 'page-slide-wrapper';

        // Build page divs
        pages.forEach(function (group, idx) {
            const pageDiv = document.createElement('div');
            pageDiv.className = 'reading-page';
            pageDiv.dataset.page = idx;
            group.forEach(function (el) {
                pageDiv.appendChild(el);
            });
            slideWrapper.appendChild(pageDiv);
        });

        prose.classList.add('page-mode');
        prose.appendChild(slideWrapper);

        updatePageUI();

        // Scroll to top of content area
        prose.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function disablePageMode() {
        pageMode = false;
        document.body.classList.remove('page-mode-active');
        toggleBtn.classList.remove('active');
        toggleBtn.querySelector('.toggle-label').textContent = 'Page Mode';

        if (!slideWrapper) return;

        // Move all elements back to prose
        const allElements = [];
        slideWrapper.querySelectorAll('.reading-page').forEach(function (pageDiv) {
            while (pageDiv.firstChild) {
                allElements.push(pageDiv.firstChild);
                pageDiv.removeChild(pageDiv.firstChild);
            }
        });

        prose.removeChild(slideWrapper);
        slideWrapper = null;
        prose.classList.remove('page-mode');

        allElements.forEach(function (el) {
            prose.appendChild(el);
        });

        pages = [];
    }

    function goToPage(idx) {
        if (idx < 0 || idx >= pages.length) return;
        currentPage = idx;
        if (slideWrapper) {
            slideWrapper.style.transform = 'translateX(-' + (currentPage * 100) + '%)';
        }
        updatePageUI();
    }

    function updatePageUI() {
        pageCounter.textContent = 'Page ' + (currentPage + 1) + ' of ' + pages.length;
        navPrev.classList.toggle('disabled', currentPage === 0);
        navNext.classList.toggle('disabled', currentPage >= pages.length - 1);
    }

    toggleBtn.addEventListener('click', function () {
        if (pageMode) {
            disablePageMode();
        } else {
            enablePageMode();
        }
    });

    navPrev.addEventListener('click', function () { goToPage(currentPage - 1); });
    navNext.addEventListener('click', function () { goToPage(currentPage + 1); });

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
        if (!pageMode) return;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            e.preventDefault();
            goToPage(currentPage + 1);
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            e.preventDefault();
            goToPage(currentPage - 1);
        }
    });

    // Touch swipe support
    prose.addEventListener('touchstart', function (e) {
        if (!pageMode) return;
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
        touchDeltaX = 0;
        isSwiping = false;
    }, { passive: true });

    prose.addEventListener('touchmove', function (e) {
        if (!pageMode) return;
        var dx = e.touches[0].clientX - touchStartX;
        var dy = e.touches[0].clientY - touchStartY;

        // Detect horizontal swipe (not vertical scroll)
        if (!isSwiping && Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 10) {
            isSwiping = true;
        }

        if (isSwiping) {
            touchDeltaX = dx;
            // Live drag feedback
            if (slideWrapper) {
                var offset = -(currentPage * 100);
                var dragPercent = (touchDeltaX / prose.offsetWidth) * 100;
                slideWrapper.style.transition = 'none';
                slideWrapper.style.transform = 'translateX(' + (offset + dragPercent) + '%)';
            }
        }
    }, { passive: true });

    prose.addEventListener('touchend', function () {
        if (!pageMode || !isSwiping) return;
        if (slideWrapper) {
            slideWrapper.style.transition = 'transform 0.45s cubic-bezier(0.4, 0, 0.2, 1)';
        }

        var threshold = prose.offsetWidth * 0.2;
        if (touchDeltaX < -threshold) {
            goToPage(currentPage + 1);
        } else if (touchDeltaX > threshold) {
            goToPage(currentPage - 1);
        } else {
            goToPage(currentPage); // snap back
        }
        isSwiping = false;
    }, { passive: true });


    // ── 2. KEYWORD-TRIGGERED BACKGROUND ANIMATIONS ──

    var kwCanvas = document.getElementById('keyword-canvas');
    var kwCtx = kwCanvas ? kwCanvas.getContext('2d') : null;
    var kwWidth, kwHeight;
    var activeKeywordTheme = null;
    var kwAnimId = null;
    var kwTime = 0;
    var kwFadeAlpha = 0;
    var kwTargetAlpha = 0;

    // Matrix rain state
    var matrixColumns = [];
    var matrixDrops = [];
    // Galaxy state
    var galaxyStars = [];
    // Neural state
    var neuralNodes = [];

    var keywordThemes = {
        void: { keywords: ['shunya', 'zero', 'void', 'nothingness'] },
        om: { keywords: ['om', '\u0950', 'brahman', 'atman'] },
        matrix: { keywords: ['simulation', 'matrix', 'digital'] },
        galaxy: { keywords: ['galaxy', 'universe', 'cosmos', 'stars'] },
        consciousness: { keywords: ['consciousness', 'awareness', 'mind'] },
        infinity: { keywords: ['infinity', '\u221E'] },
        code: { keywords: ['code', 'python', 'data', 'pipeline'] }
    };

    function resizeKwCanvas() {
        if (!kwCanvas) return;
        kwWidth = kwCanvas.width = window.innerWidth;
        kwHeight = kwCanvas.height = window.innerHeight;
        initMatrixRain();
        initGalaxyStars();
        initNeuralNodes();
    }

    function initMatrixRain() {
        var colW = 14;
        var cols = Math.ceil(kwWidth / colW);
        matrixColumns = [];
        matrixDrops = [];
        for (var i = 0; i < cols; i++) {
            matrixColumns.push(i * colW);
            matrixDrops.push(Math.random() * kwHeight);
        }
    }

    function initGalaxyStars() {
        galaxyStars = [];
        for (var i = 0; i < 200; i++) {
            var angle = Math.random() * Math.PI * 2;
            var dist = Math.random() * Math.min(kwWidth, kwHeight) * 0.45;
            galaxyStars.push({
                angle: angle, dist: dist,
                speed: 0.002 + Math.random() * 0.005,
                size: Math.random() * 2 + 0.5,
                brightness: Math.random()
            });
        }
    }

    function initNeuralNodes() {
        neuralNodes = [];
        for (var i = 0; i < 50; i++) {
            neuralNodes.push({
                x: Math.random() * kwWidth,
                y: Math.random() * kwHeight,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 3 + 1,
                pulse: Math.random() * Math.PI * 2
            });
        }
    }

    if (kwCanvas) {
        resizeKwCanvas();
        window.addEventListener('resize', resizeKwCanvas);
    }

    // Draw functions for each theme
    function drawVoid() {
        var cx = kwWidth / 2, cy = kwHeight / 2;
        var pulse = Math.sin(kwTime * 0.5) * 0.3 + 0.7;
        var radius = 80 * pulse;

        var grad = kwCtx.createRadialGradient(cx, cy, 0, cx, cy, radius * 3);
        grad.addColorStop(0, 'rgba(0,0,0,0.8)');
        grad.addColorStop(0.5, 'rgba(5,5,20,0.4)');
        grad.addColorStop(1, 'rgba(0,0,0,0)');
        kwCtx.fillStyle = grad;
        kwCtx.fillRect(0, 0, kwWidth, kwHeight);

        // Glowing circle
        kwCtx.beginPath();
        kwCtx.arc(cx, cy, radius, 0, Math.PI * 2);
        kwCtx.strokeStyle = 'rgba(167, 139, 250, ' + (0.3 * pulse) + ')';
        kwCtx.lineWidth = 2;
        kwCtx.stroke();

        // Outer glow ring
        kwCtx.beginPath();
        kwCtx.arc(cx, cy, radius * 1.5, 0, Math.PI * 2);
        kwCtx.strokeStyle = 'rgba(99, 102, 241, ' + (0.15 * pulse) + ')';
        kwCtx.lineWidth = 1;
        kwCtx.stroke();
    }

    function drawOm() {
        var cx = kwWidth / 2, cy = kwHeight / 2;
        var pulse = Math.sin(kwTime * 0.4) * 0.4 + 0.8;
        var radius = 120 * pulse;

        var grad = kwCtx.createRadialGradient(cx, cy, 0, cx, cy, radius * 2);
        grad.addColorStop(0, 'rgba(240, 192, 64, ' + (0.12 * pulse) + ')');
        grad.addColorStop(0.4, 'rgba(255, 153, 51, ' + (0.06 * pulse) + ')');
        grad.addColorStop(1, 'rgba(0,0,0,0)');
        kwCtx.fillStyle = grad;
        kwCtx.fillRect(0, 0, kwWidth, kwHeight);

        // Pulsing rings
        for (var i = 0; i < 5; i++) {
            var r = radius * (0.3 + i * 0.2) + Math.sin(kwTime * 0.6 + i) * 10;
            kwCtx.beginPath();
            kwCtx.arc(cx, cy, r, 0, Math.PI * 2);
            kwCtx.strokeStyle = 'rgba(240, 192, 64, ' + (0.08 - i * 0.012) + ')';
            kwCtx.lineWidth = 1.5;
            kwCtx.stroke();
        }
    }

    function drawMatrix() {
        kwCtx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        kwCtx.fillRect(0, 0, kwWidth, kwHeight);

        kwCtx.font = '12px monospace';
        kwCtx.fillStyle = 'rgba(34, 211, 100, 0.12)';

        var chars = '01\u0950\u221E\u25CB';
        for (var i = 0; i < matrixDrops.length; i++) {
            var ch = chars[Math.floor(Math.random() * chars.length)];
            kwCtx.fillText(ch, matrixColumns[i], matrixDrops[i]);
            matrixDrops[i] += 12;
            if (matrixDrops[i] > kwHeight && Math.random() > 0.98) {
                matrixDrops[i] = 0;
            }
        }
    }

    function drawGalaxy() {
        var cx = kwWidth / 2, cy = kwHeight / 2;

        for (var i = 0; i < galaxyStars.length; i++) {
            var s = galaxyStars[i];
            s.angle += s.speed;

            // Spiral offset
            var spiralDist = s.dist + Math.sin(s.angle * 2) * 30;
            var x = cx + Math.cos(s.angle) * spiralDist;
            var y = cy + Math.sin(s.angle) * spiralDist * 0.6;

            var alpha = 0.08 + s.brightness * 0.12;
            var hue = (s.angle * 30 + kwTime * 10) % 360;

            kwCtx.beginPath();
            kwCtx.arc(x, y, s.size, 0, Math.PI * 2);
            kwCtx.fillStyle = 'hsla(' + hue + ', 60%, 70%, ' + alpha + ')';
            kwCtx.fill();
        }
    }

    function drawConsciousnessNet() {
        for (var i = 0; i < neuralNodes.length; i++) {
            var n = neuralNodes[i];
            n.x += n.vx;
            n.y += n.vy;
            n.pulse += 0.02;

            if (n.x < 0 || n.x > kwWidth) n.vx *= -1;
            if (n.y < 0 || n.y > kwHeight) n.vy *= -1;

            var alpha = 0.1 + Math.sin(n.pulse) * 0.06;

            kwCtx.beginPath();
            kwCtx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
            kwCtx.fillStyle = 'rgba(167, 139, 250, ' + alpha + ')';
            kwCtx.fill();

            // Connect nearby
            for (var j = i + 1; j < neuralNodes.length; j++) {
                var m = neuralNodes[j];
                var dx = n.x - m.x, dy = n.y - m.y;
                var distSq = dx * dx + dy * dy;
                if (distSq < 20000) {
                    var lineA = (1 - distSq / 20000) * 0.04;
                    kwCtx.beginPath();
                    kwCtx.moveTo(n.x, n.y);
                    kwCtx.lineTo(m.x, m.y);
                    kwCtx.strokeStyle = 'rgba(167, 139, 250, ' + lineA + ')';
                    kwCtx.lineWidth = 0.5;
                    kwCtx.stroke();
                }
            }
        }
    }

    function drawInfinityLoop() {
        var cx = kwWidth / 2, cy = kwHeight / 2;
        var scale = Math.min(kwWidth, kwHeight) * 0.2;

        kwCtx.beginPath();
        for (var t = 0; t < Math.PI * 2; t += 0.02) {
            var angle = t + kwTime * 0.3;
            // Lemniscate of Bernoulli
            var denom = 1 + Math.sin(angle) * Math.sin(angle);
            var x = cx + (scale * Math.cos(angle)) / denom;
            var y = cy + (scale * Math.sin(angle) * Math.cos(angle)) / denom;
            if (t === 0) kwCtx.moveTo(x, y); else kwCtx.lineTo(x, y);
        }
        kwCtx.closePath();
        kwCtx.strokeStyle = 'rgba(240, 192, 64, 0.12)';
        kwCtx.lineWidth = 2;
        kwCtx.stroke();

        // Second loop slightly offset
        kwCtx.beginPath();
        for (var t2 = 0; t2 < Math.PI * 2; t2 += 0.02) {
            var angle2 = t2 + kwTime * 0.3 + 0.5;
            var denom2 = 1 + Math.sin(angle2) * Math.sin(angle2);
            var x2 = cx + (scale * 1.1 * Math.cos(angle2)) / denom2;
            var y2 = cy + (scale * 1.1 * Math.sin(angle2) * Math.cos(angle2)) / denom2;
            if (t2 === 0) kwCtx.moveTo(x2, y2); else kwCtx.lineTo(x2, y2);
        }
        kwCtx.closePath();
        kwCtx.strokeStyle = 'rgba(167, 139, 250, 0.08)';
        kwCtx.lineWidth = 1.5;
        kwCtx.stroke();
    }

    function drawCodeRain() {
        kwCtx.fillStyle = 'rgba(0, 0, 0, 0.04)';
        kwCtx.fillRect(0, 0, kwWidth, kwHeight);

        kwCtx.font = '11px monospace';
        var codeChars = '{}[]();=>+-*/|&^~!@#$%def class import for while';
        kwCtx.fillStyle = 'rgba(34, 211, 238, 0.1)';

        for (var i = 0; i < matrixDrops.length; i += 2) {
            var ch = codeChars[Math.floor(Math.random() * codeChars.length)];
            kwCtx.fillText(ch, matrixColumns[i], matrixDrops[i]);
            matrixDrops[i] += 10;
            if (matrixDrops[i] > kwHeight && Math.random() > 0.97) {
                matrixDrops[i] = 0;
            }
        }
    }

    var kwDrawFunctions = {
        void: drawVoid,
        om: drawOm,
        matrix: drawMatrix,
        galaxy: drawGalaxy,
        consciousness: drawConsciousnessNet,
        infinity: drawInfinityLoop,
        code: drawCodeRain
    };

    function kwAnimate() {
        if (!kwCtx) return;

        // Fade in/out
        if (activeKeywordTheme) {
            kwTargetAlpha = 1;
        } else {
            kwTargetAlpha = 0;
        }
        kwFadeAlpha += (kwTargetAlpha - kwFadeAlpha) * 0.03;

        if (kwFadeAlpha < 0.01 && kwTargetAlpha === 0) {
            kwCanvas.classList.remove('active');
            kwAnimId = requestAnimationFrame(kwAnimate);
            return;
        }

        kwCanvas.classList.add('active');
        kwCanvas.style.opacity = kwFadeAlpha;

        // Only clear for non-trail themes
        if (activeKeywordTheme !== 'matrix' && activeKeywordTheme !== 'code') {
            kwCtx.clearRect(0, 0, kwWidth, kwHeight);
        }

        if (activeKeywordTheme && kwDrawFunctions[activeKeywordTheme]) {
            kwDrawFunctions[activeKeywordTheme]();
        }

        kwTime += 0.016;
        kwAnimId = requestAnimationFrame(kwAnimate);
    }

    if (kwCanvas) {
        kwAnimate();
    }

    // IntersectionObserver to detect visible paragraphs and scan for keywords
    function scanTextForKeywords(text) {
        var lower = text.toLowerCase();
        for (var theme in keywordThemes) {
            var kws = keywordThemes[theme].keywords;
            for (var i = 0; i < kws.length; i++) {
                if (lower.indexOf(kws[i].toLowerCase()) !== -1) {
                    return theme;
                }
            }
        }
        return null;
    }

    var visibleThemes = new Map();
    var kwObserver = null;

    function setupKeywordObserver() {
        var elements = prose.querySelectorAll('p, h2, h3, h4, blockquote, li');
        if (elements.length === 0) return;

        kwObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                var el = entry.target;
                var text = el.textContent || '';
                var theme = scanTextForKeywords(text);

                if (entry.isIntersecting && theme) {
                    visibleThemes.set(el, theme);
                } else {
                    visibleThemes.delete(el);
                }
            });

            // Pick the most recent visible theme
            if (visibleThemes.size > 0) {
                var lastTheme = null;
                visibleThemes.forEach(function (t) { lastTheme = t; });
                activeKeywordTheme = lastTheme;
            } else {
                activeKeywordTheme = null;
            }
        }, { threshold: 0.3 });

        elements.forEach(function (el) {
            kwObserver.observe(el);
        });
    }

    setupKeywordObserver();


    // ── 3. INTERACTIVE TEXT EFFECTS ──

    // 3a. Sanskrit text golden glow — detect Devanagari unicode and wrap
    function wrapSanskritText() {
        var walker = document.createTreeWalker(prose, NodeFilter.SHOW_TEXT, null, false);
        var devanagariRegex = /[\u0900-\u097F\u0950]+/g;
        var nodesToProcess = [];

        while (walker.nextNode()) {
            var node = walker.currentNode;
            if (node.parentElement && node.parentElement.closest('.sanskrit-hover-glow')) continue;
            if (devanagariRegex.test(node.textContent)) {
                nodesToProcess.push(node);
            }
            devanagariRegex.lastIndex = 0;
        }

        nodesToProcess.forEach(function (textNode) {
            var text = textNode.textContent;
            var parts = text.split(/([\u0900-\u097F\u0950]+)/g);
            if (parts.length <= 1) return;

            var frag = document.createDocumentFragment();
            parts.forEach(function (part) {
                if (/[\u0900-\u097F\u0950]/.test(part)) {
                    var span = document.createElement('span');
                    span.className = 'sanskrit-hover-glow';
                    span.textContent = part;
                    frag.appendChild(span);
                } else {
                    frag.appendChild(document.createTextNode(part));
                }
            });

            textNode.parentNode.replaceChild(frag, textNode);
        });
    }

    wrapSanskritText();

    // 3b. Blockquote parallax float on scroll
    var blockquotes = prose.querySelectorAll('blockquote');
    blockquotes.forEach(function (bq) {
        bq.classList.add('parallax-quote');
    });

    var lastScrollY = window.scrollY;
    var ticking = false;

    function updateParallaxQuotes() {
        var scrollY = window.scrollY;
        blockquotes.forEach(function (bq) {
            var rect = bq.getBoundingClientRect();
            var viewH = window.innerHeight;
            if (rect.top < viewH && rect.bottom > 0) {
                // Offset based on position in viewport
                var centerOffset = (rect.top + rect.height / 2 - viewH / 2) / viewH;
                var translateY = centerOffset * -12; // subtle float
                bq.style.transform = 'translateY(' + translateY.toFixed(2) + 'px)';
            }
        });
        ticking = false;
    }

    // 3c. H2 heading reveal animation
    var headings = prose.querySelectorAll('h2');
    headings.forEach(function (h) {
        h.classList.add('heading-reveal');
    });

    var headingObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, { threshold: 0.2 });

    headings.forEach(function (h) { headingObserver.observe(h); });

    // Scroll handler — throttled with rAF
    window.addEventListener('scroll', function () {
        if (!ticking) {
            requestAnimationFrame(updateParallaxQuotes);
            ticking = true;
        }
    }, { passive: true });

    // Handle visibility change for keyword canvas
    document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
            if (kwAnimId) cancelAnimationFrame(kwAnimId);
        } else {
            if (kwCanvas) kwAnimate();
        }
    });

})();
