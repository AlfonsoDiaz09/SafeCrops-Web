import expresiones from "./expresiones.js";
import errores from "./errores.js";
import validarCampoText from "../camposValidate/campoText/validarCampoText.js";
import validarCampoFile from "../camposValidate/campoFile/validarCampoFile.js";
import validarCampoSelect from "../camposValidate/campoSelect/validarCampoSelect.js";

const validarFormularioDataset = (e) => {
    switch (e.target.name){
        case "nombreModelo_transformer":
            validarCampoText(expresiones.nombreModelo_transformer, e.target, e.target.name, errores.error_nombreModelo_transformer);
        break;

        case "datasetModelo_transformer":
            validarCampoSelect(e.target.value, e.target.name, errores.error_datasetModelo_transformer);
        break;

        case "pesosModelo_transformer":
            validarCampoFile(expresiones.pesosModelo_transformer, e.target, e.target.name, errores.error_pesosModelo_transformer);
        break;

        case "epocas_transformer":
            validarCampoText(expresiones.epocas_transformer, e.target, e.target.name, errores.error_epocas_transformer);
        break;
        
        case "batch_size_transformer":
            validarCampoSelect(e.target.value, e.target.name, errores.error_batch_size_transformer);
        break;
    }
}

export default validarFormularioDataset;