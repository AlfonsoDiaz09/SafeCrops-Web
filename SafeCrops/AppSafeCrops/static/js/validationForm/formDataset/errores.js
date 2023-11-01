/* 
	Mensajes que se mostraran debajo de cada campo del formulario
    cuando no se cumpla con la validación de expresiones establecida
*/

const errores = {
    error_nombreDataset: 'Debe contener de 4 a 45 caracteres y sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Dígitos numéricos (0-9). <br> * Guión bajo (_). <br> * Carácteres acentuados. <br> * Espacios en blanco.',
    error_tipoDataset: 'Debe seleccionar una opción válida',
    error_segmentacion_SAM: 'Debe seleccionar una opción válida',
    error_formatoImg: 'Debe seleccionar una opción válida',
    error_ruta: 'Debe cargar un archivo con extensión .zip',
}

export default errores;