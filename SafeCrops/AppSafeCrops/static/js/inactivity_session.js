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
    setTimeout(logout_redirect, 60000*60); // 15 min de inactividad (60,000 mls = 1 min)
    logoutTimer = 60000*60;
}

// Función para actualizar el contador regresivo
function updateCountdown() {
    const countdownElement = document.getElementById('countdown');
    if (logoutTimer) {
        logoutTimer -= 1000;
        const minutos = Math.floor(logoutTimer / 60000); // 1 min = 60000 ms
        var segundos = Math.floor((logoutTimer % 60000) / 1000); // segundos restantes
        if (segundos >= 0 && segundos <= 9){
            segundos = `0${segundos}`;
        }
        countdownElement.textContent = `Cierre de sesión en ${minutos} : ${segundos}`;
    } else {
        countdownElement.textContent = '';
    }
}


// Registrar eventos para detectar la actividad del usuario
window.addEventListener('mousemove', resetLogoutTimer);
window.addEventListener('click', resetLogoutTimer);
window.addEventListener('keyup', resetLogoutTimer);
window.addEventListener('load', resetLogoutTimer);

// Iniciar temporizador de cierre de sesión al cargar la página
resetLogoutTimer();

// Actualizar el contador regresivo cada segundo
setInterval(updateCountdown, 1000)
