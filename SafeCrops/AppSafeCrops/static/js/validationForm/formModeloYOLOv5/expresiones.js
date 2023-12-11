/* 
	Expresiones regulares que validan la información minima 
	que debe contener cada campo del formulario
*/

const expresiones = {
	nombreModelo_y5: /^[a-zA-Z0-9À-ÿ\_]{4,45}$/,
	pesosModelo_y5: /^(?:\.(pth))?$/,
	epocas_y5: /^(20|[2-9][0-9]|1[0-9]{2}|2[0-9]{2}|300)$/,
}

export default expresiones;