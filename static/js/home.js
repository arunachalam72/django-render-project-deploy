// ==============================
// AOS Animation
// ==============================

AOS.init({
    duration: 800,
    easing: "ease-in-out",
    once: true
});


// ==============================
// Category Swiper
// ==============================

const categorySwiper = new Swiper(".categorySwiper", {

    slidesPerView: 6,

    spaceBetween: 20,

    loop: true,

    autoplay: {

        delay: 2500,

        disableOnInteraction: false,

    },

    pagination: {

        el: ".swiper-pagination",

        clickable: true,

    },

    breakpoints: {

        1200: {
            slidesPerView: 6
        },

        992: {
            slidesPerView: 5
        },

        768: {
            slidesPerView: 4
        },

        576: {
            slidesPerView: 3
        },

        320: {
            slidesPerView: 2
        }

    }

});


// ==============================
// Hero Carousel Auto
// ==============================

const heroCarousel = document.querySelector("#heroCarousel");

if (heroCarousel) {

    new bootstrap.Carousel(heroCarousel, {

        interval: 3500,

        ride: "carousel",

        pause: false,

        wrap: true

    });

}


// ==============================
// Product Hover Effect
// ==============================

document.querySelectorAll(".product-card").forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-8px)";

        card.style.transition = ".3s";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0px)";

    });

});


// ==============================
// Wishlist Toggle
// ==============================

function toggleFavorite(element) {

    const productId = element.dataset.productId;

    const url = `/toggle_favorite/${productId}/`;

    fetch(url, {

        method: "GET",

        headers: {

            "X-Requested-With": "XMLHttpRequest"

        }

    })

    .then(response => response.json())

    .then(data => {

        if (data.is_favorite) {

            element.classList.add("active");

        } else {

            element.classList.remove("active");

        }

    })

    .catch(error => {

        console.error("Favorite Error:", error);

    });

}


// Make available globally because onclick calls it
window.toggleFavorite = toggleFavorite;


// ==============================
// Smooth Scroll
// ==============================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function(e) {

        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {

            target.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});


// ==============================
// Back To Top Button
// (Requires an element with id="backToTop")
// ==============================

const backToTop = document.getElementById("backToTop");

window.addEventListener("scroll", () => {

    if (!backToTop) return;

    if (window.scrollY > 300) {

        backToTop.style.display = "flex";

    } else {

        backToTop.style.display = "none";

    }

});

if (backToTop) {

    backToTop.addEventListener("click", () => {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

}


// ==============================
// Fade-in Cards on Load
// ==============================

window.addEventListener("load", () => {

    document.querySelectorAll(".product-card").forEach((card, index) => {

        setTimeout(() => {

            card.classList.add("fade-up");

        }, index * 80);

    });

});


// ==============================
// Optional Image Zoom
// ==============================

document.querySelectorAll(".product-card img").forEach(img => {

    img.addEventListener("mouseenter", () => {

        img.style.transform = "scale(1.08)";

    });

    img.addEventListener("mouseleave", () => {

        img.style.transform = "scale(1)";

    });

});