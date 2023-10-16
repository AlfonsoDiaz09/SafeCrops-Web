import campos from "../../campos.js";

const validarPassword2 = (expresion, campo, error) => {
    const inputPassword1 = document.getElementById('password1');
    const inputPassword2 = document.getElementById('password2');

    if((inputPassword1.value == inputPassword2.value) && (expresion.test(inputPassword2.value))){
        document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto')
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto')
        document.querySelector(`#help-text-${campo}`).innerHTML = '';
        campos[campo] = true;
    }else{
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto')
        document.querySelector(`#help-text-${campo}`).innerHTML = (expresion.test(inputPassword1.value)) ? error : 'Revise primero que el campo Password anterior sea válido.';
        campos[campo] = false;
    }
}

export default validarPassword2;