import camposAdmin from "../../formAdministrador/campos.js";
import camposExperto from "../../formExperto/campos.js";
import camposTester from "../../formTester/campos.js";

// Obtener el nombre del id del formulario sin la palabra formulario y convertir la primer letra en mayuscula
const data_formulario = document.querySelector('[data-formulario]');
var nombre = data_formulario.id.split('-')[1]
nombre = nombre.charAt(0).toUpperCase() + nombre.slice(1)

const validarCampoDate = (expresion, input, campo, error, error_edad) => {

    // Separar y formatear fecha de 
    var formatearFecha = (function () {
        const partesFecha = input.value.split('-');

        var dia = parseInt(partesFecha[2], 10);
        var mes = parseInt(partesFecha[1], 10);
        var annio = parseInt(partesFecha[0], 10);


        if(dia >= 1 && dia <= 9){
            dia = `0${dia}`
        }
    
        if(mes >= 1 && mes <= 9){
            mes = `0${mes}`
        }

        var fechaFormateada = `${annio}-${mes}-${dia}`;

        return fechaFormateada;
    });
        
    // Calcular edad
    var obtenerEdad = (function(){
        var fechaActual = moment(new Date())
        fechaActual.format('YYYY-MM-DD')
        var annios = fechaActual.diff(nuevaFecha, 'year');

        return annios;
    });

    var nuevaFecha = formatearFecha();
    var edad = obtenerEdad();

    if(expresion.test(nuevaFecha) && edad > 17 && edad < 86){
        document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto')
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto')
        document.querySelector(`#help-text-${campo}`).innerHTML = '';
        nombre == 'Administrador' ? camposAdmin[campo] = true : nombre == 'Experto' ? camposExperto[campo] = true : nombre == 'Tester' ? camposTester[campo] = true : '';
    }else{
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto')
        document.querySelector(`#help-text-${campo}`).innerHTML = ((expresion.test(nuevaFecha) && (edad < 17 || edad > 86)) ? error_edad : error);
        nombre == 'Administrador' ? camposAdmin[campo] = false : nombre == 'Experto' ? camposExperto[campo] = false : nombre == 'Tester' ? camposTester[campo] = false : '';
    }
}

export default validarCampoDate;