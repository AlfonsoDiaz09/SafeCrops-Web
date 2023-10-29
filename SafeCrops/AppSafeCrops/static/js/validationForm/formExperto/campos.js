/* 
	Se establece un valor inicial false a todos los campos del formulario
    para indicar que los campos no son válidos de acuerdo a las expresiones
    regulares, este valor se cambiara a true cuando el campo sea llenado 
    correctamente en la función correspondiente
*/

const campos = {
    nombre: false,
    apellidoP: false,
    apellidoM: false,
    fechaNac: false,
    correo: false,
    institucionPerteneciente: false,
    imagen: false,
    username: false,
    password1: false,
    password2: false,
}

export default campos;