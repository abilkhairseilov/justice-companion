/* script.js
   Small helpers:
   - mobile menu toggle
   - accordion toggles
   - mock prediction calculation and update UI
   - accessible focus/aria updates
*/

document.addEventListener('DOMContentLoaded', () => {
  // --- mobile menu toggle ---
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      const expanded = mobileToggle.getAttribute('aria-expanded') === 'true';
      mobileToggle.setAttribute('aria-expanded', String(!expanded));
      const hidden = mobileMenu.getAttribute('aria-hidden') === 'true';
      mobileMenu.setAttribute('aria-hidden', String(!hidden));
      mobileMenu.style.display = hidden ? 'block' : 'none';
    });
  }

  // --- accordion ---
  document.querySelectorAll('.acc-item').forEach(button => {
    button.addEventListener('click', () => {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!expanded));

      // toggle panel next element
      const panel = button.nextElementSibling;
      if (!panel) return;
      panel.style.display = expanded ? 'none' : 'block';
      // also adjust the chevron (simple character swap)
      const chev = button.querySelector('.chev');
      if (chev) chev.textContent = expanded ? '▸' : '▾';
    });

    // initially collapse panels that are aria-expanded=false
    const panel = button.nextElementSibling;
    if (panel && button.getAttribute('aria-expanded') !== 'true') panel.style.display = 'none';
  });

  // --- mock prediction ---
  const form = document.getElementById('predict-form');
  const resultNumber = document.querySelector('.value-number');
  const resultText = document.getElementById('result-text');

  // simple mock model: base life expectancy 50 + (log GDP contribution) - (co2 * 0.6) - (childMort * 0.12)
  function mockPredict(gdp, co2, childMort) {
    // guard and transforms
    const g = Math.max(1, Number(gdp));
    const c = Math.max(0, Number(co2));
    const child = Math.max(0, Number(childMort));
    const gdpFactor = Math.log10(g + 1) * 6.5; // scaled
    let score = 50 + gdpFactor - (c * 0.6) - (child * 0.12);
    // clamp realistic range
    score = Math.max(25, Math.min(95, score));
    return Math.round(score * 10) / 10; // one decimal
  }

  if (form) {
    form.addEventListener('submit', (evt) => {
      evt.preventDefault();
      const gdp = form.querySelector('#gdp').value;
      const co2 = form.querySelector('#co2').value;
      const child = form.querySelector('#childMort').value;

      // basic validation
      if (!gdp || !co2 || !child) {
        resultText.textContent = 'Please complete all fields.';
        return;
      }

      const prediction = mockPredict(gdp, co2, child);
      resultNumber.textContent = prediction;
      resultText.textContent = `This projection suggests a life expectancy of ${prediction} years based on the provided metrics.`;
      resultNumber.parentElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }

  // --- small hover animation for chart bars (pure UI) ---
  document.querySelectorAll('.chart-svg .bar').forEach(bar => {
    bar.addEventListener('mouseenter', () => bar.style.transform = 'scaleY(1.03)');
    bar.addEventListener('mouseleave', () => bar.style.transform = 'scaleY(1)');
  });

  // set initial mobile menu display none for a11y
  if (mobileMenu) {
    mobileMenu.setAttribute('aria-hidden', 'true');
    mobileMenu.style.display = 'none';
  }
});