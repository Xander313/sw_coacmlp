function confirmCreate(formElement) {
    Swal.fire({
        title: "CONFIRMACIÓN",
        text: "¿Está seguro que desea agregar este capítulo?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, agregar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            formElement.submit();
        }
    });
}

function confirmUpdate(formElement) {
    Swal.fire({
        title: "CONFIRMACIÓN",
        text: "¿Está seguro que desea editar este capítulo? Esta acción es irreversible.",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, editar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            formElement.submit();
        }
    });
}

function confirmDelete(id) {
    Swal.fire({
        title: "CONFIRMACIÓN",
        text: "¿Está seguro de eliminar este capítulo? Esta acción es irreversible.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/administrarEducacion/ejecutareliminacionCapitulo/" + id;
        }
    });
}

// 👇 TODO DENTRO DE UN SOLO DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    // Botón de creación
    const boton = document.getElementById('botonConfirmar');
    if (boton) {
        const formulario = boton.closest('form');
        boton.addEventListener('click', (e) => {
            e.preventDefault();
            if (formulario.checkValidity()) {
                confirmCreate(formulario);
            } else {
                formulario.reportValidity();
            }
        });
    }

    // Botón de edición
    const botonActualizar = document.getElementById('botonEditar');
    if (botonActualizar) {
        const formUpdate = botonActualizar.closest('form');
        botonActualizar.addEventListener('click', (e) => {
            e.preventDefault();
            if (formUpdate.checkValidity()) {
                confirmUpdate(formUpdate);
            } else {
                formUpdate.reportValidity();
            }
        });
    }

    // Botones de eliminación
    document.querySelectorAll('.btn-eliminar').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const id = btn.dataset.id;
            confirmDelete(id);
        });
    });
});

