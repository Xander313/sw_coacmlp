document.addEventListener('DOMContentLoaded', function () {
    const checkbox = document.getElementById('examenS');
    const examenForm = document.querySelector('.examenForm');
    const wrapper = document.querySelector(".wrapper"); // Asegúrate de tener este contenedor en tu HTML
    let contadorPreguntas = 0;

        // Muestra u oculta el formulario del examen
    let preguntaAgregada = false; // bandera global

    function toggleExamenForm() {
        if (checkbox.checked) {
            examenForm.style.display = 'block';
            wrapper?.classList.add('doble-columna');

            // Ejecutar agregarPregunta() solo una vez
            if (!preguntaAgregada) {
                agregarPregunta();
                preguntaAgregada = true;
            }

            examenForm.querySelectorAll("input, textarea").forEach(el => {
                if (el.dataset.originalRequired === "true") {
                    el.required = true;
                }
            });
        } else {
            examenForm.style.display = 'none';
            wrapper?.classList.remove('doble-columna');

            examenForm.querySelectorAll("input, textarea").forEach(el => {
                el.dataset.originalRequired = el.required;
                el.required = false;
            });
        }
    }


    checkbox.addEventListener("change", toggleExamenForm);
    toggleExamenForm(); // Inicializa al cargar

    // Función para generar el HTML de una respuesta
    window.generarRespuestaHTML = function (preguntaIndex, respuestaIndex) {
        const requiredAttr = respuestaIndex === 0 ? 'required' : '';
        return `
            <div class="respuestaItemExamen">
                <label>Respuesta:</label>
                <input type="text" name="preguntas[${preguntaIndex}][respuestas][]" ${requiredAttr}>
                <label>
                    <input type="radio" name="preguntas[${preguntaIndex}][respuesta_correcta]" value="${respuestaIndex}" ${requiredAttr}>
                </label>
                <span class="material-symbols-outlined delete-icon" onclick="eliminarElemento(this)">delete</span>
            </div>
        `;
    };

    // Agrega una nueva pregunta
    window.agregarPregunta = function () {
        const contenedor = document.getElementById("contenedorPreguntas");
        const nuevaPregunta = document.createElement("div");
        nuevaPregunta.className = "elementoPregunta";
        nuevaPregunta.dataset.index = contadorPreguntas;

        nuevaPregunta.innerHTML = `
            <div class="preguntaLinea">
                <label>Pregunta:</label>
                <input type="text" name="preguntas[${contadorPreguntas}][texto]" required>
                <span class="material-symbols-outlined delete-icon" onclick="eliminarElemento(this)">delete</span>
            </div>
            <div class="respuestasContainer">
                ${generarRespuestaHTML(contadorPreguntas, 0)}
                ${generarRespuestaHTML(contadorPreguntas, 1)}
            </div>
            <button type="button" class="botonAgregar botonAgregarNuevaRespuesta" onclick="agregarRespuesta(this)"> <span class="material-symbols-outlined">add</span> Nueva respuesta</button>
        `;

        contenedor.appendChild(nuevaPregunta);
        contadorPreguntas++;
        actualizarBotonesEliminar();
    };

    // Agrega una nueva respuesta a una pregunta específica
    window.agregarRespuesta = function (boton) {
        const preguntaDiv = boton.closest(".elementoPregunta");
        const index = preguntaDiv.dataset.index;
        const respuestasContainer = preguntaDiv.querySelector(".respuestasContainer");
        const respuestaIndex = respuestasContainer.querySelectorAll(".respuestaItemExamen").length;

        const nuevaRespuesta = document.createElement("div");
        nuevaRespuesta.innerHTML = generarRespuestaHTML(index, respuestaIndex);
        respuestasContainer.appendChild(nuevaRespuesta.firstElementChild);

        actualizarBotonesEliminar();
    };

    // Reindexa los radio buttons tras eliminar una respuesta
    function reindexarRespuestas(preguntaDiv) {
        const respuestas = preguntaDiv.querySelectorAll(".respuestaItemExamen");
        respuestas.forEach((respuesta, i) => {
            const inputRadio = respuesta.querySelector("input[type=radio]");
            inputRadio.value = i;
        });
    }

    // Actualiza la visibilidad de los botones de eliminar
    function actualizarBotonesEliminar() {
        const contenedor = document.getElementById("contenedorPreguntas");
        const preguntas = contenedor.querySelectorAll(".elementoPregunta");

        preguntas.forEach(pregunta => {
            const deletePreguntaBtn = pregunta.querySelector(".preguntaLinea .delete-icon");
            deletePreguntaBtn.style.display = (preguntas.length >= 2) ? "inline-block" : "none";

            const respuestas = pregunta.querySelectorAll(".respuestaItemExamen");
            respuestas.forEach(respuesta => {
                const deleteRespuestaBtn = respuesta.querySelector(".delete-icon");
                deleteRespuestaBtn.style.display = (respuestas.length >= 3) ? "inline-block" : "none";
            });
        });
    }

    // Elimina una pregunta o una respuesta
    window.eliminarElemento = function (icono) {
        const respuestaItem = icono.closest(".respuestaItemExamen");
        if (respuestaItem) {
            const respuestasContainer = respuestaItem.parentElement;
            const numRespuestas = respuestasContainer.querySelectorAll('.respuestaItemExamen').length;
            if (numRespuestas > 2) {
                const preguntaDiv = respuestaItem.closest(".elementoPregunta");
                respuestaItem.remove();
                reindexarRespuestas(preguntaDiv);
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
    };

});
