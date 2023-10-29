import expresiones from "./expresiones.js";
import errores from "./errores.js";
import validarCampoText from "../camposValidate/campoText/validarCampoText.js";
import validarCampoSelect from "../camposValidate/campoSelect/validarCampoSelect.js";

const validarFormularioEnfermedad = (e) => {
    switch (e.target.name){
        case "nombreEnfermedad":
            validarCampoText(expresiones.nombreEnfermedad, e.target, e.target.name, errores.error_nombreEnfermedad);
        break;

        case "cultivoEnfermedad":
            validarCampoSelect(e.target.value, e.target.name, errores.error_cultivoEnfermedad);
        break;

        case "descripcionEnfermedad":
            validarCampoText(expresiones.descripcionEnfermedad, e.target, e.target.name, errores.error_descripcionEnfermedad);
        break;

        case "tratamientoEnfermedad":
            validarCampoText(expresiones.tratamientoEnfermedad, e.target, e.target.name, errores.error_tratamientoEnfermedad);
        break;
    }
}

export default validarFormularioEnfermedad;