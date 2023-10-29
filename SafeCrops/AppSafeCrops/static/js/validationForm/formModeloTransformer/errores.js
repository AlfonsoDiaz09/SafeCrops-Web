/* 
	Mensajes que se mostraran debajo de cada campo del formulario
    cuando no se cumpla con la validación de expresiones establecida
*/

const errores = {
    error_nombreModelo_transformer: 'Debe contener de 4 a 45 caracteres y sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Dígitos numéricos (0-9). <br> * Guión bajo (_). <br> * Carácteres acentuados.',
    error_datasetModelo_transformer: 'Debe seleccionar una opción válida',
    error_pesosModelo_transformer: 'Debe cargar un archivo con extensión .pth',
    error_epocas_transformer: 'Debe contener sólo Dígitos numéricos (0-9).',
    error_batch_size_transformer: 'Debe seleccionar una opción válida',
}

export default errores;