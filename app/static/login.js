const form = document.getElementById("loginForm");
const msg = document.getElementById("msg");

form.addEventListener("submit", async(e) =>{
    e.preventDefault();

    const formData = new FormData(form);
    const res = await fetch("/login", {method: "POST", body:formData});

    const data = await res.json();
    if (res.ok && data.redirect) {
        window.location.href = data.redirect;
        return;
    }
    else {
        msg.textContent = typeof data === "string" ? data : `Error: ${JSON.stringify(data)}`;
    }
    setTimeout(() => {
        msg.textContent = "";
    }, 3000);


});