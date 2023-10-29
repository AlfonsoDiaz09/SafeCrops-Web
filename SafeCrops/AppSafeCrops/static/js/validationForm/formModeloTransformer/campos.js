/* 
	Se establece un valor inicial false a todos los campos del formulario
    para indicar que los campos no son válidos de acuerdo a las expresiones
    regulares, este valor se cambiara a true cuando el campo sea llenado 
    correctamente en la función correspondiente
*/

const campos = {
    nombreModelo_transformer: false,
    datasetModelo_transformer: false,
    pesosModelo_transformer: false,
    epocas_transformer: false,
    batch_size_transformer: false,
}

export default campos;