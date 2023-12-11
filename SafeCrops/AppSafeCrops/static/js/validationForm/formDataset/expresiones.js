/* 
	Expresiones regulares que validan la información minima 
	que debe contener cada campo del formulario
*/

const expresiones = {
	nombreDataset: /^[a-zA-Z0-9À-ÿ\s]{4,45}$/,
	ruta: /\.(zip)$/,
}

export default expresiones;