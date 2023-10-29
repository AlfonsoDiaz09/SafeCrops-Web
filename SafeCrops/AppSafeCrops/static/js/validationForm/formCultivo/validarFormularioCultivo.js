import expresiones from "./expresiones.js";
import errores from "./errores.js";
import validarCampoText from "../camposValidate/campoText/validarCampoText.js";

const validarFormularioCultivo = (e) => {
    switch (e.target.name){
        case "nombreCultivo":
            validarCampoText(expresiones.nombreCultivo, e.target, e.target.name, errores.error_nombreCultivo);
        break;

        case "descripcionCultivo":
            validarCampoText(expresiones.descripcionCultivo, e.target, e.target.name, errores.error_descripcionCultivo);
        break;
    }
}

export default validarFormularioCultivo;