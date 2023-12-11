import expresiones from "./expresiones.js";
import errores from "./errores.js";
import validarCampoText from "../camposValidate/campoText/validarCampoText.js";
import validarCampoFile from "../camposValidate/campoFile/validarCampoFile.js";
import validarCampoSelect from "../camposValidate/campoSelect/validarCampoSelect.js";

const validarFormularioYOLOv7 = (e) => {
    switch (e.target.name){
        case "nombreModelo_y7":
            validarCampoText(expresiones.nombreModelo_y7, e.target, e.target.name, errores.error_nombreModelo_y7);
        break;

        case "datasetModelo_y7":
            validarCampoSelect(e.target.value, e.target.name, errores.error_datasetModelo_y7);
        break;

        case "pesosModelo_y7":
            validarCampoFile(expresiones.pesosModelo_y7, e.target, e.target.name, errores.error_pesosModelo_y7);
        break;

        case "epocas_y7":
            validarCampoText(expresiones.epocas_y7, e.target, e.target.name, errores.error_epocas_y7);
        break;
        
        case "batch_size_y7":
            validarCampoSelect(e.target.value, e.target.name, errores.error_batch_size_y7);
        break;
    }
}

export default validarFormularioYOLOv7;