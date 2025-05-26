document.addEventListener("DOMContentLoaded", function () {
    const boton = document.getElementById("toggleContenidoBtn");
    const contenido = document.getElementById("contenidoExtra");
    const icono = document.getElementById("icono");


    if (boton) {
        boton.addEventListener("click", function () {
            contenido.classList.toggle("activo");

            if (contenido.classList.contains("activo")) {
                boton.firstChild.textContent = "Ocultar contenido extra ";
                icono.textContent = "keyboard_arrow_up";
            } else {
                boton.firstChild.textContent = "Mostrar contenido extra ";
                icono.textContent = "keyboard_arrow_down";
            }
        });
    }
});
