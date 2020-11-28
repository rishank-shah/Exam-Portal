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
	if(usernameValue.length>0){
		usernamevalidOut.textContent = `Checking Username ${usernameValue}`;
		fetch('/student/username-validate',{
			body: JSON.stringify({username:usernameValue}),
			method:"POST",
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
	if(emailVal.length>0){
		fetch('/student/email-validate',{
			body: JSON.stringify({ email: emailVal}),
			method: "POST",
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