import camposDataset from "../../formDataset/campos.js";
import camposAdmin from "../../formAdministrador/campos.js";
import camposExperto from "../../formExperto/campos.js";
import camposTester from "../../formTester/campos.js";
import camposCultivo from "../../formCultivo/campos.js";
import camposEnfermedad from "../../formEnfermedad/campos.js";
import camposModeloTransformer from "../../formModeloTransformer/campos.js";

// Obtener el nombre del id del formulario sin la palabra formulario y convertir la primer letra en mayuscula
const data_formulario = document.querySelector('[data-formulario]');
var nombre = data_formulario.id.split('-')[1]
nombre = nombre.charAt(0).toUpperCase() + nombre.slice(1)

const validarCampoText = (expresion, input, campo, error) => {

    if(expresion.test(input.value)){
        document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto')
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto')
        document.querySelector(`#help-text-${campo}`).innerHTML = '';
        nombre == 'Dataset' ? camposDataset[campo] = true : nombre == 'Administrador' ? camposAdmin[campo] = true : nombre == 'Experto' ? camposExperto[campo] = true : nombre == 'Tester' ? camposTester[campo] = true : nombre == 'Cultivo' ? camposCultivo[campo] = true : nombre == 'Enfermedad' ? camposEnfermedad[campo] = true : nombre == 'ModeloTransformer' ? camposModeloTransformer[campo] = true : '';
        console.log("Campo True: ", camposTester[campo], campo)
    }else{
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto')
        document.querySelector(`#help-text-${campo}`).innerHTML = error;
        nombre == 'Dataset' ? camposDataset[campo] = false : nombre == 'Administrador' ? camposAdmin[campo] = false : nombre == 'Experto' ? camposExperto[campo] = false : nombre == 'Tester' ? camposTester[campo] = false : nombre == 'Cultivo' ? camposCultivo[campo] = false : nombre == 'Enfermedad' ? camposEnfermedad[campo] = false : nombre == 'ModeloTransformer' ? camposModeloTransformer[campo] = false : '';
        console.log("Campo False: ", camposTester[campo], campo)
    }
}

export default validarCampoText;