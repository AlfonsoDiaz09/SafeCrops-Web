/*
    Este es el archivo principal donde se hacen las validaciones de los formularios 
    antes de registrarlos en la base de datos, de esta forma se
    permite validar que cada input se encuentre lleno correctamente
*/

import notificationSweet2 from "./notificationSweet2.js";

// (Dataset) Importaciones de funciones alojados en otros archivos JS
import validarFormularioDataset from './formDataset/validarFormularioDataset.js';
import camposDataset from './formDataset/campos.js';

// (Administrador) Importaciones de funciones alojados en otros archivos JS
import validarFormularioAdministrador from './formAdministrador/validarFormularioAdministrador.js';
import camposAdmin from "./formAdministrador/campos.js";

// (Experto) Importaciones de funciones en otros archivos JS
import validarFormularioExperto from "./formExperto/validarFormularioExperto.js";
import camposExperto from './formExperto/campos.js'

// (Tester) Importaciones de funciones en otros archivos JS
import validarFormularioTester from './formTester/validarFormularioTester.js';
import camposTester from './formTester/campos.js';

// (Cultivo) Importaciones de funciones en otros archivos JS
import validarFormularioCultivo from './formCultivo/validarFormularioCultivo.js';
import camposCultivo from './formCultivo/campos.js';

// (Enfermedad) Importaciones de funciones en otros archivos JS
import validarFormularioEnfermedad from './formEnfermedad/validarFormularioEnfermedad.js';
import camposEnfermedad from './formEnfermedad/campos.js';

// Declaración de constantes
const data_formulario = document.querySelector('[data-formulario]');
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
    input.addEventListener('keyup', (nombre=='Dataset') ? validarFormularioDataset : (nombre=='Administrador') ? validarFormularioAdministrador : (nombre=='Experto') ? validarFormularioExperto : (nombre=='Tester') ? validarFormularioTester : (nombre=='Cultivo') ? validarFormularioCultivo : (nombre=='Enfermedad') ? validarFormularioEnfermedad : ''); // Cuando se levanta la tecla
    input.addEventListener('blur', (nombre=='Dataset') ? validarFormularioDataset : (nombre=='Administrador') ? validarFormularioAdministrador : (nombre=='Experto') ? validarFormularioExperto : (nombre=='Tester') ? validarFormularioTester : (nombre=='Cultivo') ? validarFormularioCultivo : (nombre=='Enfermedad') ? validarFormularioEnfermedad : ''); // Cuando sale del input
    input.addEventListener('change', (nombre=='Dataset') ? validarFormularioDataset : (nombre=='Administrador') ? validarFormularioAdministrador : (nombre=='Experto') ? validarFormularioExperto : (nombre=='Tester') ? validarFormularioTester : (nombre=='Cultivo') ? validarFormularioCultivo : (nombre=='Enfermedad') ? validarFormularioEnfermedad : ''); // Cuando sale del input
    input.addEventListener('input', (nombre=='Dataset') ? validarFormularioDataset : (nombre=='Administrador') ? validarFormularioAdministrador : (nombre=='Experto') ? validarFormularioExperto : (nombre=='Tester') ? validarFormularioTester : (nombre=='Cultivo') ? validarFormularioCultivo : (nombre=='Enfermedad') ? validarFormularioEnfermedad : ''); // Cuando sale del input
});


// Agregar eventos a cada select para ejecutar una función
selects.forEach((select) => {
    select.addEventListener('click', (nombre=='Dataset') ? validarFormularioDataset : (nombre=='Administrador') ? validarFormularioAdministrador : (nombre=='Experto') ? validarFormularioExperto : (nombre=='Tester') ? validarFormularioTester :  (nombre=='Cultivo') ? validarFormularioCultivo : (nombre=='Enfermedad') ? validarFormularioEnfermedad : ''); // Cuando da un click dentro del select
    select.addEventListener('change', (nombre=='Dataset') ? validarFormularioDataset : (nombre=='Administrador') ? validarFormularioAdministrador : (nombre=='Experto') ? validarFormularioExperto : (nombre=='Tester') ? validarFormularioTester :  (nombre=='Cultivo') ? validarFormularioCultivo : (nombre=='Enfermedad') ? validarFormularioEnfermedad : ''); // Cuando se hace un cambio en la opción
    select.addEventListener('blur', (nombre=='Dataset') ? validarFormularioDataset : (nombre=='Administrador') ? validarFormularioAdministrador : (nombre=='Experto') ? validarFormularioExperto : (nombre=='Tester') ? validarFormularioTester :  (nombre=='Cultivo') ? validarFormularioCultivo : (nombre=='Enfermedad') ? validarFormularioEnfermedad : ''); // Cuando sale del select
});

