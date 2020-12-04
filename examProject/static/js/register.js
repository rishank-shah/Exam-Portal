const passwordfield = document.querySelector('#passwordfield');
const usernamefield = document.querySelector('#usernamefield');
const emailfield = document.querySelector('#emailfield');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const emailfeedBack = document.querySelector('.email-feedback');
const feedBackField = document.querySelector('.invalid-feedback');
const usernamevalidOut = document.querySelector('.usernamevalidOut');

const handlePasswordToggle = (e) =>{
	if(showPasswordToggle.textContent=='SHOW'){
		showPasswordToggle.textContent = 'HIDE'
		passwordfield.setAttribute('type','text')
	}else{	
		showPasswordToggle.textContent = 'SHOW'
		passwordfield.setAttribute('type','password')
	}
}
showPasswordToggle.addEventListener('click',handlePasswordToggle);

usernamefield.addEventListener('keyup',(e)=>{
	usernameValue = e.target.value;
	usernamevalidOut.style.display = 'block';
	usernamefield.classList.remove('is-invalid');
	feedBackField.style.display = 'none';
	let headers = new Headers();
	if(usernameValue.length>0){
		usernamevalidOut.textContent = `Checking Username ${usernameValue}`;
		fetch('/student/username-validate',{
			body: JSON.stringify({username:usernameValue}),
			method:"POST",
			credentials: "same-origin",
			headers: {
				"X-CSRFToken": getCookie("csrftoken"),
				"Accept": "application/json",
				"Content-Type": "application/json"
			},
		})
		.then((res)=>res.json())
		.then(data=>{
			usernamevalidOut.style.display = 'none';
			if(data.username_error){
				usernamefield.classList.add('is-invalid');
				feedBackField.style.display = 'block';
				feedBackField.innerHTML = `<p>${data.username_error}</p>`
			}
		})
	}
})

emailfield.addEventListener('keyup',(e)=>{
	const emailVal = e.target.value;
	emailfield.classList.remove('is-invalid');
	emailfeedBack.style.display = 'none';
	let headers = new Headers();
	if(emailVal.length>0){
		fetch('/student/email-validate',{
			body: JSON.stringify({ email: emailVal}),
			method:"POST",
			credentials: "same-origin",
			headers: {
				"X-CSRFToken": getCookie("csrftoken"),
				"Accept": "application/json",
				"Content-Type": "application/json"
			},
		})
		.then((res)=>res.json())
		.then((data) => {
			if(data.email_error){
				emailfield.classList.add('is-invalid');
				emailfeedBack.style.display = 'block';
				emailfeedBack.innerHTML = `<p>${data.email_error}</p>`
			}
		})
	}
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}