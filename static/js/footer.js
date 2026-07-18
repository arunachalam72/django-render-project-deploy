
// =================================
// FOOTER SCROLL ANIMATION
// =================================


const footerItems =
document.querySelectorAll(".animate-footer");



if(footerItems.length > 0){


const footerObserver =
new IntersectionObserver(

(entries)=>{


entries.forEach(entry=>{


if(entry.isIntersecting){


entry.target.classList.add("show");


}


});


},

{

threshold:0.2

}

);




footerItems.forEach(item=>{


footerObserver.observe(item);


});


}









// =================================
// BACK TO TOP BUTTON
// =================================


const footerTop =
document.getElementById("footerTop");





if(footerTop){



window.addEventListener(
"scroll",
()=>{


if(window.scrollY > 400){


footerTop.style.display="flex";


}

else{


footerTop.style.display="none";


}


});







footerTop.addEventListener(
"click",
()=>{


window.scrollTo({

top:0,

behavior:"smooth"

});


});



}









// =================================
// NEWSLETTER BUTTON ANIMATION
// =================================


const newsletterButton =
document.querySelector(".newsletter button");




if(newsletterButton){


newsletterButton.addEventListener(
"click",
()=>{


newsletterButton.style.transform =
"scale(.85)";



setTimeout(()=>{


newsletterButton.style.transform =
"scale(1)";


},200);



});


}
