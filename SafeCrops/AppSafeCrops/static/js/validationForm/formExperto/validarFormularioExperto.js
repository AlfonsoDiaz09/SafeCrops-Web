import expresiones from "./expresiones.js";
import errores from "./errores.js";
import validarCampoText from "../camposValidate/campoText/validarCampoText.js";
import validarPassword2 from "../camposValidate/campoPassword/validarCampoPassword.js";
import validarCampoDate from "../camposValidate/campoDate/validarCampoDate.js";
import validarCampoImage from "../camposValidate/campoImage/validarCampoImage.js";

const validarFormularioExperto = (e) => {
    switch (e.target.name){
        case "nombre":
            validarCampoText(expresiones.nombre, e.target, e.target.name, errores.error_nombre);
        break;

        case "apellidoP":
            validarCampoText(expresiones.apellidoP, e.target, e.target.name, errores.error_apellidoP);
        break;

        case "apellidoM":
            validarCampoText(expresiones.apellidoM, e.target, e.target.name, errores.error_apellidoM);
        break;

        case "fechaNac":
            validarCampoDate(expresiones.fechaNac, e.target, e.target.name, errores.error_fechaNac, errores.error_edad);
        break;

        case "correo":
            validarCampoText(expresiones.correo, e.target, e.target.name, errores.error_correo);
        break;
        
        case "institucionPerteneciente":
            validarCampoText(expresiones.institucionPerteneciente, e.target, e.target.name, errores.error_institucionPerteneciente);
        break;

        case "imagen":
            validarCampoImage(expresiones.imagen, e.target, e.target.name, errores.error_imagen);
        break;

        case "username":
            validarCampoText(expresiones.username, e.target, e.target.name, errores.error_username);
        break;

        case "password1":
            validarPassword2(expresiones.password, e.target.name, errores.error_password2);
            validarCampoText(expresiones.password, e.target, e.target.name, errores.error_password1);
        break;

        case "password2":
            validarPassword2(expresiones.password, e.target.name, errores.error_password2);
        break;
    }
}

export default validarFormularioExperto;