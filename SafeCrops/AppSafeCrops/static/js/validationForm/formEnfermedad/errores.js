/* 
	Mensajes que se mostraran debajo de cada campo del formulario
    cuando no se cumpla con la validación de expresiones establecida
*/

const errores = {
    error_nombreEnfermedad: 'Debe contener de 3 a 45 caracteres y sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Carácteres acentuados. <br> * Espacios en blanco.',
    error_cultivoEnfermedad: 'Debe seleccionar una opción válida.',
    error_descripcionEnfermedad: 'Debe contener de 5 a 200 caracteres y sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Carácteres acentuados. <br> * Espacios en blanco.',
    error_tratamientoEnfermedad: 'Debe contener de 4 a 200 caracteres y sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Carácteres acentuados. <br> * Espacios en blanco.',
}

export default errores;