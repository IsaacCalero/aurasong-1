document.addEventListener("DOMContentLoaded", () => {
  const carouselImages = document.querySelector(".carousel-images");
  const images = document.querySelectorAll(".carousel-images img");
  const prevBtn = document.querySelector(".prev");
  const nextBtn = document.querySelector(".next");

  let counter = 0;
  const size = images[0].clientWidth;

  function updateCarousel() {
    carouselImages.style.transform = `translateX(${-size * counter}px)`;
  }

  nextBtn.addEventListener("click", () => {
    if (counter >= images.length - 1) {
      counter = 0;
    } else {
      counter++;
    }
    updateCarousel();
  });

  prevBtn.addEventListener("click", () => {
    if (counter <= 0) {
      counter = images.length - 1;
    } else {
      counter--;
    }
    updateCarousel();
  });

  updateCarousel();
});
