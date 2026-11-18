(() => {
  const root = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const WA = '27640725121';

  /* Hero entrance */
  const start = () => requestAnimationFrame(() => root.classList.add('is-loaded'));
  if (document.readyState === 'complete') start(); else window.addEventListener('load', start, { once: true });
  setTimeout(start, 1600); // do not hold the hero hostage to a slow image

  const yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  /* Header turns solid once the hero top leaves */
  const header = document.querySelector('.site-header');
  const hero = document.querySelector('.hero');
  const fab = document.querySelector('.fab');
  if (header) {
    const sentinel = document.createElement('div');
    sentinel.style.cssText = 'position:absolute;top:0;left:0;height:80px;width:1px;pointer-events:none';
    document.body.prepend(sentinel);
    new IntersectionObserver(([e]) => header.classList.toggle('is-solid', !e.isIntersecting)).observe(sentinel);
  }
  if (hero && fab) {
    new IntersectionObserver(([e]) => fab.classList.toggle('is-on', !e.isIntersecting), { threshold: .15 }).observe(hero);
  } else if (fab) {
    fab.classList.add('is-on');
  }

  /* Mobile menu */
  const btn = document.querySelector('.menu-btn');
  const nav = document.getElementById('nav');
  if (btn && nav) {
    const set = (open) => {
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      nav.classList.toggle('is-open', open);
      header.classList.toggle('menu-open', open);
    };
    btn.addEventListener('click', () => set(btn.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') set(false); });
    window.matchMedia('(min-width: 981px)').addEventListener('change', (m) => { if (m.matches) set(false); });
  }

  /* Embers drifting up from the braai side of the hero photo */
  const canvas = document.querySelector('.hero__embers');
  if (canvas && !reduce) {
    const ctx = canvas.getContext('2d');
    let w = 0, h = 0, dpr = 1, raf = 0, running = false, embers = [];
    const mobile = () => w < 700;
    const spawn = (anywhere) => {
      const fromX = mobile() ? .15 : .48;
      return {
        x: w * (fromX + Math.random() * (1 - fromX)),
        y: anywhere ? Math.random() * h : h * (mobile() ? .9 : .8) + Math.random() * h * .2,
        r: .6 + Math.random() * 1.7,
        vy: .25 + Math.random() * .7,
        vx: -.15 + Math.random() * .3,
        sway: Math.random() * Math.PI * 2,
        life: 0,
        max: 260 + Math.random() * 380,
        hue: 18 + Math.random() * 22
      };
    };
    const resize = () => {
      const r = canvas.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = r.width; h = r.height;
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = mobile() ? 22 : 46;
      embers = Array.from({ length: n }, () => spawn(true));
    };
    const tick = () => {
      ctx.clearRect(0, 0, w, h);
      ctx.globalCompositeOperation = 'lighter';
      for (let i = 0; i < embers.length; i++) {
        const p = embers[i];
        p.life++;
        p.sway += .02;
        p.x += p.vx + Math.sin(p.sway) * .35;
        p.y -= p.vy;
        const t = p.life / p.max;
        if (t >= 1 || p.y < -10) { embers[i] = spawn(false); continue; }
        const a = Math.sin(Math.PI * t) * .85;
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4);
        g.addColorStop(0, `hsla(${p.hue}, 100%, 70%, ${a})`);
        g.addColorStop(.35, `hsla(${p.hue}, 95%, 55%, ${a * .45})`);
        g.addColorStop(1, `hsla(${p.hue}, 90%, 45%, 0)`);
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r * 4, 0, Math.PI * 2); ctx.fill();
      }
      raf = requestAnimationFrame(tick);
    };
    const play = (on) => {
      if (on && !running) { running = true; raf = requestAnimationFrame(tick); }
      if (!on && running) { running = false; cancelAnimationFrame(raf); }
    };
    resize();
    let rt;
    window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(resize, 150); });
    new IntersectionObserver(([e]) => play(e.isIntersecting)).observe(canvas);
    document.addEventListener('visibilitychange', () => play(!document.hidden && canvas.getBoundingClientRect().bottom > 0));
  }

  /* Braai planner */
  const form = document.getElementById('plan');
  if (form) {
    const state = { adults: 4, kids: 2, nights: 3 };
    const limits = { adults: [1, 30], kids: [0, 30], nights: [1, 14] };
    const list = document.getElementById('plan-list');
    const total = document.getElementById('plan-total');
    const when = document.getElementById('plan-when');
    const prev = {};

    if (when) {
      const d = new Date();
      when.min = new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    }

    const kg = (g) => {
      const v = Math.max(.5, Math.round(g / 250) * .25);
      return v.toFixed(2).replace(/0+$/, '').replace(/\.$/, '') + ' kg';
    };

    const compute = () => {
      const meats = [...form.querySelectorAll('input[name="meat"]:checked')].map((i) => i.value);
      const biltong = form.querySelector('input[name="extra"]:checked');
      const perBraai = state.adults * 350 + state.kids * 175;
      const all = perBraai * state.nights;
      const items = meats.map((m) => ({ name: m, qty: kg(all / meats.length) }));
      if (biltong) items.push({ name: 'Biltong', qty: kg(state.adults * 100 * Math.min(state.nights, 7)) });
      return { items, all, meats };
    };

    const render = () => {
      for (const k of Object.keys(state)) {
        document.getElementById(k).textContent = state[k];
        form.querySelector(`[data-step="${k}"][data-d="-1"]`).disabled = state[k] <= limits[k][0];
        form.querySelector(`[data-step="${k}"][data-d="1"]`).disabled = state[k] >= limits[k][1];
      }
      const { items, all, meats } = compute();
      if (!meats.length && !items.length) {
        list.innerHTML = '<li class="plan__empty">Pick at least one thing for the fire and we\'ll work out the amounts.</li>';
        total.textContent = '';
        return;
      }
      list.innerHTML = items.map((i) => `<li><span>${i.name}</span><span class="q${prev[i.name] && prev[i.name] !== i.qty ? ' bump' : ''}">${i.qty}</span></li>`).join('');
      items.forEach((i) => { prev[i.name] = i.qty; });
      total.innerHTML = meats.length
        ? `About <strong>${kg(all)}</strong> of braai meat for ${state.nights} ${state.nights === 1 ? 'night' : 'nights'}.`
        : 'Add something for the fire to see braai amounts.';
    };

    form.addEventListener('click', (e) => {
      const b = e.target.closest('[data-step]');
      if (!b) return;
      const k = b.dataset.step;
      state[k] = Math.min(limits[k][1], Math.max(limits[k][0], state[k] + Number(b.dataset.d)));
      render();
    });
    form.addEventListener('change', render);

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const { items } = compute();
      const name = form.elements.name.value.trim();
      let day = '';
      if (when && when.value) {
        const d = new Date(when.value + 'T12:00:00');
        day = d.toLocaleDateString('en-ZA', { weekday: 'long', day: 'numeric', month: 'long' });
      }
      const lines = [
        'Hi Wild Butchery,',
        '',
        `We're ${state.adults} ${state.adults === 1 ? 'adult' : 'adults'}${state.kids ? ` and ${state.kids} ${state.kids === 1 ? 'child' : 'children'}` : ''} braaiing for ${state.nights} ${state.nights === 1 ? 'night' : 'nights'}. Could you put this together for us?`,
        '',
        ...(items.length ? items.map((i) => `- ${i.name}: ${i.qty}`) : ['- (please suggest a mix)']),
        '',
        day ? `We'd like to collect on ${day}.` : 'Please let us know when we can collect.',
        name ? `Thanks, ${name}` : 'Thank you!'
      ];
      window.open(`https://wa.me/${WA}?text=${encodeURIComponent(lines.join('\n'))}`, '_blank', 'noopener');
    });

    render();
  }
})();
