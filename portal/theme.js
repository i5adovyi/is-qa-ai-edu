// Apply before the stylesheet loads to avoid a light flash on a dark visit.
// Appearance belongs to this browser, independently of the learning record.
(() => {
  'use strict';
  const key = 'ai-engineering-academy-theme';
  const choices = ['system', 'light', 'dark'];
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = 'system';
  let saveFailed = false;
  const valid = value => choices.includes(value) ? value : 'system';
  try { preference = valid(localStorage.getItem(key)); } catch (_) { /* Session-only is still usable. */ }

  function apply() {
    const theme = preference === 'system' ? (system.matches ? 'dark' : 'light') : preference;
    document.documentElement.dataset.theme = theme;
    const control = document.getElementById('theme-choice');
    if (control) control.value = preference;
    const status = document.getElementById('theme-status');
    if (status) {
      status.hidden = !saveFailed;
      status.textContent = saveFailed ? 'Theme changed for this tab; browser storage is unavailable.' : '';
    }
  }
  apply();
  system.addEventListener('change', apply);
  window.addEventListener('storage', event => {
    if (event.key === key || event.key === null) {
      preference = valid(event.newValue);
      saveFailed = false;
      apply();
    }
  });
  document.addEventListener('DOMContentLoaded', () => {
    apply();
    document.getElementById('theme-choice').addEventListener('change', event => {
      preference = valid(event.target.value);
      try {
        localStorage.setItem(key, preference);
        saveFailed = false;
      } catch (_) { saveFailed = true; }
      apply();
    });
  });
})();
