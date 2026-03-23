/**
 * CosmicVedanta - Immersive Cosmic Background & UI Interactions
 * Stars, nebulae, and consciousness-inspired particle effects
 */

(function () {
    'use strict';

    // ── Cosmic Background Canvas ──
    const canvas = document.getElementById('cosmic-bg');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let stars = [];
    let nebulae = [];
    let animationId;

    const STAR_COUNT = 200;
    const NEBULA_COUNT = 4;

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    function createStars() {
        stars = [];
        for (let i = 0; i < STAR_COUNT; i++) {
            stars.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.8 + 0.2,
                alpha: Math.random() * 0.8 + 0.2,
                alphaSpeed: Math.random() * 0.008 + 0.002,
                alphaDir: Math.random() > 0.5 ? 1 : -1,
                // Color: mix of whites, golds, violets, cyans
                color: randomStarColor(),
                drift: (Math.random() - 0.5) * 0.15,
            });
        }
    }

    function randomStarColor() {
        const colors = [
            '255, 255, 255',   // white
            '240, 192, 64',    // gold
            '167, 139, 250',   // violet
            '34, 211, 238',    // cyan
            '244, 114, 182',   // rose
            '255, 200, 150',   // warm
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    function createNebulae() {
        nebulae = [];
        const nebulaColors = [
            { r: 99, g: 102, b: 241, a: 0.015 },   // indigo
            { r: 124, g: 58, b: 237, a: 0.012 },    // violet
            { r: 194, g: 24, b: 91, a: 0.008 },     // vedanta deep
            { r: 34, g: 211, b: 238, a: 0.008 },    // cyan
        ];
        for (let i = 0; i < NEBULA_COUNT; i++) {
            const c = nebulaColors[i % nebulaColors.length];
            nebulae.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 300 + 200,
                color: c,
                driftX: (Math.random() - 0.5) * 0.1,
                driftY: (Math.random() - 0.5) * 0.1,
            });
        }
    }

    function drawNebulae() {
        for (const n of nebulae) {
            const gradient = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.radius);
            gradient.addColorStop(0, `rgba(${n.color.r}, ${n.color.g}, ${n.color.b}, ${n.color.a})`);
            gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
            ctx.fillStyle = gradient;
            ctx.fillRect(n.x - n.radius, n.y - n.radius, n.radius * 2, n.radius * 2);

            // Drift
            n.x += n.driftX;
            n.y += n.driftY;
            if (n.x < -n.radius) n.x = width + n.radius;
            if (n.x > width + n.radius) n.x = -n.radius;
            if (n.y < -n.radius) n.y = height + n.radius;
            if (n.y > height + n.radius) n.y = -n.radius;
        }
    }

    function drawStars() {
        for (const s of stars) {
            // Twinkle
            s.alpha += s.alphaSpeed * s.alphaDir;
            if (s.alpha >= 1) { s.alpha = 1; s.alphaDir = -1; }
            if (s.alpha <= 0.1) { s.alpha = 0.1; s.alphaDir = 1; }

            ctx.beginPath();
            ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${s.color}, ${s.alpha})`;
            ctx.fill();

            // Subtle glow for larger stars
            if (s.radius > 1.2) {
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.radius * 3, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(${s.color}, ${s.alpha * 0.1})`;
                ctx.fill();
            }

            // Drift
            s.y += s.drift;
            if (s.y < -5) s.y = height + 5;
            if (s.y > height + 5) s.y = -5;
        }
    }

    // Occasional shooting star
    let shootingStar = null;
    let shootingTimer = 0;

    function maybeShootingStar() {
        shootingTimer++;
        if (shootingTimer > 400 && Math.random() < 0.005) {
            shootingStar = {
                x: Math.random() * width * 0.8,
                y: Math.random() * height * 0.3,
                length: Math.random() * 80 + 40,
                speed: Math.random() * 6 + 4,
                alpha: 1,
                angle: Math.PI / 4 + (Math.random() - 0.5) * 0.3,
            };
            shootingTimer = 0;
        }
    }

    function drawShootingStar() {
        if (!shootingStar) return;
        const s = shootingStar;
        const dx = Math.cos(s.angle) * s.length;
        const dy = Math.sin(s.angle) * s.length;

        const gradient = ctx.createLinearGradient(s.x, s.y, s.x - dx, s.y - dy);
        gradient.addColorStop(0, `rgba(255, 255, 255, ${s.alpha})`);
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(s.x - dx, s.y - dy);
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Move
        s.x += Math.cos(s.angle) * s.speed;
        s.y += Math.sin(s.angle) * s.speed;
        s.alpha -= 0.015;

        if (s.alpha <= 0 || s.x > width + 100 || s.y > height + 100) {
            shootingStar = null;
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        drawNebulae();
        drawStars();
        maybeShootingStar();
        drawShootingStar();
        animationId = requestAnimationFrame(animate);
    }

    // Initialize
    resize();
    createStars();
    createNebulae();
    animate();

    window.addEventListener('resize', function () {
        resize();
        createStars();
        createNebulae();
    });

    // Reduce animation when tab is not visible
    document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
            cancelAnimationFrame(animationId);
        } else {
            animate();
        }
    });


    // ── Mobile Nav Toggle ──
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function () {
            navLinks.classList.toggle('active');
        });

        // Close nav when clicking a real link (not dropdown triggers)
        navLinks.querySelectorAll('a').forEach(function (link) {
            if (!link.classList.contains('dropdown-trigger')) {
                link.addEventListener('click', function () {
                    navLinks.classList.remove('active');
                    // Also close any open dropdowns
                    document.querySelectorAll('.nav-dropdown.open').forEach(function (d) {
                        d.classList.remove('open');
                    });
                });
            }
        });
    }

    // ── Dropdown Toggle (works on both mobile & desktop click) ──
    document.querySelectorAll('.dropdown-trigger').forEach(function (trigger) {
        trigger.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            var parent = this.closest('.nav-dropdown');
            var isOpen = parent.classList.contains('open');

            // Close all other dropdowns
            document.querySelectorAll('.nav-dropdown.open').forEach(function (d) {
                d.classList.remove('open');
            });

            // Toggle this one
            if (!isOpen) {
                parent.classList.add('open');
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function () {
        document.querySelectorAll('.nav-dropdown.open').forEach(function (d) {
            d.classList.remove('open');
        });
    });


    // ── Scroll-based nav background ──
    const nav = document.querySelector('.cosmic-nav');
    if (nav) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                nav.style.background = 'rgba(5, 5, 16, 0.95)';
            } else {
                nav.style.background = 'rgba(5, 5, 16, 0.85)';
            }
        });
    }


    // ── Auto-dismiss alerts ──
    document.querySelectorAll('.cosmic-alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(30px)';
            setTimeout(function () { alert.remove(); }, 400);
        }, 5000);
    });

})();
