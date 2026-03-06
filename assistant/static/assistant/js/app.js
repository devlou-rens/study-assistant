// ── INPUT TYPE TABS ──────────────────────────────────────────
function switchTab(type) {
  document.querySelectorAll('.input-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('[data-panel]').forEach(p => p.classList.add('hidden'));

  document.querySelector(`[data-tab="${type}"]`).classList.add('active');
  document.querySelector(`[data-panel="${type}"]`).classList.remove('hidden');
  document.getElementById('input_type').value = type;

  // Reset file input
  const fileInput = document.getElementById('file');
  if (fileInput) fileInput.value = '';
  const fileName = document.getElementById('file-name');
  if (fileName) fileName.textContent = '';
}

// ── FILE DROP ────────────────────────────────────────────────
function initFileDrop() {
  const drop = document.querySelector('.file-drop');
  if (!drop) return;

  const fileInput = document.getElementById('file');
  const fileNameEl = document.getElementById('file-name');

  fileInput.addEventListener('change', () => {
    const f = fileInput.files[0];
    if (f && fileNameEl) fileNameEl.textContent = `Selected: ${f.name}`;
  });

  ['dragover', 'dragleave', 'drop'].forEach(evt => {
    drop.addEventListener(evt, e => {
      e.preventDefault();
      if (evt === 'dragover') drop.classList.add('dragover');
      else drop.classList.remove('dragover');
      if (evt === 'drop' && e.dataTransfer.files[0]) {
        fileInput.files = e.dataTransfer.files;
        if (fileNameEl) fileNameEl.textContent = `Selected: ${e.dataTransfer.files[0].name}`;
      }
    });
  });
}

// ── FORM SUBMIT / LOADING ─────────────────────────────────────
function initForm() {
  const form = document.getElementById('study-form');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    const type = document.getElementById('input_type').value;

    if (type === 'text') {
      const txt = document.getElementById('text_content').value.trim();
      if (!txt) { e.preventDefault(); alert('Please enter some content to study.'); return; }
    } else {
      const file = document.getElementById('file').files[0];
      if (!file) { e.preventDefault(); alert('Please upload a file.'); return; }
    }

    const overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.classList.add('active');
  });
}

// ── FLASHCARD FLIP ───────────────────────────────────────────
function initFlashcards() {
  document.addEventListener('click', function(e) {
    const card = e.target.closest('.flashcard');
    if (card) card.classList.toggle('flipped');
  });
}

// ── FLASHCARD CONTROLS ────────────────────────────────────────
function revealAll() {
  document.querySelectorAll('.flashcard').forEach(c => c.classList.add('flipped'));
}

function resetAll() {
  document.querySelectorAll('.flashcard').forEach(c => c.classList.remove('flipped'));
}

// ── PRINT / COPY ──────────────────────────────────────────────
function copyReviewer() {
  const el = document.getElementById('reviewer-text');
  if (!el) return;
  navigator.clipboard.writeText(el.innerText).then(() => {
    const btn = document.getElementById('copy-btn');
    const orig = btn.textContent;
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = orig, 1500);
  });
}

// ── INIT ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initFileDrop();
  initForm();
  initFlashcards();
});
