
// ==============================
// AOS Animation
// ==============================

if (typeof AOS !== "undefined") {

    AOS.init({

        duration:800,

        easing:"ease-in-out",

        once:true

    });

}




// ==============================
// Category Swiper
// ==============================


if (typeof Swiper !== "undefined") {


const categorySwiper = new Swiper(".categorySwiper", {


    slidesPerView:2,

    spaceBetween:10,


    loop:true,


    autoplay:{


        delay:2500,

        disableOnInteraction:false


    },



    breakpoints:{


        1200:{

            slidesPerView:6,

            spaceBetween:20

        },



        992:{

            slidesPerView:5,

            spaceBetween:15

        },



        768:{

            slidesPerView:4,

            spaceBetween:15

        },



        576:{

            slidesPerView:3,

            spaceBetween:10

        },



        320:{

            slidesPerView:2,

            spaceBetween:10

        }


    }


});


}






// ==============================
// Hero Carousel
// ==============================


const heroCarousel = document.querySelector("#heroCarousel");


if(heroCarousel && typeof bootstrap !== "undefined"){


new bootstrap.Carousel(heroCarousel,{


    interval:3500,

    ride:"carousel",

    pause:false,

    wrap:true


});


}






// ==============================
// Product Hover Animation
// ==============================


document.querySelectorAll(".product-card").forEach(card=>{


card.addEventListener("mouseenter",()=>{


    card.style.transform="translateY(-8px)";

    card.style.transition=".3s";


});




card.addEventListener("mouseleave",()=>{


    card.style.transform="translateY(0)";


});



});






// ==============================
// Wishlist Toggle
// ==============================


function toggleFavorite(element){


const productId = element.dataset.productId;


const url = `/toggle_favorite/${productId}/`;



fetch(url,{


    method:"GET",


    headers:{


        "X-Requested-With":"XMLHttpRequest"


    }


})



.then(response=>response.json())



.then(data=>{


    if(data.is_favorite){


        element.classList.add("active");


    }


    else{


        element.classList.remove("active");


    }


})



.catch(error=>{


    console.error(
        "Favorite Error:",
        error
    );


});



}



window.toggleFavorite = toggleFavorite;







// ==============================
// Smooth Scroll
// ==============================


document.querySelectorAll('a[href^="#"]').forEach(anchor=>{


anchor.addEventListener("click",function(e){


    e.preventDefault();


    const target=document.querySelector(
        this.getAttribute("href")
    );



    if(target){


        target.scrollIntoView({

            behavior:"smooth"

        });


    }


});


});






// ==============================
// Back To Top
// ==============================


const backToTop=document.getElementById(
    "backToTop"
);



if(backToTop){


window.addEventListener("scroll",()=>{


    if(window.scrollY>300){


        backToTop.style.display="flex";


    }


    else{


        backToTop.style.display="none";


    }


});



backToTop.addEventListener("click",()=>{


window.scrollTo({


    top:0,

    behavior:"smooth"


});


});


}







// ==============================
// Fade Cards
// ==============================


window.addEventListener("load",()=>{


document.querySelectorAll(".product-card")
.forEach((card,index)=>{


setTimeout(()=>{


    card.classList.add("fade-up");


},index*80);



});


});







// ==============================
// Image Zoom
// ==============================


document.querySelectorAll(".product-img")
.forEach(img=>{


img.addEventListener("mouseenter",()=>{


    img.style.transform="scale(1.08)";


});



img.addEventListener("mouseleave",()=>{


    img.style.transform="scale(1)";


});


});
