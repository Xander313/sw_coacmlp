document.addEventListener('DOMContentLoaded', function () {
    const checkbox = document.getElementById('examenS');
    const examenForm = document.querySelector('.examenForm');
    let contadorPreguntas = 0;
    checkbox.addEventListener('change', function () {
        examenForm.style.display = checkbox.checked ? 'block' : 'none';
    });

    window.agregarPregunta = function () {
        const contenedor = document.getElementById("contenedorPreguntas");
        const nuevaPregunta = document.createElement("div");
        nuevaPregunta.className = "elementoPregunta";
        nuevaPregunta.dataset.index = contadorPreguntas;
        nuevaPregunta.innerHTML = `
            <label>Pregunta:</label>
            <input type="text" name="preguntas[${contadorPreguntas}][texto]" required>
            <span class="material-symbols-outlined delete-icon" onclick="eliminarElemento(this)">delete</span>
            <div class="respuestasContainer">
                ${generarRespuestaHTML(contadorPreguntas, 0)}
                ${generarRespuestaHTML(contadorPreguntas, 1)}
            </div>
            <button type="button" onclick="agregarRespuesta(this)">Nueva respuesta</button>
        `;
        contenedor.appendChild(nuevaPregunta);
        contadorPreguntas++;
        actualizarBotonesEliminar();
    }

    window.generarRespuestaHTML = function (preguntaIndex, respuestaIndex) {
        const requiredAttr = respuestaIndex === 0 ? 'required' : '';
        return `
            <div class="respuestaItem">
                <label>Respuesta:</label>
                <input type="text" name="preguntas[${preguntaIndex}][respuestas][]" required>
                <label>
                    <input type="radio" name="preguntas[${preguntaIndex}][respuesta_correcta]" value="${respuestaIndex}" ${requiredAttr}>
                    Correcta
                </label>
                <span class="material-symbols-outlined delete-icon" onclick="eliminarElemento(this)">delete</span>
            </div>
        `;
    }

    window.agregarRespuesta = function (boton) {
        const preguntaDiv = boton.closest(".elementoPregunta");
        const index = preguntaDiv.dataset.index;
        const respuestasContainer = preguntaDiv.querySelector(".respuestasContainer");
        const respuestaIndex = respuestasContainer.querySelectorAll(".respuestaItem").length;
        const nuevaRespuesta = document.createElement("div");
        nuevaRespuesta.className = "respuestaItem";
        nuevaRespuesta.innerHTML = `
            <label>Respuesta:</label>
            <input type="text" name="preguntas[${index}][respuestas][]" required>
            <label>
                <input type="radio" name="preguntas[${index}][respuesta_correcta]" value="${respuestaIndex}">
                Correcta
            </label>
            <span class="material-symbols-outlined delete-icon" onclick="eliminarElemento(this)">delete</span>
        `;
        respuestasContainer.appendChild(nuevaRespuesta);
        actualizarBotonesEliminar();
    }

    function actualizarBotonesEliminar() {
        const contenedor = document.getElementById("contenedorPreguntas");
        const preguntas = contenedor.querySelectorAll(".elementoPregunta");
        preguntas.forEach(pregunta => {
            const deletePreguntaBtn = pregunta.querySelector(":scope > .delete-icon");
            deletePreguntaBtn.style.display = (preguntas.length >= 2) ? "inline-block" : "none";
            const respuestas = pregunta.querySelectorAll(".respuestaItem");
            respuestas.forEach(respuesta => {
                const deleteRespuestaBtn = respuesta.querySelector(".delete-icon");
                deleteRespuestaBtn.style.display = (respuestas.length >= 3) ? "inline-block" : "none";
            });
        });
    }

    window.eliminarElemento = function (icono) {
        const respuestaItem = icono.closest(".respuestaItem");
        if (respuestaItem) {
            const respuestasContainer = respuestaItem.parentElement;
            const numRespuestas = respuestasContainer.querySelectorAll('.respuestaItem').length;
            if (numRespuestas > 2) {
                respuestaItem.remove();
                actualizarBotonesEliminar();
            } else {
                alert("Cada pregunta debe tener al menos 2 respuestas.");
            }
            return;
        }

        const preguntaItem = icono.closest(".elementoPregunta");
        if (preguntaItem) {
            const contenedor = document.getElementById("contenedorPreguntas");
            if (contenedor.querySelectorAll(".elementoPregunta").length > 1) {
                preguntaItem.remove();
                actualizarBotonesEliminar();
            } else {
                alert("Debe haber al menos 2 preguntas.");
            }
        }
    }
});
