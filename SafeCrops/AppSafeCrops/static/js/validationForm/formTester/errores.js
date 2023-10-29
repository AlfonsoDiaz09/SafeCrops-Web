/* 
	Mensajes que se mostraran debajo de cada campo del formulario
    cuando no se cumpla con la validación de expresiones establecida
*/

const errores = {
    error_nombre: 'Debe contener de 3 a 45 caracteres y sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Carácteres acentuados. <br> * Espacios en blanco.',
    error_apellidoP: 'Debe contener de 4 a 45 caracteres y sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Carácteres acentuados. <br> * Espacios en blanco.',
    error_apellidoM: 'Debe contener de 4 a 45 caracteres y sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Carácteres acentuados. <br> * Espacios en blanco.',
    error_fechaNac: 'Debe ingresar una fecha válida y debe estar en el formato dd/mm/aaaa',
    error_edad: 'Su edad debe estar entre 18 y 85 años',
    error_correo: 'El correo sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Dígitos numéricos (0-9). <br> * Puntos <br> * Guiones y guion bajo.',
    error_imagen: 'Debe cargar un archivo de imagen (jpg, jpeg, png, gif, webp).',
    error_username: 'El usuario debe contener de 4 a 25 caracteres y sólo puede contener: <br> * Letras minúsculas (a-z). <br> * Letras mayúsculas (A-Z). <br> * Dígitos numéricos (0-9). <br> * Guión bajo.',
    error_password1: 'La contraseña debe contener de 8 a 16 dígitos.',
    error_password2: 'Ambas contraseñas deben ser iguales.',
}

export default errores;