/* 
	Expresiones regulares que validan la información minima 
	que debe contener cada campo del formulario
*/

const expresiones = {
	nombreModelo_transformer: /^[a-zA-Z0-9À-ÿ\_]{4,45}$/,
	pesosModelo_transformer: /^(?:\.(pth))?$/,
	epocas_transformer: /^[0-9]$/,
}

export default expresiones;