/* ============================================================
   Dashboard — disease detection photo picker + preview
   Preview only; no upload wired yet.
   ============================================================ */

(function () {
  const takeBtn = document.getElementById('takePictureBtn');
  const input = document.getElementById('leafInput');
  const preview = document.getElementById('leafPreview');
  const previewImg = document.getElementById('leafPreviewImg');
  const clearBtn = document.getElementById('leafPreviewClear');

  if (!takeBtn || !input) return;

  let objectUrl = null;

  takeBtn.addEventListener('click', () => input.click());

  input.addEventListener('change', () => {
    const file = input.files && input.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      alert('Please choose an image file.');
      input.value = '';
      return;
    }

    releaseUrl();
    objectUrl = URL.createObjectURL(file);
    previewImg.src = objectUrl;
    preview.hidden = false;
    takeBtn.textContent = 'Choose a Different Photo';
  });

  clearBtn.addEventListener('click', () => {
    releaseUrl();
    previewImg.removeAttribute('src');
    preview.hidden = true;
    input.value = '';
    takeBtn.textContent = 'Take a Picture';
  });

  function releaseUrl() {
    if (objectUrl) {
      URL.revokeObjectURL(objectUrl);
      objectUrl = null;
    }
  }

  window.addEventListener('pagehide', releaseUrl);
})();
