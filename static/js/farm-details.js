/* ============================================================
   Farm Details — soil selection, live validation, submit
   ============================================================ */

(function () {
  const form = document.getElementById('farmForm');
  const generateBtn = document.getElementById('generateBtn');
  const soilOptions = document.querySelectorAll('.soil-option');
  const soilInput = document.getElementById('soilTypeInput');
  const cropSelect = document.getElementById('cropSelect');
  const districtSelect = document.getElementById('districtSelect');
  const sowingDate = document.getElementById('sowingDate');

  // Cap sowing date to today (no future-sowing entries).
  sowingDate.max = new Date().toISOString().split('T')[0];

  soilOptions.forEach((btn) => {
    btn.addEventListener('click', () => {
      soilOptions.forEach((b) => b.setAttribute('aria-checked', 'false'));
      btn.setAttribute('aria-checked', 'true');
      soilInput.value = btn.dataset.soil;
      validate();
    });
  });

  [cropSelect, districtSelect, sowingDate].forEach((el) => {
    el.addEventListener('change', validate);
  });

  function validate() {
    const valid =
      cropSelect.value &&
      districtSelect.value &&
      soilInput.value &&
      sowingDate.value;
    generateBtn.disabled = !valid;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (generateBtn.disabled) return;

    generateBtn.disabled = true;
    const originalHTML = generateBtn.innerHTML;
    generateBtn.textContent = 'Generating…';

    const payload = {
      crop: cropSelect.value,
      district: districtSelect.value,
      soil_type: soilInput.value,
      sowing_date: sowingDate.value,
    };

    try {
      const res = await fetch('/farm-details', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (data.ok && data.redirect) {
        window.location.href = data.redirect;
      } else {
        throw new Error(data.error || 'Failed to generate plan');
      }
    } catch (err) {
      console.error(err);
      generateBtn.disabled = false;
      generateBtn.innerHTML = originalHTML;
      alert('Something went wrong. Please try again.');
    }
  });

  validate();
})();
