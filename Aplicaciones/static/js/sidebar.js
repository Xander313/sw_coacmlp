document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    const mainContent = document.getElementById('mainContent');

    if (!sidebar || !sidebarToggle || !closeSidebar || !mainContent) {
        console.error('No se encontraron los elementos del sidebar');
        return;
    }

    function openSidebar() {
        sidebar.classList.add('active');
        document.body.style.overflow = 'hidden';
        sidebarToggle.classList.add('hidden'); // Usa clase CSS
    }

    function closeSidebarFunc(e) {
        if (e) e.preventDefault();
        sidebar.classList.remove('active');
        document.body.style.overflow = 'auto';
        sidebarToggle.classList.remove('hidden');
    }

    sidebarToggle.addEventListener('click', openSidebar);
    closeSidebar.addEventListener('click', closeSidebarFunc);
    closeSidebar.addEventListener('touchstart', closeSidebarFunc); 

    // Cerrar al hacer clic fuera
    document.addEventListener('click', function(event) {
        const isMobile = window.innerWidth <= 992;
        const isSidebarOpen = sidebar.classList.contains('active');
        const clickedOutside = !sidebar.contains(event.target) && event.target !== sidebarToggle;
        
        if (isMobile && isSidebarOpen && clickedOutside) {
            closeSidebarFunc();
        }
    });

    mainContent.addEventListener('click', () => {
        if (sidebar.classList.contains('active')) {
            closeSidebarFunc(); 
        }
    });



    const sidebarElements = sidebar.querySelectorAll('a, button, li');
    sidebarElements.forEach(element => {
        element.addEventListener('click', () => {
            if (window.innerWidth <= 992 && sidebar.classList.contains('active')) {
                closeSidebarFunc();
            }
        });
    });

    document.querySelectorAll('.redirect-icon').forEach(icon => {
        icon.addEventListener('click', function () {
            window.location.href = "/administrarEducacion/administracion/";
        });
    });

});
