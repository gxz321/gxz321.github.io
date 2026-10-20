/* Small, dependency-free interactions for the GXZ portfolio. */
(() => {
  'use strict';

  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const mediaChange = (query, listener) => {
    if (query.addEventListener) query.addEventListener('change', listener);
    else if (query.addListener) query.addListener(listener);
  };

  function setupMenu() {
    const toggle = document.querySelector('.menu-toggle');
    const nav = document.getElementById('main-nav');
    if (!toggle || !nav) return;

    toggle.setAttribute('aria-controls', nav.id);
    const setOpen = (open, returnFocus = false) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.classList.toggle('is-open', open);
      nav.classList.toggle('is-open', open);
      document.body.classList.toggle('menu-open', open);
      const label = toggle.querySelector('[data-menu-label]');
      if (label) label.textContent = open ? 'Close' : 'Menu';
      if (returnFocus) toggle.focus();
    };
    setOpen(false);

    toggle.addEventListener('click', () => {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) setOpen(false);
    });
    document.addEventListener('click', (event) => {
      if (!nav.contains(event.target) && !toggle.contains(event.target)) setOpen(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false, true);
      }
    });
    window.addEventListener('resize', () => {
      if (toggle.getClientRects().length === 0) setOpen(false);
    }, { passive: true });
  }

  function setupSectionNavigation() {
    if (!('IntersectionObserver' in window)) return;
    const pairs = Array.from(document.querySelectorAll('.nav-link[href]'))
      .map((link) => {
        const url = new URL(link.href, window.location.href);
        if (url.origin !== window.location.origin || url.pathname !== window.location.pathname || !url.hash) return null;
        let section;
        try { section = document.getElementById(decodeURIComponent(url.hash.slice(1))); }
        catch { return null; }
        return section ? { link, section } : null;
      }).filter(Boolean);
    if (!pairs.length) return;

    const activate = (id) => pairs.forEach(({ link, section }) => {
      const active = section.id === id;
      link.classList.toggle('is-active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible.length) activate(visible[0].target.id);
    }, { rootMargin: '-14% 0px -58% 0px', threshold: 0 });
    pairs.forEach(({ section }) => observer.observe(section));
    pairs.forEach(({ link, section }) => link.addEventListener('click', () => activate(section.id)));
  }

  function setupReveals() {
    const elements = Array.from(document.querySelectorAll('[data-reveal]'));
    if (!elements.length || motionPreference.matches || !('IntersectionObserver' in window)) return;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px 36px 0px', threshold: 0.035 });
    elements.forEach((element) => {
      element.classList.add('reveal-ready');
      observer.observe(element);
    });
    mediaChange(motionPreference, () => {
      if (!motionPreference.matches) return;
      elements.forEach((element) => element.classList.add('is-visible'));
      observer.disconnect();
    });
  }

  function setupMagneticControls() {
    document.querySelectorAll('[data-magnetic]').forEach((element) => {
      const reset = () => { element.style.translate = ''; };
      element.addEventListener('pointermove', (event) => {
        if (!finePointer.matches || motionPreference.matches || event.pointerType === 'touch') return;
        const bounds = element.getBoundingClientRect();
        const x = clamp((event.clientX - bounds.left - bounds.width / 2) * 0.055, -3, 3);
        const y = clamp((event.clientY - bounds.top - bounds.height / 2) * 0.055, -3, 3);
        element.style.translate = `${x.toFixed(2)}px ${y.toFixed(2)}px`;
      });
      element.addEventListener('pointerleave', reset);
      element.addEventListener('blur', reset);
      mediaChange(motionPreference, reset);
      mediaChange(finePointer, reset);
    });
  }

  const fields = [];
  let animationFrame = 0;
  let lastFrameTime = 0;
  const frameInterval = 1000 / 30;

  function syncAnimation() {
    const needed = !document.hidden && fields.some((field) => field.canAnimate());
    if (needed && !animationFrame) animationFrame = window.requestAnimationFrame(animate);
    else if (!needed && animationFrame) {
      window.cancelAnimationFrame(animationFrame);
      animationFrame = 0;
      lastFrameTime = 0;
    }
  }

  function animate(now) {
    animationFrame = 0;
    if (document.hidden) { lastFrameTime = 0; return; }
    const elapsed = now - lastFrameTime;
    if (!lastFrameTime || elapsed >= frameInterval) {
      const delta = lastFrameTime ? Math.min(elapsed / 1000, 0.065) : 1 / 30;
      lastFrameTime = now;
      fields.forEach((field) => {
        if (!field.canAnimate()) return;
        field.advance(delta);
        field.draw();
      });
    }
    if (fields.some((field) => field.canAnimate())) animationFrame = window.requestAnimationFrame(animate);
    else lastFrameTime = 0;
  }

  class FlowField {
    constructor(canvas) {
      this.canvas = canvas;
      this.context = canvas.getContext('2d', { alpha: false });
      if (!this.context) return;
      this.width = 0;
      this.height = 0;
      this.particles = [];
      this.pointer = { x: -1000, y: -1000, active: false };
      this.visible = true;
      this.running = !motionPreference.matches;
      this.manuallyToggled = false;
      this.time = 0;
      this.seed = 23821;
      const namedButton = Array.from(document.querySelectorAll('.flow-toggle[aria-controls]'))
        .find((button) => canvas.id && button.getAttribute('aria-controls').split(/\s+/).includes(canvas.id));
      const panel = canvas.closest('[data-flow-panel]') || canvas.parentElement;
      this.button = namedButton || panel.querySelector('.flow-toggle');
      this.palette = canvas.dataset.scheme === 'light'
        ? { background: '#eeeee8', grid: '#d9ddd2', outline: '#7e8c77', wall: '#d5dacb', accent: '#708421', particle: '#26372b', secondary: '#74806b', text: '#52604c', route: 'rgba(71,91,59,0.24)', accentRoute: 'rgba(112,132,33,0.28)' }
        : { background: '#181f1b', grid: '#29352d', outline: '#899681', wall: '#2c362e', accent: '#dfff00', particle: '#e0e6dd', secondary: '#a1ad9b', text: '#bdc8b4', route: 'rgba(209,222,202,0.22)', accentRoute: 'rgba(223,255,0,0.24)' };

      canvas.setAttribute('aria-hidden', 'true');
      if (this.button) {
        this.button.addEventListener('click', () => {
          this.manuallyToggled = true;
          this.running = !this.running;
          this.updateButton();
          syncAnimation();
        });
        this.updateButton();
      }
      canvas.addEventListener('pointermove', (event) => {
        if (!finePointer.matches || event.pointerType === 'touch') return;
        const rect = canvas.getBoundingClientRect();
        this.pointer.x = event.clientX - rect.left;
        this.pointer.y = event.clientY - rect.top;
        this.pointer.active = true;
      }, { passive: true });
      canvas.addEventListener('pointerleave', () => { this.pointer.active = false; });

      if ('ResizeObserver' in window) {
        this.resizeObserver = new ResizeObserver(() => this.resize());
        this.resizeObserver.observe(canvas);
      } else window.addEventListener('resize', () => this.resize(), { passive: true });
      if ('IntersectionObserver' in window) {
        this.visibilityObserver = new IntersectionObserver((entries) => {
          this.visible = entries[0].isIntersecting;
          syncAnimation();
        }, { rootMargin: '60px', threshold: 0 });
        this.visibilityObserver.observe(canvas);
      }
      mediaChange(motionPreference, () => {
        if (!this.manuallyToggled) this.running = !motionPreference.matches;
        this.pointer.active = false;
        this.updateButton();
        this.draw();
        syncAnimation();
      });
      this.resize();
      fields.push(this);
      syncAnimation();
    }

    random() {
      this.seed = (Math.imul(this.seed, 1664525) + 1013904223) >>> 0;
      return this.seed / 4294967296;
    }

    canAnimate() { return this.running && this.visible && this.width > 0 && this.height > 0; }

    updateButton() {
      if (!this.button) return;
      const label = this.running ? 'Pause motion' : 'Play motion';
      const text = this.button.querySelector('[data-flow-label]');
      if (text) text.textContent = label;
      else this.button.textContent = label;
      this.button.removeAttribute('aria-label');
      this.button.setAttribute('aria-pressed', String(this.running));
    }

    resize() {
      const rect = this.canvas.getBoundingClientRect();
      const width = Math.round(rect.width);
      const height = Math.round(rect.height);
      if (!width || !height) return;
      const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      if (width === this.width && height === this.height && this.dpr === dpr) return;
      this.width = width;
      this.height = height;
      this.dpr = dpr;
      this.canvas.width = Math.round(width * dpr);
      this.canvas.height = Math.round(height * dpr);
      this.context.setTransform(dpr, 0, 0, dpr, 0, 0);
      this.scale = Math.min(width / 700, height / 440);
      this.backdrop = null;
      this.obstacles = [
        [0.47, 0.055, 0.048, 0.31],
        [0.47, 0.47, 0.048, 0.06],
        [0.47, 0.635, 0.048, 0.31]
      ].map(([x, y, w, h]) => ({ x: x * width, y: y * height, w: w * width, h: h * height }));
      this.seed = 23821;
      const count = width < 500 ? 72 : 150;
      this.particles = Array.from({ length: count }, () => this.createParticle(true));
      this.draw();
      syncAnimation();
    }

    route(lane, offset, reverse, exitY) {
      const y = (lane ? 0.5825 : 0.4175) + offset;
      const startY = (lane ? 0.74 : 0.26) + offset * 5.0;
      const points = [];
      const cubic = (a, b, c, d, steps) => {
        for (let index = 0; index <= steps; index += 1) {
          const t = index / steps;
          const u = 1 - t;
          points.push({
            x: (u * u * u * a[0] + 3 * u * u * t * b[0] + 3 * u * t * t * c[0] + t * t * t * d[0]) * this.width,
            y: (u * u * u * a[1] + 3 * u * u * t * b[1] + 3 * u * t * t * c[1] + t * t * t * d[1]) * this.height
          });
        }
      };
      // Broad observation space contracts into two passages, then expands into the exits.
      cubic([-0.08, startY], [0.245, startY], [0.27, y], [0.445, y], 38);
      for (let index = 1; index <= 9; index += 1) {
        points.push({ x: (0.445 + 0.11 * index / 9) * this.width, y: y * this.height });
      }
      cubic([0.555, y], [0.755, y], [0.725, exitY], [1.08, exitY], 38);
      // Remove the shared segment endpoint before reversing a path.
      points.splice(48, 1);
      return reverse ? points.reverse() : points;
    }

    createParticle(initial) {
      const lane = this.random() > 0.5 ? 1 : 0;
      const offset = (this.random() - 0.5) * 0.082;
      const reverse = this.random() < 0.16;
      const exitY = (lane ? 0.75 : 0.25) + (this.random() - 0.5) * 0.40;
      const points = this.route(lane, offset, reverse, exitY);
      const particle = {
        points, index: 1, x: points[0].x, y: points[0].y,
        vx: 0, vy: 0, reverse, accent: this.random() < 0.28, phase: this.random() * Math.PI * 2,
        speed: (26 + this.random() * 15) * Math.max(0.65, this.scale),
        radius: (1.45 + this.random() * 0.65) * Math.max(0.75, this.scale),
        opacity: 0.65 + this.random() * 0.35
      };
      if (initial) {
        const lengths = points.slice(1).map((point, index) => Math.hypot(point.x - points[index].x, point.y - points[index].y));
        let distance = this.random() * lengths.reduce((total, length) => total + length, 0);
        for (let index = 0; index < lengths.length; index += 1) {
          if (distance <= lengths[index]) {
            const amount = distance / lengths[index];
            particle.x = points[index].x + (points[index + 1].x - points[index].x) * amount;
            particle.y = points[index].y + (points[index + 1].y - points[index].y) * amount;
            particle.index = index + 1;
            break;
          }
          distance -= lengths[index];
        }
      }
      const target = points[particle.index];
      const distance = Math.hypot(target.x - particle.x, target.y - particle.y) || 1;
      particle.vx = (target.x - particle.x) / distance * particle.speed;
      particle.vy = (target.y - particle.y) / distance * particle.speed;
      return particle;
    }

    advance(delta) {
      this.time += delta;
      const influence = Math.max(16, 28 * this.scale);
      this.particles.forEach((particle, index) => {
        let target = particle.points[particle.index];
        let dx = target.x - particle.x;
        let dy = target.y - particle.y;
        let distance = Math.hypot(dx, dy);
        if (distance < Math.max(5, particle.speed * delta * 2.5)) {
          particle.index += 1;
          if (particle.index >= particle.points.length) {
            this.particles[index] = this.createParticle(false);
            return;
          }
          target = particle.points[particle.index];
          dx = target.x - particle.x;
          dy = target.y - particle.y;
          distance = Math.hypot(dx, dy);
        }
        let desiredX = dx / (distance || 1) * particle.speed;
        let desiredY = dy / (distance || 1) * particle.speed;
        desiredY += Math.sin(this.time * 1.35 + particle.phase) * 1.0 * this.scale;

        this.obstacles.forEach((obstacle) => {
          const nearX = clamp(particle.x, obstacle.x, obstacle.x + obstacle.w);
          const nearY = clamp(particle.y, obstacle.y, obstacle.y + obstacle.h);
          const awayX = particle.x - nearX;
          const awayY = particle.y - nearY;
          const separation = Math.hypot(awayX, awayY);
          if (separation > 0 && separation < influence) {
            const force = (1 - separation / influence) * particle.speed * 1.4;
            desiredX += awayX / separation * force;
            desiredY += awayY / separation * force;
          }
        });

        if (this.pointer.active) {
          const awayX = particle.x - this.pointer.x;
          const awayY = particle.y - this.pointer.y;
          const separation = Math.hypot(awayX, awayY);
          const radius = 70 * Math.max(this.scale, 0.7);
          if (separation > 0 && separation < radius) {
            const force = (1 - separation / radius) * particle.speed * 0.48;
            desiredX += awayX / separation * force;
            desiredY += awayY / separation * force;
          }
        }
        const smooth = Math.min(1, delta * 4.2);
        particle.vx += (desiredX - particle.vx) * smooth;
        particle.vy += (desiredY - particle.vy) * smooth;
        particle.x += particle.vx * delta;
        particle.y += particle.vy * delta;

        // Hard boundaries keep the illustrative trajectories outside the solid plan geometry.
        this.obstacles.forEach((obstacle) => {
          const padding = particle.radius + 1;
          if (particle.x <= obstacle.x - padding || particle.x >= obstacle.x + obstacle.w + padding
            || particle.y <= obstacle.y - padding || particle.y >= obstacle.y + obstacle.h + padding) return;
          const edges = [
            { distance: Math.abs(particle.x - obstacle.x + padding), axis: 'x', value: obstacle.x - padding },
            { distance: Math.abs(particle.x - obstacle.x - obstacle.w - padding), axis: 'x', value: obstacle.x + obstacle.w + padding },
            { distance: Math.abs(particle.y - obstacle.y + padding), axis: 'y', value: obstacle.y - padding },
            { distance: Math.abs(particle.y - obstacle.y - obstacle.h - padding), axis: 'y', value: obstacle.y + obstacle.h + padding }
          ];
          const edge = edges.reduce((nearest, candidate) => candidate.distance < nearest.distance ? candidate : nearest);
          particle[edge.axis] = edge.value;
          if (edge.axis === 'x') particle.vx *= 0.4;
          else particle.vy *= 0.4;
        });
      });
    }

    draw() {
      if (!this.width || !this.height) return;
      const ctx = this.context;
      const width = this.width;
      const height = this.height;
      const colors = this.palette;
      ctx.globalAlpha = 1;
      if (this.backdrop) {
        ctx.drawImage(this.backdrop, 0, 0, width, height);
      } else {
      ctx.fillStyle = colors.background;
      ctx.fillRect(0, 0, width, height);

      const grid = Math.max(30, Math.round(Math.min(width, height) / 10));
      ctx.strokeStyle = colors.grid;
      ctx.lineWidth = 0.6;
      ctx.globalAlpha = 0.34;
      ctx.beginPath();
      for (let x = grid / 2; x < width; x += grid) { ctx.moveTo(x, 0); ctx.lineTo(x, height); }
      for (let y = grid / 2; y < height; y += grid) { ctx.moveTo(0, y); ctx.lineTo(width, y); }
      ctx.stroke();
      ctx.globalAlpha = 1;

      // Context lines establish a floor plan, with two legible passages through its spine.
      ctx.strokeStyle = colors.outline;
      ctx.lineWidth = 0.8;
      ctx.globalAlpha = 0.32;
      ctx.beginPath();
      ctx.moveTo(width * 0.045, height * 0.055);
      ctx.lineTo(width * 0.955, height * 0.055);
      ctx.moveTo(width * 0.045, height * 0.945);
      ctx.lineTo(width * 0.955, height * 0.945);
      ctx.stroke();
      ctx.globalAlpha = 1;

      ctx.lineWidth = Math.max(0.65, this.scale * 0.7);
      const routeCount = width < 500 ? 23 : 37;
      for (let lane = 0; lane < 2; lane += 1) {
        for (let index = 0; index < routeCount; index += 1) {
          const offset = (index / (routeCount - 1) - 0.5) * 0.082;
          const exitY = (lane ? 0.75 : 0.25) + offset * 5.0;
          const points = this.route(lane, offset, false, exitY);
          ctx.strokeStyle = index % 5 === 1 ? colors.accentRoute : colors.route;
          ctx.beginPath();
          ctx.moveTo(points[0].x, points[0].y);
          for (let i = 1; i < points.length; i += 1) ctx.lineTo(points[i].x, points[i].y);
          ctx.stroke();
        }
      }

      this.obstacles.forEach((obstacle) => {
        ctx.fillStyle = colors.wall;
        ctx.fillRect(obstacle.x, obstacle.y, obstacle.w, obstacle.h);
        ctx.strokeStyle = colors.outline;
        ctx.lineWidth = 0.8;
        ctx.strokeRect(obstacle.x + 0.5, obstacle.y + 0.5, obstacle.w - 1, obstacle.h - 1);
        // A single plan hatch makes the obstructions read as solid architectural objects.
        ctx.save();
        ctx.beginPath();
        ctx.rect(obstacle.x, obstacle.y, obstacle.w, obstacle.h);
        ctx.clip();
        ctx.globalAlpha = 0.42;
        ctx.beginPath();
        for (let x = obstacle.x - obstacle.h; x < obstacle.x + obstacle.w; x += 9) {
          ctx.moveTo(x, obstacle.y + obstacle.h);
          ctx.lineTo(x + obstacle.h, obstacle.y);
        }
        ctx.stroke();
        ctx.restore();
      });

      ctx.setLineDash([3, 4]);
      ctx.strokeStyle = colors.accent;
      ctx.globalAlpha = 0.68;
      ctx.lineWidth = 1;
      [0.365, 0.53].forEach((start) => {
        ctx.beginPath();
        ctx.moveTo(width * 0.494, height * start);
        ctx.lineTo(width * 0.494, height * (start + 0.105));
        ctx.stroke();
      });
      ctx.setLineDash([]);
      ctx.globalAlpha = 1;
      // The architectural plan and full curves are static; rasterise them only on resize.
      this.backdrop = document.createElement('canvas');
      this.backdrop.width = this.canvas.width;
      this.backdrop.height = this.canvas.height;
      const backdropContext = this.backdrop.getContext('2d', { alpha: false });
      if (backdropContext) backdropContext.drawImage(this.canvas, 0, 0);
      else this.backdrop = null;
      }

      this.particles.forEach((particle) => {
        const magnitude = Math.hypot(particle.vx, particle.vy) || 1;
        const length = 7 * Math.max(this.scale, 0.65);
        const color = particle.accent ? colors.accent : (particle.reverse ? colors.secondary : colors.particle);
        ctx.strokeStyle = color;
        ctx.fillStyle = color;
        ctx.globalAlpha = particle.opacity * 0.34;
        ctx.lineWidth = particle.radius * 0.85;
        ctx.beginPath();
        ctx.moveTo(particle.x - particle.vx / magnitude * length, particle.y - particle.vy / magnitude * length);
        ctx.lineTo(particle.x, particle.y);
        ctx.stroke();
        ctx.globalAlpha = particle.opacity;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.globalAlpha = 1;

      const fontSize = width < 420 ? 8 : 9;
      ctx.font = `${fontSize}px "Courier New", monospace`;
      ctx.fillStyle = colors.text;
      ctx.textBaseline = 'middle';
      ctx.textAlign = 'left';
      ctx.fillText('IN / 01', width * 0.045, height * 0.027);
      ctx.textAlign = 'right';
      ctx.fillText('OUT / 02', width * 0.955, height * 0.027);
      ctx.textAlign = 'left';
      ctx.fillText('A', width * 0.535, height * 0.365);
      ctx.fillText('B', width * 0.535, height * 0.635);
      ctx.fillText('PLAN — FLOW STUDY', width * 0.045, height * 0.974);
      ctx.textAlign = 'right';
      ctx.fillText('→', width * 0.955, height * 0.974);
    }
  }

  function init() {
    setupMenu();
    setupSectionNavigation();
    setupReveals();
    setupMagneticControls();
    document.querySelectorAll('canvas[data-flow-field]').forEach((canvas) => new FlowField(canvas));
    document.addEventListener('visibilitychange', syncAnimation);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
