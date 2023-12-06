// script.js

// This code ensures that the JavaScript runs only after the HTML document has fully loaded.
$(document).ready(function () {

    // Add an event listener to the form submission
    $('#signin-form').submit(function (event) {

        // Prevent the default form submission behavior
        event.preventDefault();

        // Get the values of username and password inputs
        var username = $('#username').val();
        var password = $('#password').val();

        // Show an alert with the entered username and password
        alert('Username: ' + username + '\nPassword: ' + password);
    });

    // Add an event listener to the Sign-in button
    $('button[type="submit"]').click(function () {

        // Show a different alert when the button is clicked
        alert('Sign-in button clicked!');
    });
});
