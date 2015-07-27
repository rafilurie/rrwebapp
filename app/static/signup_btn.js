window.onload = function() {
    
    var COLOR = '#6D6D6D';
    var SIGNUP = 1;
    var LOGIN = 2;
    clickedBtn = SIGNUP;

    document.getElementById("signup-btn").onclick = function() {
        clickedBtn = SIGNUP;
        window.location.href='/welcome';
    }

    document.getElementById("login-btn").onclick = function() {
        clickedBtn = LOGIN;
        window.location.href='/welcome/login';
    }

    document.getElementById("signup-btn").onmouseover = function() {
        this.style.backgroundColor = COLOR;
        this.style.color = "white";
        document.getElementById("login-btn").style.backgroundColor = "white";
        document.getElementById("login-btn").style.color = COLOR;
    }

    document.getElementById("login-btn").onmouseover = function() {
        this.style.backgroundColor = COLOR;
        this.style.color = "white";
        document.getElementById("signup-btn").style.backgroundColor = "white";
        document.getElementById("signup-btn").style.color = COLOR;
    }

    document.getElementById("signup-btn").onmouseout = function() {
        if (clickedBtn == SIGNUP) {
            this.style.backgroundColor = COLOR;
            this.style.color = "white";
            document.getElementById("login-btn").style.backgroundColor = "white";
            document.getElementById("login-btn").style.color = COLOR;
        } else {
            this.style.backgroundColor = "white";
            this.style.color = COLOR;
            document.getElementById("login-btn").style.backgroundColor = COLOR;
            document.getElementById("login-btn").style.color = "white";
        }
    }

    document.getElementById("login-btn").onmouseout = function() {
        if (clickedBtn == LOGIN) {
            this.style.backgroundColor = COLOR;
            this.style.color = "white";
            document.getElementById("signup-btn").style.backgroundColor = "white";
            document.getElementById("signup-btn").style.color = COLOR;
        } else {
            this.style.backgroundColor = "white";
            this.style.color = COLOR;
            document.getElementById("signup-btn").style.backgroundColor = COLOR;
            document.getElementById("signup-btn").style.color = "white";
        }
    }
}