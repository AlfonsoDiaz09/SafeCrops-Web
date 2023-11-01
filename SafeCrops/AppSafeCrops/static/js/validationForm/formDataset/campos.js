/* 
	Se establece un valor inicial false a todos los campos del formulario
    para indicar que los campos no son válidos de acuerdo a las expresiones
    regulares, este valor se cambiara a true cuando el campo sea llenado 
    correctamente en la función correspondiente
*/

const campos = {
    nombreDataset: false,
    ruta: false,
    tipoDataset: false,
    segmentacion_SAM: false,
    formatoImg: false,
}

export default campos;