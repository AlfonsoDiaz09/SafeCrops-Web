import expresiones from "./expresiones.js";
import errores from "./errores.js";
import validarCampoText from "../camposValidate/campoText/validarCampoText.js";
import validarCampoFile from "../camposValidate/campoFile/validarCampoFile.js";
import validarCampoSelect from "../camposValidate/campoSelect/validarCampoSelect.js";

const validarFormularioYOLOv5 = (e) => {
    switch (e.target.name){
        case "nombreModelo_y5":
            validarCampoText(expresiones.nombreModelo_y5, e.target, e.target.name, errores.error_nombreModelo_y5);
        break;

        case "datasetModelo_y5":
            validarCampoSelect(e.target.value, e.target.name, errores.error_datasetModelo_y5);
        break;

        case "pesosModelo_y5":
            validarCampoFile(expresiones.pesosModelo_y5, e.target, e.target.name, errores.error_pesosModelo_y5);
        break;

        case "epocas_y5":
            validarCampoText(expresiones.epocas_y5, e.target, e.target.name, errores.error_epocas_y5);
        break;
        
        case "batch_size_y5":
            validarCampoSelect(e.target.value, e.target.name, errores.error_batch_size_y5);
        break;
    }
}

export default validarFormularioYOLOv5;