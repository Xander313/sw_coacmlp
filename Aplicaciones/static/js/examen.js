document.addEventListener('DOMContentLoaded', function () {
    const checkbox = document.getElementById('examenS');
    const examenForm = document.querySelector('.examenForm');

    checkbox.addEventListener('change', function () {
        if (checkbox.checked) {
            examenForm.style.display = 'block';
        } else {
            examenForm.style.display = 'none';
        }
    });
});
