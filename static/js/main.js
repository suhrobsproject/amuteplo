document.addEventListener("DOMContentLoaded", function () {

    // 1. Tungi va kunduzgi rejim
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    function setThemeIcon(theme) {
        if (!themeIcon) return;
        themeIcon.classList.toggle('fa-sun', theme === 'dark');
        themeIcon.classList.toggle('fa-moon', theme !== 'dark');
    }
    setThemeIcon(document.documentElement.getAttribute('data-theme'));

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function () {
            const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            if (next === 'dark') {
                document.documentElement.setAttribute('data-theme', 'dark');
            } else {
                document.documentElement.removeAttribute('data-theme');
            }
            try { localStorage.setItem('theme', next); } catch (e) {}
            setThemeIcon(next);
        });
    }

    // 2. Mobil menyu (burger)
    const burger = document.getElementById('burger');
    const nav = document.getElementById('main-nav');

    function closeMenu() {
        if (!nav) return;
        nav.classList.remove('open');
        document.body.classList.remove('no-scroll');
        if (burger) {
            burger.setAttribute('aria-expanded', 'false');
            burger.querySelector('i').className = 'fas fa-bars';
        }
    }

    if (burger && nav) {
        burger.addEventListener('click', function () {
            const open = !nav.classList.contains('open');
            nav.classList.toggle('open', open);
            document.body.classList.toggle('no-scroll', open);
            burger.setAttribute('aria-expanded', String(open));
            burger.querySelector('i').className = open ? 'fas fa-times' : 'fas fa-bars';
        });
        nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeMenu); });
        window.addEventListener('resize', function () { if (window.innerWidth > 960) closeMenu(); });
    }

    // 3. Bosh banner slayderi
    const slides = document.querySelectorAll('.hero .slide');
    const dots = document.querySelectorAll('.hero .dot-btn');
    if (slides.length > 1) {
        let cur = 0;
        let timer;
        function show(i) {
            slides[cur].classList.remove('active');
            if (dots[cur]) dots[cur].classList.remove('active');
            cur = (i + slides.length) % slides.length;
            slides[cur].classList.add('active');
            if (dots[cur]) dots[cur].classList.add('active');
        }
        function start() {
            clearInterval(timer);
            timer = setInterval(function () { show(cur + 1); }, 5000);
        }
        dots.forEach(function (d, i) { d.addEventListener('click', function () { show(i); start(); }); });

        // Telefonda barmoq bilan surish
        const hero = document.querySelector('.hero');
        let startX = null;
        hero.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
        hero.addEventListener('touchend', function (e) {
            if (startX === null) return;
            const dx = e.changedTouches[0].clientX - startX;
            if (Math.abs(dx) > 50) { show(dx < 0 ? cur + 1 : cur - 1); start(); }
            startX = null;
        });
        start();
    }

    // 4. "Menga qaysi qozon mos?" kalkulyatori
    const calcForm = document.getElementById('calc-form');
    const dataEl = document.getElementById('calc-data');
    if (calcForm && dataEl) {
        const boilers = JSON.parse(dataEl.textContent || '[]');

        function numbers(str) {
            return (String(str || '').replace(/,/g, '.').match(/\d+(\.\d+)?/g) || []).map(parseFloat);
        }
        // Qozon isita oladigan maksimal maydon: "Isitish maydoni" dan, bo'lmasa quvvatdan (1 kVt ≈ 10 m²)
        function capacity(b) {
            const a = numbers(b.area);
            if (a.length) return Math.max.apply(null, a);
            const p = numbers(b.power);
            return p.length ? Math.max.apply(null, p) * 10 : null;
        }
        function formatPrice(n) {
            return n === null ? '—' : String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
        }

        const placeholder = document.getElementById('calc-placeholder');
        const result = document.getElementById('calc-result');
        const placeholderText = placeholder.textContent;

        calcForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const area = parseFloat(document.getElementById('area-input').value) || 0;
            const fuel = document.getElementById('fuel-input').value;

            const options = boilers
                .filter(function (b) { return b.fuel === fuel; })
                .map(function (b) { return { b: b, cap: capacity(b) }; });

            if (!options.length) {
                placeholder.textContent = "Bu yoqilg'i turi uchun hozircha model yo'q. Boshqa turni tanlang.";
                placeholder.style.display = 'block';
                result.classList.remove('show');
                return;
            }

            // Maydonni qoplaydigan eng kichik qozon; topilmasa — eng kuchlisi
            const known = options.filter(function (o) { return o.cap !== null; });
            let best;
            if (known.length) {
                const enough = known.filter(function (o) { return o.cap >= area; }).sort(function (x, y) { return x.cap - y.cap; });
                best = enough.length ? enough[0] : known.sort(function (x, y) { return y.cap - x.cap; })[0];
            } else {
                best = options[0];
            }
            const b = best.b;

            document.getElementById('res-name').textContent = b.name;
            document.getElementById('res-fuel').textContent = b.fuel_label;
            document.getElementById('res-power').textContent = b.power || '—';
            document.getElementById('res-area').textContent = b.area || '—';
            document.getElementById('res-price').textContent = formatPrice(b.price);
            document.getElementById('res-link').href = b.url;

            const img = document.getElementById('res-img');
            img.innerHTML = '';
            if (b.image) {
                const el = document.createElement('img');
                el.src = b.image;
                el.alt = b.name;
                img.appendChild(el);
            } else {
                img.innerHTML = '<i class="fas fa-fire"></i>';
            }

            placeholder.textContent = placeholderText;
            placeholder.style.display = 'none';
            result.classList.add('show');
            if (window.innerWidth <= 960) result.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }
});

// Buyurtma modali
function openOrderModal() {
    const m = document.getElementById('orderModal');
    if (!m) return;
    m.classList.add('show');
    document.body.classList.add('no-scroll');
}
function closeOrderModal() {
    const m = document.getElementById('orderModal');
    if (!m) return;
    m.classList.remove('show');
    if (!document.getElementById('main-nav') || !document.getElementById('main-nav').classList.contains('open')) {
        document.body.classList.remove('no-scroll');
    }
}
document.addEventListener('click', function (e) {
    if (e.target && e.target.id === 'orderModal') closeOrderModal();
});
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeOrderModal();
});
