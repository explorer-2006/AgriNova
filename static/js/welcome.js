/* ============================================================
   Welcome Screen — language selection
   Talks to Flask via POST /set-language
   ============================================================ */

(function () {
  const root = document.querySelector(".welcome");
  const cards = document.querySelectorAll(".lang-card");
  const continueBtn = document.getElementById("continueBtn");

  let selectedLang = root.dataset.currentLang || null;

  // Restore prior selection if server sent one.
  if (selectedLang) {
    applySelection(selectedLang);
  }

  cards.forEach((card) => {
    card.addEventListener("click", () => {
      selectedLang = card.dataset.lang;
      applySelection(selectedLang);
    });
  });

  continueBtn.addEventListener("click", async () => {
    if (!selectedLang || continueBtn.disabled) return;

    continueBtn.disabled = true;
    continueBtn.textContent = "Please wait…";

    try {
      const res = await fetch("/set-language", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lang: selectedLang }),
      });
      const data = await res.json();
      if (data.ok && data.redirect) {
        window.location.href = data.redirect;
      } else {
        throw new Error(data.error || "Failed to save language");
      }
    } catch (err) {
      console.error(err);
      continueBtn.disabled = false;
      continueBtn.textContent = "Continue";
      alert("Something went wrong. Please try again.");
    }
  });

  function applySelection(lang) {
    cards.forEach((c) => {
      const isSel = c.dataset.lang === lang;
      c.setAttribute("aria-checked", isSel ? "true" : "false");
    });
    continueBtn.disabled = false;
  }
})();
