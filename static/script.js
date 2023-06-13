document.addEventListener("DOMContentLoaded", function() {
    // Check if the token exists in localStorage
    var token = localStorage.getItem("token");
    if (token) {
       // Retrieve the token from localStorage
        var logout = document.getElementById("logout");
        if (logout){
          logout.style.display = "inline";
          logout.style.cursor = "pointer";
          logout.style.marginLeft = "10px";
        }
        var token = localStorage.getItem("token");

        // Decode the JWT token to access the "name" claim
        var base64Url = token.split(".")[1];
        var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        var jsonPayload = decodeURIComponent(atob(base64).split("").map(function(c) {
            return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(""));

        var name = JSON.parse(jsonPayload).name;

        // Update the username in the UI
        var signUpButton = document.querySelector(".btn.btn-sm.btn-outline-secondary");
        signUpButton.style.display = "none"; // Hide the sign-up button

        var usernameElement = document.createElement("a");
        usernameElement.textContent = name;
        usernameElement.href = "http://localhost:8000/view/user"
        usernameElement.style.color = "black";
        signUpButton.parentNode.insertBefore(usernameElement, signUpButton);
    }
 });
