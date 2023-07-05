if (window.location.pathname == "/login") {
  document.querySelector(".container").classList.toggle("sign-up");
} else if (window.location.pathname == "/register") {
  document.querySelector(".container").classList.toggle("log-in");
}

document.querySelectorAll(".info-item .btn").forEach(function (btn) {
  btn.addEventListener("click", function () {
    // toggle the class "log-in" on an element with class "container"
    document.querySelector(".container").classList.toggle("log-in");
  });
});



// if form submit button is clicked
// document.querySelector(".form").addEventListener("submit", function (e) {
//   // prevent the default action of the form
//   e.preventDefault();
//   // when a button with class "btn" is clicked inside an element with class "container-form"
//   document.querySelectorAll(".container-form .btn").forEach(function (btn) {
//     btn.addEventListener("click", function () {
//       // add the class "active" to an element with class "container"
//       document.querySelector(".container").classList.add("active");
//     });
//   });
// });
