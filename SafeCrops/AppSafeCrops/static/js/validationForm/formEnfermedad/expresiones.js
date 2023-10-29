/* 
	Expresiones regulares que validan la información minima 
	que debe contener cada campo del formulario
*/

const expresiones = {
	nombreEnfermedad: /^[a-zA-ZÀ-ÿ\s]{3,45}$/,
	descripcionEnfermedad: /^[a-zA-ZÀ-ÿ\s]{5,200}$/,
	tratamientoEnfermedad: /^[a-zA-ZÀ-ÿ\s]{4,200}$/,
}

export default expresiones;