// =================================
// MOBILE NAVBAR OPEN / CLOSE
// =================================

const mobileToggle = document.getElementById("mobileToggle");
const mobileClose = document.getElementById("mobileClose");
const navMenu = document.getElementById("navMenu");


if (mobileToggle && navMenu) {

    mobileToggle.addEventListener("click", () => {

        navMenu.classList.add("active");

    });

}


if (mobileClose && navMenu) {

    mobileClose.addEventListener("click", () => {

        navMenu.classList.remove("active");

    });

}



// =================================
// CLOSE MENU WHEN CLICKING LINK
// =================================

document.querySelectorAll(".nav-item, .login-btn, .profile-link")
.forEach(link => {


    link.addEventListener("click", () => {


        if(window.innerWidth <= 991 && navMenu){

            navMenu.classList.remove("active");

        }


    });


});



// =================================
// CLOSE MENU WHEN CLICK OUTSIDE
// =================================


document.addEventListener("click", function(event){


    if(!navMenu || !mobileToggle) return;


    const clickedInsideMenu =
    navMenu.contains(event.target);


    const clickedToggle =
    mobileToggle.contains(event.target);



    if(!clickedInsideMenu && !clickedToggle){

        navMenu.classList.remove("active");

    }


});




// =================================
// PRODUCT SEARCH SUGGESTIONS
// =================================


const searchInput =
document.getElementById("searchInput");


const suggestionsBox =
document.getElementById("suggestionsBox");



if(searchInput){


searchInput.addEventListener("keyup", function(){


    let query=this.value.trim();



    if(query.length < 2){

        suggestionsBox.innerHTML="";

        return;

    }



    fetch(`/search-suggestions/?q=${query}`)

    .then(response=>response.json())


    .then(data=>{


        suggestionsBox.innerHTML="";



        if(data.length===0){


            suggestionsBox.innerHTML=

            `<div class="p-3 text-center">
                No products found
             </div>`;

            return;

        }



        data.forEach(product=>{


            let url =
            productDetailUrl.replace(
                "0",
                product.id
            );



            let highlighted =
            product.name.replace(

                new RegExp(
                    `(${query})`,
                    "gi"
                ),

                "<strong>$1</strong>"

            );



            suggestionsBox.innerHTML += `

            <a href="${url}"
            class="suggestion-item">


                <img src="${product.image}"
                width="45"
                height="45"
                style="
                object-fit:cover;
                border-radius:8px;
                margin-right:12px;
                ">


                <div>

                    <div>
                    ${highlighted}
                    </div>


                    <small
                    style="color:#2874f0;font-weight:600">

                    ₹${product.price}

                    </small>


                </div>


            </a>

            `;


        });


    })


    .catch(error=>{

        console.log(
            "Search error:",
            error
        );

    });



});


}




// =================================
// CLOSE SEARCH DROPDOWN
// =================================


document.addEventListener("click",function(e){


if(!searchInput || !suggestionsBox)
return;



if(
!searchInput.contains(e.target)
&&
!suggestionsBox.contains(e.target)

){

    suggestionsBox.innerHTML="";

}


});




// =================================
// SEARCH ENTER KEY
// =================================


if(searchInput){


searchInput.addEventListener(
"keypress",
function(e){


    if(e.key==="Enter"){


        let value =
        searchInput.value.trim();



        if(value.length>0){


            window.location.href =
            `/search/?q=${value}`;


        }


    }


});


}



// =================================
// NAVBAR SHADOW ON SCROLL
// =================================


const navbar =
document.querySelector(".shop-navbar");



window.addEventListener("scroll",()=>{


if(!navbar)
return;



if(window.scrollY > 30){


    navbar.style.boxShadow =
    "0 8px 25px rgba(0,0,0,.15)";


}

else{


    navbar.style.boxShadow =
    "0 5px 20px rgba(0,0,0,.08)";


}


});