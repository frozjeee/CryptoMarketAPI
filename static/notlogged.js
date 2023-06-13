document.addEventListener("DOMContentLoaded", function() {
if (!localStorage.getItem("token")) {
    // Redirect to the login page
    
    window.location.href = "http://localhost:8000/login";
  }
});