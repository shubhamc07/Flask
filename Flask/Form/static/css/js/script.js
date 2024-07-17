let form = document.getElementById("form");
let fullName = document.getElementById("fname");
let userName = document.getElementById("uname");
let email = document.getElementById("email");
let phoneNumber = document.getElementById("pnumber");
let password = document.getElementById("pass");
let confrimPassword = document.getElementById("cpass");
// let gender_btn = document.querySelector('input[name="gender"]:checked')

let fullName_error = document.getElementById("fname_error");
let userName_error = document.getElementById("uname_error");
let email_error = document.getElementById("email_error");
let phoneNumber_error = document.getElementById("pnumber_error");
let password_error = document.getElementById("pass_error");
let confrimPassword_error = document.getElementById("cpass_error");
let gender_error = document.getElementById("gen_error");

fullName.addEventListener("input", (e) => {
  // let name_check = /[^0-9]+/;
  let name_check = /[A-Za-z]$/;
  if (fullName.value === "" || fullName.value == null) {
    e.preventDefault();
    fullName_error.innerHTML = "*Fullname is required";
  } else if (!fullName.value.match(name_check)) {
    e.preventDefault();
    fullName_error.innerHTML = "*Not a valid input";
    fullName.value = "";
  } else {
    fullName_error.innerHTML = "";
  }
});

userName.addEventListener("input", (e) => {
  let user_check = /^[A-Za-z0-9]{1,9}$/;

  if (userName.value === "" || userName.value == null) {
    e.preventDefault();
    userName_error.innerHTML = "*Username is required";
  } else if (!userName.value.match(user_check)) {
    e.preventDefault();
    userName_error.innerHTML = "*Invalid username";
    userName.value = "";
  } else {
    userName_error.innerHTML = "";
  }
});

email.addEventListener("input", (e) => {
  let email_check =
    /^([A-Za-z0-9_\-\.])+@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

  if (!email.value.match(email_check)) {
    e.preventDefault();
    email_error.innerHTML = "*Enter a valid email id";
    // email.value="";
  } else {
    email_error.innerHTML = "";
  }
});

phoneNumber.addEventListener("input", (e) => {
  let num_check = /[0-9]{10}/;

  if (!phoneNumber.value.match(num_check)) {
    e.preventDefault();
    phoneNumber_error.innerHTML = "*Not a valid number";
    // phoneNumber.value="";
  } else {
    phoneNumber_error.innerHTML = "";
  }
});

password.addEventListener("input", (e) => {
  if (password.value.length <= 5) {
    e.preventDefault();
    password_error.innerHTML = "*Password must be more than 6 charecters";
  } else if (password.value.length >= 15) {
    e.preventDefault();
    password_error.innerHTML = "*Password canot be more than 15 charecters";
  } else if (password.value === "password") {
    e.preventDefault();
    password_error.innerHTML = "*Password canot be password";
  } else if (!password.value.match(passcheck)) {
    e.preventDefault();
    password_error.innerHTML =
      "*Must contain 6 characters, 1 uppercase, 1 lowercase, 1 number, and one special character";
    password.value = "";
  } else {
    password_error.innerHTML = "";
  }
});

confrimPassword.addEventListener("input", (e) => {
  if (confrimPassword.value != password.value) {
    e.preventDefault();
    confrimPassword_error.innerHTML =
      "*Confrim Password must match with password";
    confrimPassword.value = "";
  } else {
    confrimPassword_error.innerHTML = "";
  }
});

form.addEventListener("submit", (e) => {
  let name_check = /[A-Za-z]$/;
  let num_check = /[0-9]{10}/;
  let user_check = /^[A-Za-z0-9]{1,9}$/;
  let passcheck = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{6,15}$/;
  // e.preventDefault();
  let email_check =
    /^([A-Za-z0-9_\-\.])+@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

  if (fullName.value === "" || fullName.value == null) {
    e.preventDefault();
    fullName_error.innerHTML = "*Fullname is required";
  } else if (!fullName.value.match(name_check)) {
    e.preventDefault();
    fullName_error.innerHTML = "*Not a valid input";
  } else {
    fullName_error.innerHTML = "";
  }

  if (userName.value === "" || userName.value == null) {
    e.preventDefault();
    userName_error.innerHTML = "*Username is required";
  } else if (!userName.value.match(user_check)) {
    e.preventDefault();
    userName_error.innerHTML = "*Invalid username";
  } else {
    userName_error.innerHTML = "";
  }

  if (!phoneNumber.value.match(num_check)) {
    e.preventDefault();
    phoneNumber_error.innerHTML = "*Not a valid number";
  } else {
    phoneNumber_error.innerHTML = "";
  }

  if (!email.value.match(email_check)) {
    e.preventDefault();
    email_error.innerHTML = "*Enter a valid email id";
  } else {
    email_error.innerHTML = "";
  }

  if (password.value.length <= 5) {
    e.preventDefault();
    password_error.innerHTML = "*Password must be more than 6 charecters";
  } else if (password.value.length >= 15) {
    e.preventDefault();
    password_error.innerHTML = "*Password canot be more than 15 charecters";
  } else if (password.value === "password") {
    e.preventDefault();
    password_error.innerHTML = "*Password canot be password";
  } else if (!password.value.match(passcheck)) {
    e.preventDefault();
    password_error.innerHTML =
      "*Must contain 6 characters, 1 uppercase, 1 lowercase, 1 number, and one special character";
  } else {
    password_error.innerHTML = "";
  }

  if (confrimPassword.value != password.value) {
    e.preventDefault();
    confrimPassword_error.innerHTML =
      "*Confrim Password must match with password";
  } else {
    confrimPassword_error.innerHTML = "";
  }

  // if(!gender_btn){
  //     e.preventDefault();
  //     gender_error.innerHTML = "*Select your gender"
  // }
  // else{
  //     gender_error.innerHTML = "";
  // }
});
