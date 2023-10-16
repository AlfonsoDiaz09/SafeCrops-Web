/*
    En este archivo se hacen las validaciones de los formularios 
    antes de registrarlos en la base de datos, de esta forma se
    permite validar que cada input se encuentre lleno correctamente
*/

// Importanciones de funciones alojados en otros archivos JS
import validarFormularioDataset from "./formDataset/validarFormularioDataset.js";
import campos from "./formDataset/campos.js";
import notificationSweet2 from "./notificationSweet2.js";

// Declaración de constantes
const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input')
const selects = document.querySelectorAll('#formulario select')

// Agregar eventos a cada input para ejecutar una función
inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormularioDataset); // Cuando se levanta la tecla
    input.addEventListener('blur', validarFormularioDataset); // Cuando sale del input
    input.addEventListener('change', validarFormularioDataset); // Cuando sale del input
});

// Agregar eventos a cada select para ejecutar una función
selects.forEach((select) => {
    select.addEventListener('click', validarFormularioDataset); // Cuando da un click dentro del select
    select.addEventListener('change', validarFormularioDataset); // Cuando se hace un cambio en la opción
    select.addEventListener('blur', validarFormularioDataset); // Cuando sale del select
});

formulario.addEventListener('submit', (e) => {
    
    if(!(campos.nombreDataset && campos.ruta && campos.segmentacion_SAM && campos.formatoImg && campos.tipoDataset && campos.dentro_carpeta)){
        e.preventDefault(); // Evitar que el formulario se envíe

        // Mandar una alerta a la vista
        notificationSweet2('Campos Incompletos', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')

        // Validar el formulario para cada input
        inputs.forEach((input) => {
            validarFormularioDataset({target: input}) // {target: input} sirve para simular un evento
        });

        // Validar el formulario para cada select
        selects.forEach((select) => {
            validarFormularioDataset({target: select}) // {target: select} sirve para simular un evento
        });
    }else{
        // Muestra una notificación usando SweetAlert2
        const text = 'El proceso puede demorar un tiempo. Por favor no cierre esta ventana mientras termina el proceso. <br><br> Puede navegar en otra pestaña si lo desea.'
        Swal.fire({
            title: 'Cargando...',
            html: `<section class="talign-center"><img class="logoSweet2" src="../../../static/img/logoSafeCrops.png" width="70px" alt="logo"><div class="spinner icon-spinner-5" aria-hidden="true"></div><div class="textoSweet2">${text}</div></section>`,
            showConfirmButton: false,
            allowEscapeKey: false,
            allowOutsideClick: false,
            onOpen: () => {
                Swal.showLoading();
            }
        });

        // Agrega un evento para cerrar la notificación cuando la página se haya cargado
        window.addEventListener('load', function () {
            Swal.close(); // Cierra la notificación de carga
        });
    }

    
});


