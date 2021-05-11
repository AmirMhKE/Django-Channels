const loginBtn = document.querySelector(".login .title")
const login = document.querySelector(".login")
const signupBtn = document.querySelector('.signup .title')
const signup = document.querySelector(".signup")
loginBtn.addEventListener('click', () => {
    login.classList.toggle("slide-up")
    signup.classList.toggle("slide-up")
});

signupBtn.addEventListener('click', () => {
    login.classList.toggle("slide-up")
    signup.classList.toggle("slide-up")
})

// validation
const loginBtnV = document.querySelector(".login button");
const signUpBtnV = document.querySelector(".signup button");

const usernameLogin = document.querySelector(".login input[name='username']");
const passwordLogin = document.querySelector(".login input[name='password']");

const usernameSignUp = document.querySelector(".signup input[name='username']");
const password1SignUp = document.querySelector(".signup input[name='password1']");
const password2SignUp = document.querySelector(".signup input[name='password2']");

var errorField = document.querySelector(".errors");

loginBtnV.addEventListener("click", (e) => {
    let usernameValue = usernameLogin.value.replaceAll(" ", "");
    let passwordValue = passwordLogin.value.replaceAll(" ", "");

    if(usernameValue === "" || passwordValue === "") {
        e.preventDefault();
        errorField.classList.add("alert-danger");
        errorField.innerHTML = "<ul><li>لطفا بخش های لازم رو پر کنید.</li></ul>";
    }
});

signUpBtnV.addEventListener("click", (e) => {
    let usernameValue = usernameSignUp.value.replaceAll(" ", "");
    let password1Value = password1SignUp.value.replaceAll(" ", "");
    let password2Value = password2SignUp.value.replaceAll(" ", "");

    if(usernameValue === "" || password1Value === "" || password2Value === "") {
        e.preventDefault();
        errorField.classList.add("alert-danger");
        errorField.innerHTML = "<ul><li>لطفا بخش های لازم رو پر کنید.</li></ul>";
    }
});