function login() {
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;

      // Perform any client-side validation you want here (e.g., check if fields are not empty).

      // For the sake of this example, let's just show a success message.
      document.getElementById('login-error').innerText = `Welcome, ${username}!`;

      // Redirect to the index.html page with the username as a query parameter.
      window.location.href = `index.html?username=${encodeURIComponent(username)}`;

      return false; // Prevent form submission
}

function signUp() {
      const newUsername = document.getElementById('newUsername').value
      const newPassword = document.getElementById('newPassword').value

      // Perform any client-side validation you want here (e.g., check if fields are not empty).

      // For the sake of this example, let's just show a success message.
      document.getElementById(
            'signup-success'
      ).innerText = `Account created for ${newUsername}!`
      return false // Prevent form submission
}
