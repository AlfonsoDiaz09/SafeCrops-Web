function logout_redirect(){
    // Realiza un solicitud AJAX para cerrar la sesión en el servidor
    fetch('http://127.0.0.1:8000/logout/', {method : 'GET'})
    .then(response => {
        if(response.ok){
            // Redireccionar al usuario al inicio de sesión
            window.location.href = '/login';
        }else{
            console.error('No se pudo cerrar la sesión');
        }
    })
    .catch(error => {
        console.error('Error al cerrar la sesión: ', error);
    });
}

// Temporizador para cerrar la sesión despues de cierto tiempo de inactividad
let logoutTimer;

// Función para reiniciar el temporizador de cierre de sesión
function resetLogoutTimer(){
    clearTimeout(logoutTimer);
    logoutTimer = setTimeout(logout_redirect, 60000*15); // 15 min de inactividad (60,000 mls = 1 min)
}

// Registrar eventos para detectar la actividad del usuario
document.addEventListener('mousemove', resetLogoutTimer);
document.addEventListener('keypress', resetLogoutTimer);
document.addEventListener('load', resetLogoutTimer);

// Iniciar temporizador de cierre de sesión al cargar la página
resetLogoutTimer();
