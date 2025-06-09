document.addEventListener("DOMContentLoaded", () => {
    const boton2 = document.getElementById("botonAvance");

    if (!boton2) {
        console.log("No se encontró el botón 'botonAvance'");
        return;
    }

    if (boton2.classList.contains("aprobado")) {
        console.log("El capítulo ya está aprobado, no se aplica temporizador.");
        return;
    }

    const segundos = parseInt(boton2.dataset.activacion || "0");

    setTimeout(() => {
        console.log("¡Timeout ejecutado!");
        boton2.disabled = false;
        boton2.style.opacity = "1";

        boton2.addEventListener("click", () => {
            console.log("Botón clickeado, redirigiendo a:", boton2.dataset.url);
            window.location.href = boton2.dataset.url;
        });

        console.log("Botón activado después de", segundos, "segundos");
    }, segundos * 1000);

    const mensaje = document.getElementById("mensajeActivacion");
    const botonAvance = document.getElementById("botonAvance");
    if (!mensaje) return;

    let segundos1 = parseInt(botonAvance?.dataset.activacion || "0");
    if (isNaN(segundos1) || segundos1 <= 0) {
        mensaje.innerHTML = `<small>✅</small>`;
        return;
    }

    const intervalo = setInterval(() => {
        segundos1--;

        if (segundos1 > 0) {
            mensaje.innerHTML = `<small>${segundos1}⌚</small>`;
        } else {
            clearInterval(intervalo);
            mensaje.innerHTML = `<small>✅</small>`;
        }
    }, 1000);




});

