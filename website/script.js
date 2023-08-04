async function login() {
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
  
      // Perform any client-side validation you want here (e.g., check if fields are not empty).
      const resp2 = await fetch("http://127.0.0.1:8080/users/auth", {
          method: "POST",
          headers: {
              'Content-Type': 'application/json;charset=utf-8'
          },
          body: JSON.stringify({
              "email": email,
              "password": password
          })
      });
      let result = await resp2.json(); 
      if (resp2.ok){
            localStorage.setItem("Authorization", `${result.jwt}`);
            localStorage.setItem("user_id", `${result.user_id}`);
            localStorage.setItem("username", `${result.username}`);
  
            // For the sake of this example, let's just show a success message.
            document.getElementById('login-error').innerText = `Welcome, ${result.username}!`;
  
            // Redirect to the index.html page with the username as a query parameter.
            window.location.href = `index.html`;
  
            return false; // Prevent form submission
      }
      else{
            document.getElementById('login-error').innerText = `Error: ${result.reason}`;
            return false; // Prevent form submission
      }

  }
  

async function signUp() {
      const newUsername = document.getElementById('newUsername').value;
      const newEmail = document.getElementById('newEmail').value;
      const newPassword = document.getElementById('newPassword').value;

      // Perform any client-side validation you want here (e.g., check if fields are not empty).
      const resp = await fetch("http://127.0.0.1:8080/users", {
            method: "POST",
            headers: {
                  'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                  "username": newUsername,
                  "email": newEmail,
                  "password": newPassword
            })
      });
      let result = await resp.json();
      if (resp.ok){
            localStorage.setItem("Authorization",`${result.token}`);
            localStorage.setItem("user_id", `${result.user_id}`);
            localStorage.setItem("username", `${result.username}`);
            // For the sake of this example, let's just show a success message.
            document.getElementById(
                  'signup-success'
            ).innerText = `Account created for ${newUsername}!`;
            return false; // Prevent form submission
      }
      else {
            document.getElementById(
                  'signup-success'
            ).innerText = `Error: ${result.reason}`;
            return false; // Prevent form submission
      }
}

async function onMessage() {
      const message = document.getElementById("messageInput").value
      document.getElementById("messages").innerHTML += `<p class="user-message">${message}</p>`

      const resp = await fetch("http://127.0.0.1:8080/messages/",{
            method:"POST",
            headers:{
                  'Content-Type': 'application/json;charset=utf-8',
                  'Authorization': `Bearer ${localStorage.getItem("Authorization")}`
            
            },
            body:JSON.stringify({
                  "prompt":message,
            })
      });

      const result = await resp.json();
      if (resp.ok){
            document.getElementById("messages").innerHTML += `<p class="bot-message">${result.response}</p>`
      }
      else{
            document.getElementById("chat-error").innerText = result.reason
      }


}

const toggleDarkModeButton = document.getElementById('toggleDarkMode');
const pageContainer = document.getElementById('page-container');
let isDarkMode = localStorage.getItem('darkMode') === 'true'; // Load user preference

function toggleDarkMode() {
  isDarkMode = !isDarkMode;

  if (isDarkMode) {
    pageContainer.classList.add('dark-mode');
    localStorage.setItem('darkMode', 'true'); // Save user preference
  } else {
    pageContainer.classList.remove('dark-mode');
    localStorage.setItem('darkMode', 'false'); // Save user preference
  }
}

toggleDarkModeButton.addEventListener('click', toggleDarkMode);

// Initialize based on user preference
if (isDarkMode) {
  pageContainer.classList.add('dark-mode');
}
