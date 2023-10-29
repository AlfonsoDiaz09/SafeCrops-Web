import camposAdmin from "../../formAdministrador/campos.js";
import camposExperto from "../../formExperto/campos.js";
import camposTester from "../../formTester/campos.js";

// Obtener el nombre del id del formulario sin la palabra formulario y convertir la primer letra en mayuscula
const data_formulario = document.querySelector('[data-formulario]');
var nombre = data_formulario.id.split('-')[1]
nombre = nombre.charAt(0).toUpperCase() + nombre.slice(1)

const validarCampoImage = (expresion, input, campo, error) => {
    var extension = input.value.split('.')[1]

    if(expresion.test(input.value) || expresion.test('.'+extension)){
        document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto')
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto')
        document.querySelector(`#help-text-${campo}`).innerHTML = '';
        nombre == 'Administrador' ? camposAdmin[campo] = true : nombre == 'Experto' ? camposExperto[campo] = true : nombre == 'Tester' ? camposTester[campo] = true : '';
    }else{
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto')
        document.querySelector(`#help-text-${campo}`).innerHTML = error;
        nombre == 'Administrador' ? camposAdmin[campo] = false : nombre == 'Experto' ? camposExperto[campo] = false : nombre == 'Tester' ? camposTester[campo] = false : '';
    }
}

export default validarCampoImage;