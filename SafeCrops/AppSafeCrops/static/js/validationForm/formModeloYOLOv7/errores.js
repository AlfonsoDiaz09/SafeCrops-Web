/* 
	Mensajes que se mostraran debajo de cada campo del formulario
    cuando no se cumpla con la validación de expresiones establecida
*/

const errores = {
    error_nombreModelo_y7: 'Debe contener de 4 a 45 caracteres y sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Dígitos numéricos (0-9). <br> * Guión bajo (_). <br> * Carácteres acentuados.',
    error_datasetModelo_y7: 'Debe seleccionar una opción válida',
    error_pesosModelo_y7: 'Debe cargar un archivo con extensión .pt',
    error_epocas_y7: 'Debe estar entre el rango de 20 - 300 epocas.',
    error_batch_size_y7: 'Debe seleccionar una opción válida',
}

export default errores;