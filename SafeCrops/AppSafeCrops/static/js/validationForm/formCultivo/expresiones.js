/* 
	Expresiones regulares que validan la información minima 
	que debe contener cada campo del formulario
*/

const expresiones = {
	nombreCultivo: /^[a-zA-ZÀ-ÿ\s]{2,45}$/,
	descripcionCultivo: /^[a-zA-ZÀ-ÿ\s]{5,200}$/,
}

export default expresiones;