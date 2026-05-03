function getCarouselState(id) {
  const carousel = document.getElementById(id);
  const slides = [...carousel.querySelectorAll('.carousel-slide')];
  const dots = [...carousel.querySelectorAll('.dot')];
  const current = slides.findIndex(s => s.classList.contains('active'));
  return { carousel, slides, dots, current: current === -1 ? 0 : current };
}

function setCarouselSlide(id, index) {
  const { slides, dots } = getCarouselState(id);
  slides.forEach((s, i) => s.classList.toggle('active', i === index));
  dots.forEach((d, i) => d.classList.toggle('active', i === index));
}

function moveCarousel(id, direction) {
  const { slides, current } = getCarouselState(id);
  setCarouselSlide(id, (current + direction + slides.length) % slides.length);
}

function goToSlide(id, index) {
  setCarouselSlide(id, index);
}

// ─── Modal ───────────────────────────────────────────────────
const modal       = document.getElementById('gallery-modal');
const modalImg    = document.getElementById('modal-img');
const modalCap    = document.getElementById('modal-caption');
const modalDots   = document.getElementById('modal-dots');
const modalPrev   = document.getElementById('modal-prev');
const modalNext   = document.getElementById('modal-next');

let modalSlides = [];   // { src, alt } for current carousel/single
let modalIndex  = 0;
let sourceCarouselId = null;

function buildModalDots(count, active) {
  modalDots.innerHTML = '';
  if (count <= 1) return;
  for (let i = 0; i < count; i++) {
    const dot = document.createElement('span');
    dot.className = 'modal-dot' + (i === active ? ' active' : '');
    dot.onclick = () => goToModalSlide(i);
    modalDots.appendChild(dot);
  }
}

function goToModalSlide(index) {
  modalIndex = (index + modalSlides.length) % modalSlides.length;
  modalImg.src = modalSlides[modalIndex].src;
  modalImg.alt = modalSlides[modalIndex].alt;
  modalCap.textContent = modalSlides[modalIndex].alt;
  [...modalDots.querySelectorAll('.modal-dot')].forEach((d, i) =>
    d.classList.toggle('active', i === modalIndex)
  );
  // keep source carousel in sync
  if (sourceCarouselId) setCarouselSlide(sourceCarouselId, modalIndex);
}

function openModal(slides, startIndex, carouselId) {
  modalSlides = slides;
  modalIndex = startIndex;
  sourceCarouselId = carouselId || null;

  modalImg.src = slides[startIndex].src;
  modalImg.alt = slides[startIndex].alt;
  modalCap.textContent = slides[startIndex].alt;

  modalPrev.style.display = slides.length > 1 ? 'flex' : 'none';
  modalNext.style.display = slides.length > 1 ? 'flex' : 'none';
  buildModalDots(slides.length, startIndex);

  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  modal.classList.remove('open');
  document.body.style.overflow = '';
  modalImg.src = '';
}

// Wire prev/next
modalPrev.onclick = () => goToModalSlide(modalIndex - 1);
modalNext.onclick = () => goToModalSlide(modalIndex + 1);

// Close triggers
document.getElementById('modal-close').onclick = closeModal;
modal.addEventListener('click', e => { if (e.target === modal) closeModal(); });
document.addEventListener('keydown', e => {
  if (!modal.classList.contains('open')) return;
  if (e.key === 'Escape')      closeModal();
  if (e.key === 'ArrowLeft')   goToModalSlide(modalIndex - 1);
  if (e.key === 'ArrowRight')  goToModalSlide(modalIndex + 1);
});

// ─── Init on load ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Init first slide active for all carousels
  document.querySelectorAll('.gallery-carousel').forEach(carousel => {
    const slides = carousel.querySelectorAll('.carousel-slide');
    if (slides.length) slides[0].classList.add('active');
  });

  // Wire up carousel images → open modal with full carousel context
  document.querySelectorAll('.gallery-carousel').forEach(carousel => {
    const id = carousel.id;
    const slides = [...carousel.querySelectorAll('.carousel-slide')];
    const allSlides = slides.map(slide => {
      const img = slide.querySelector('img');
      return { src: img ? img.src : '', alt: img ? img.alt : '' };
    });

    slides.forEach((slide, i) => {
      const img = slide.querySelector('img');
      if (img) img.addEventListener('click', () => openModal(allSlides, i, id));
    });
  });

  // Wire up single images → open modal with just that image
  document.querySelectorAll('.gallery-single img').forEach(img => {
    img.addEventListener('click', () =>
      openModal([{ src: img.src, alt: img.alt }], 0, null)
    );
  });
});