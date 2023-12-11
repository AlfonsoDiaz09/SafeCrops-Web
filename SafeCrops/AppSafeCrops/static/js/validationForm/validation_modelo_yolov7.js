/*
    Este es el archivo principal donde se hacen las validaciones de los formularios 
    antes de registrarlos en la base de datos, de esta forma se
    permite validar que cada input se encuentre lleno correctamente
*/

import notificationSweet2 from "./notificationSweet2.js";

// (Modelo YOLOv7) Importaciones de funciones en otros archivos JS
import validarFormularioModeloYOLOv7 from './formModeloYOLOv7/validarFormularioModeloYOLOv7.js';
import camposModeloYOLOv7 from './formModeloYOLOv7/campos.js';

// Declaración de constantes
const data_formulario = document.querySelector('[data-formulario-yolov7]');
const formulario = document.getElementById(`${data_formulario.id}`);
const inputs = document.querySelectorAll(`#${data_formulario.id} input`)
const selects = document.querySelectorAll(`#${data_formulario.id} select`)

// Obtener el nombre del id del formulario sin la palabra formulario y convertir la primer letra en mayuscula
var nombre = data_formulario.id.split('-')[1]
nombre = nombre.charAt(0).toUpperCase() + nombre.slice(1)

// Obtener el nombre con la acción de Crear o Editar
//formulario__editar-administrador
var accion = data_formulario.id.split('-')[0] // formulario__editar
accion = accion.split('__')[1] // editar
accion = accion.charAt(0).toUpperCase() + accion.slice(1) // Editar

var accionNombre = accion+'-'+nombre
console.log("Nombre del formulario: ")
console.log(nombre)

console.log("Nombre del accion: ")
console.log(accionNombre)


// Agregar eventos a cada input para ejecutar una función
inputs.forEach((input) => {
    console.log(input)
    input.addEventListener('keyup', (nombre=='ModeloYOLOv7') ? validarFormularioModeloYOLOv7 : ''); // Cuando se levanta la tecla
    input.addEventListener('blur', (nombre=='ModeloYOLOv7') ? validarFormularioModeloYOLOv7 : ''); // Cuando sale del input
    input.addEventListener('change', (nombre=='ModeloYOLOv7') ? validarFormularioModeloYOLOv7 : ''); // Cuando sale del input
    input.addEventListener('input', (nombre=='ModeloYOLOv7') ? validarFormularioModeloYOLOv7 : ''); // Cuando sale del input
});


// Agregar eventos a cada select para ejecutar una función
selects.forEach((select) => {
    select.addEventListener('click', (nombre=='ModeloYOLOv7') ? validarFormularioModeloYOLOv7 : ''); // Cuando da un click dentro del select
    select.addEventListener('change', (nombre=='ModeloYOLOv7') ? validarFormularioModeloYOLOv7 : ''); // Cuando se hace un cambio en la opción
    select.addEventListener('blur', (nombre=='ModeloYOLOv7') ? validarFormularioModeloYOLOv7 : ''); // Cuando sale del select
});

formulario.addEventListener('submit', (e) => {
    switch (accionNombre){
        case 'Crear-ModeloYOLOv7':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioModeloYOLOv7({target: input}) // {target: input} sirve para simular un evento
            });
            // Validar el formulario para cada select
            selects.forEach((select) => {
                validarFormularioModeloYOLOv7({target: select}) // {target: select} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposModeloYOLOv7)
            if((camposModeloYOLOv7.nombreModelo_y7 && camposModeloYOLOv7.datasetModelo_y7 && camposModeloYOLOv7.pesosModelo_y7 && camposModeloYOLOv7.epocas_y7 && camposModeloYOLOv7.batch_size_y7) == false){
                // Evitar que el formulario se envíe
                e.preventDefault();
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Modelo YOLOv7', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }else{
                // Muestra una notificación usando SweetAlert2
                const text = 'El proceso puede demorar un tiempo. Por favor no cierre esta ventana mientras termina el proceso. <br><br> Puede navegar en otra pestaña si lo desea.'
                Swal.fire({
                    title: 'Entrenando...',
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

            break
    }
});