formulario.addEventListener('submit', (e) => {
    switch (accionNombre){
        case 'Crear-Dataset':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioDataset({target: input}) // {target: input} sirve para simular un evento
            });
            // Validar el formulario para cada select
            selects.forEach((select) => {
                validarFormularioDataset({target: select}) // {target: select} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            if((camposDataset.nombreDataset && camposDataset.ruta && camposDataset.tipoDataset && camposDataset.segmentacion_SAM && camposDataset.homogenizacion_YIQ && camposDataset.formatoImg) == false){
                // Evitar que el formulario se envíe
                e.preventDefault();
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Dataset', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
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

            break

        case 'Crear-Administrador':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioAdministrador({target: input}) // {target: input} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposAdmin)
            if((camposAdmin.id_Administrador && camposAdmin.nombre && camposAdmin.apellidoP && camposAdmin.apellidoM && camposAdmin.fechaNac && camposAdmin.correo && camposAdmin.imagen && camposAdmin.username && camposAdmin.password1 && camposAdmin.password2) == false){
                // Evitar que el formulario se envíe
                e.preventDefault(); 
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Administrador', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }

            break

        case 'Editar-Administrador':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioAdministrador({target: input}) // {target: input} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposAdmin)
            if((camposAdmin.nombre && camposAdmin.apellidoP && camposAdmin.apellidoM && camposAdmin.fechaNac && camposAdmin.correo && camposAdmin.imagen && camposAdmin.username) == false){
                // Evitar que el formulario se envíe
                e.preventDefault();
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Administrador', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }

            break

        case 'Crear-Experto':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioExperto({target: input}) // {target: input} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposExperto)
            if((camposExperto.nombre && camposExperto.apellidoP && camposExperto.apellidoM && camposExperto.fechaNac && camposExperto.correo && camposExperto.institucionPerteneciente && camposExperto.imagen && camposExperto.username && camposExperto.password1 && camposExperto.password2) == false){
                // Evitar que el formulario se envíe
                e.preventDefault(); 
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Experto', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }

            break

        case 'Editar-Experto':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioExperto({target: input}) // {target: input} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposExperto)
            if((camposExperto.nombre && camposExperto.apellidoP && camposExperto.apellidoM && camposExperto.fechaNac && camposExperto.correo && camposExperto.institucionPerteneciente && camposExperto.imagen && camposExperto.username) == false){
                // Evitar que el formulario se envíe
                e.preventDefault(); 
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Experto', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }

            break

        case 'Crear-Tester':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioTester({target: input}) // {target: input} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposTester)
            if((camposTester.nombre && camposTester.apellidoP && camposTester.apellidoM && camposTester.fechaNac && camposTester.correo && camposTester.imagen && camposTester.username && camposTester.password1 && camposTester.password2) == false){
                // Evitar que el formulario se envíe
                e.preventDefault(); 
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Tester', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }

            break

        case 'Editar-Tester':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioTester({target: input}) // {target: input} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposTester)
            if((camposTester.nombre && camposTester.apellidoP && camposTester.apellidoM && camposTester.fechaNac && camposTester.correo && camposTester.imagen && camposTester.username) == false){
                // Evitar que el formulario se envíe
                e.preventDefault(); 
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Tester', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }

            break

        case 'Crear-Cultivo':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioCultivo({target: input}) // {target: input} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposCultivo)
            if((camposCultivo.nombreCultivo && camposCultivo.descripcionCultivo) == false){
                // Evitar que el formulario se envíe
                e.preventDefault();
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Cultivo', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }

            break

        case 'Editar-Cultivo':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioCultivo({target: input}) // {target: input} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposCultivo)
            if((camposCultivo.nombreCultivo && camposCultivo.descripcionCultivo) == false){
                // Evitar que el formulario se envíe
                e.preventDefault();
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Cultivo', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }

            break

        case 'Crear-Enfermedad':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioEnfermedad({target: input}) // {target: input} sirve para simular un evento
            });
            // Validar el formulario para cada select
            selects.forEach((select) => {
                validarFormularioEnfermedad({target: select}) // {target: select} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposEnfermedad)
            if((camposEnfermedad.nombreEnfermedad && camposEnfermedad.cultivoEnfermedad && camposEnfermedad.descripcionEnfermedad && camposEnfermedad.tratamientoEnfermedad) == false){
                // Evitar que el formulario se envíe
                e.preventDefault();
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Enfermedad', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }

            break

        case 'Editar-Enfermedad':
            // Validar el formulario para cada input
            inputs.forEach((input) => {
                validarFormularioEnfermedad({target: input}) // {target: input} sirve para simular un evento
            });
            // Validar el formulario para cada select
            selects.forEach((select) => {
                validarFormularioEnfermedad({target: select}) // {target: select} sirve para simular un evento
            });
            // Valida si alguno o todos los campos no estan llenados de forma correcta
            console.log(camposEnfermedad)
            if((camposEnfermedad.nombreEnfermedad && camposEnfermedad.cultivoEnfermedad && camposEnfermedad.descripcionEnfermedad && camposEnfermedad.tratamientoEnfermedad) == false){
                // Evitar que el formulario se envíe
                e.preventDefault();
                // Mandar una alerta a la vista
                notificationSweet2('Campos Incompletos Enfermedad', 'Por favor llene todos los campos solicitados con las características señaladas para cada uno.', 'warning', 'Ok')
            }

            break
    }
});


