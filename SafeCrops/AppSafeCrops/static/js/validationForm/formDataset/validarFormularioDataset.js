import expresiones from "./expresiones.js";
import errores from "./errores.js";
import validarCampoText from "./camposValidate/campoText/validarCampoText.js";
import validarCampoFile from "./camposValidate/campoFile/validarCampoFile.js";
import validarCampoSelect from "./camposValidate/campoSelect/validarCampoSelect.js";
import validarPassword2 from "./camposValidate/campoPassword/validarCampoPassword.js";

const validarFormularioDataset = (e) => {
    switch (e.target.name){
        case "password1":
            validarPassword2(expresiones.password, e.target.name, errores.error_password2);
            validarCampoText(expresiones.password, e.target, e.target.name, errores.error_password1);
        break;

        case "password2":
            validarPassword2(expresiones.password, e.target.name, errores.error_password2);
        break;

        case "nombreDataset":
            validarCampoText(expresiones.nombreDataset, e.target, e.target.name, errores.error_nombreDataset);
        break;

        case "ruta":
            validarCampoFile(e.target.value, e.target.name, errores.error_ruta);
        break;

        case "segmentacion_SAM":
            validarCampoSelect(e.target.value, e.target.name, errores.error_segmentacion_SAM);
        break;
        
        case "formatoImg":
            validarCampoSelect(e.target.value, e.target.name, errores.error_formatoImg);
        break;

        case "tipoDataset":
            validarCampoText(expresiones.tipoDataset, e.target, e.target.name, errores.error_tipoDataset);
        break;

        case "dentro_carpeta":
            validarCampoSelect(e.target.value, e.target.name, errores.error_dentro_carpeta);
        break;
    }
}

export default validarFormularioDataset;