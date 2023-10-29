import camposDataset from "../../formDataset/campos.js";
import camposEnfermedad from "../../formEnfermedad/campos.js";
import camposModeloTransformer from "../../formModeloTransformer/campos.js";

// Obtener el nombre del id del formulario sin la palabra formulario y convertir la primer letra en mayuscula
const data_formulario = document.querySelector('[data-formulario]');
var nombre = data_formulario.id.split('-')[1]
nombre = nombre.charAt(0).toUpperCase() + nombre.slice(1)

const validarCampoSelect = (valor, campo, error) => {
    if(valor != ''){
        document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto')
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto')
        document.querySelector(`#help-text-${campo}`).innerHTML = '';
        nombre == 'Dataset' ? camposDataset[campo] = true : nombre == 'Enfermedad' ? camposEnfermedad[campo] = true : nombre == 'ModeloTransformer' ? camposModeloTransformer[campo] = true : '';
    }else{
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto')
        document.querySelector(`#help-text-${campo}`).innerHTML = error;
        nombre == 'Dataset' ? camposDataset[campo] = false : nombre == 'Enfermedad' ? camposEnfermedad[campo] = false : nombre == 'ModeloTransformer' ? camposModeloTransformer[campo] = false : '';
    }
}

export default validarCampoSelect;