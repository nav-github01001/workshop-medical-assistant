function login() {
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      // Perform any client-side validation you want here (e.g., check if fields are not empty).
      const resp2 = fetch("http://127.0.0.1:8080/users/auth", {
            method: "POST",
            mode: "no-cors",
            headers: {
                  'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                  "email": email,
                  "password": password
            })
      });
      resp2.then(response => response.json()).catch(error => console.error(error));
      if (response.status === 401) {
            document.getElementById('login-error').textContent = "Invalid Password";
            return false; // Prevent form submission
      }

      sessionStorage.setItem("Authorization",response.token);

      // For the sake of this example, let's just show a success message.
      document.getElementById('login-error').textContent = `Welcome, ${response.username}!`;


      // Redirect to the index.html page with the username as a query parameter.
      window.location.href = `index.html?username=${encodeURIComponent(username)}`;

      return false; // Prevent form submission
}
function signUp() {
      const newUsername = document.getElementById('newUsername').value
      const newEmail = document.getElementById('newEmail').value
      const newPassword = document.getElementById('newPassword').value

      // Perform any client-side validation you want here (e.g., check if fields are not empty).
      const resp = fetch("http://127.0.0.1:8080/users", {
            method: "POST",
            mode: "no-cors",
            headers: {
                  'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                  "username": newUsername,
                  "email": newEmail,
                  "password": newPassword
            })
      });
      resp.then(response => response.json()).catch(error => console.error(error))
      //if (error != 201){
      //      document.getElementById(
      //            'signup-success'
      //      ).innerText = response.reason;
      //      return false;
      //};
      sessionStorage.setItem("Authorization",response.token);
      // For the sake of this example, let's just show a success message.
      document.getElementById(
            'signup-success'
      ).innerText = `Account created for ${newUsername}!`;
      return false; // Prevent form submission
}

function onMessage() {
      const message = document.getElementById("messageInput").value

      const resp = fetch("http://127.0.0.1:8080/messages",{
            method:"POST",
            mode:"no-cors",
            headers:{
                  'Content-Type': 'application/json;charset=utf-8',
                  'Authorization': `Bearer ${sessionStorage.getItem("Authorization")}`
            
            },
            body:JSON.stringify({
                  "prompt":message,
            })
      });
      

}

const toggleDarkModeButton = document.getElementById('toggleDarkMode');
const pageContainer = document.getElementById('page-container');
let isDarkMode = false;

function toggleDarkMode() {
  isDarkMode = !isDarkMode;

  if (isDarkMode) {
    pageContainer.classList.add('dark-mode');
  } else {
    pageContainer.classList.remove('dark-mode');
  }
}

toggleDarkModeButton.addEventListener('click', toggleDarkMode);
