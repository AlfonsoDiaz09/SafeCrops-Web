import expresiones from "./expresiones.js";
import errores from "./errores.js";
import validarCampoText from "../camposValidate/campoText/validarCampoText.js";
import validarCampoFile from "../camposValidate/campoFile/validarCampoFile.js";
import validarCampoSelect from "../camposValidate/campoSelect/validarCampoSelect.js";

const validarFormularioDataset = (e) => {
    switch (e.target.name){
        case "nombreDataset":
            validarCampoText(expresiones.nombreDataset, e.target, e.target.name, errores.error_nombreDataset);
        break;

        case "ruta":
            validarCampoFile(expresiones.ruta, e.target, e.target.name, errores.error_ruta);
        break;

        case "tipoDataset":
            validarCampoSelect(e.target.value, e.target.name, errores.error_tipoDataset);
        break;
        
        case "segmentacion_SAM":
            validarCampoSelect(e.target.value, e.target.name, errores.error_segmentacion_SAM);
        break;
        
        case "homogenizacion_YIQ":
            validarCampoSelect(e.target.value, e.target.name, errores.error_homogenizacion_YIQ);
        break;
        
        case "formatoImg":
            validarCampoSelect(e.target.value, e.target.name, errores.error_formatoImg);
        break;
    }
}

export default validarFormularioDataset;