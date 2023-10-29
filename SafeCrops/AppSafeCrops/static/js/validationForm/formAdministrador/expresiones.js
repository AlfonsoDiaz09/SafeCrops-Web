/* 
	Expresiones regulares que validan la información minima 
	que debe contener cada campo del formulario
*/

const expresiones = {
	id_Administrador: /^[A-Z0-9]{3,15}$/,
	nombre: /^[a-zA-ZÀ-ÿ\s]{3,45}$/,
	apellidoP: /^[a-zA-ZÀ-ÿ\s]{3,45}$/,
	apellidoM: /^[a-zA-ZÀ-ÿ\s]{3,45}$|^$/,
	fechaNac: /^(\d{4}\-\d{2}\-\d{2})$/,
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	imagen: /^(?:\.(jpg|jpeg|png|gif|webp))?$/,
	username: /^[a-zA-Z0-9\_]{4,25}$/,
    password: /^.{8,16}$/,
	telefono: /^\d{7,14}$/
}

export default expresiones;