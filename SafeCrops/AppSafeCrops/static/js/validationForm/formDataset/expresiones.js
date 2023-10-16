const expresiones = {
	usuario: /^[a-zA-Z0-9\_]{4,16}$/,
	nombre: /^[a-zA-ZÀ-ÿ\s]{4,40}$/,
	nombreDataset: /^[a-zA-Z0-9À-ÿ\s\_]{4,45}$/,
    tipoDataset: /^[a-zA-Z]{4,45}$/,
    password: /^.{4,12}$/,
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^\d{7,14}$/
}

export default expresiones;