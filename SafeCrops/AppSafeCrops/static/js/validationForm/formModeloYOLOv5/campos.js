/* 
	Se establece un valor inicial false a todos los campos del formulario
    para indicar que los campos no son válidos de acuerdo a las expresiones
    regulares, este valor se cambiara a true cuando el campo sea llenado 
    correctamente en la función correspondiente
*/

const campos = {
    nombreModelo_y5: false,
    datasetModelo_y5: false,
    pesosModelo_y5: false,
    epocas_y5: false,
    batch_size_y5: false,
}

export default campos;