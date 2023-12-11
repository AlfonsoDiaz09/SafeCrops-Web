import camposDataset from "../../formDataset/campos.js";
import camposModeloTransformer from "../../formModeloTransformer/campos.js";

// // Obtener el nombre del id del formulario sin la palabra formulario y convertir la primer letra en mayuscula
// const data_formulario = document.querySelector('[data-formulario]');
// var nombre = data_formulario.id.split('-')[1]
// nombre = nombre.charAt(0).toUpperCase() + nombre.slice(1)

// Obtener el nombre del id del formulario sin la palabra formulario y convertir la primer letra en mayúscula
const data_formulario = document.querySelector('[data-formulario]');

if (data_formulario && data_formulario.hasAttribute('data-formulario')) {
    var nombre = data_formulario.id.split('-')[1];
    nombre = nombre.charAt(0).toUpperCase() + nombre.slice(1);
    // Hacer algo con la variable "nombre"
} else {
    // Verificar si existe el atributo data-formulario-transformer
    const data_formulario_transformer = document.querySelector('[data-formulario-transformer]');
    
    if (data_formulario_transformer && data_formulario_transformer.hasAttribute('data-formulario-transformer')) {
        var nombre = data_formulario_transformer.id.split('-')[1];
        nombre = nombre.charAt(0).toUpperCase() + nombre.slice(1);
        // Hacer algo relacionado con data-formulario-transformer
    } else {
        // Verificar si existe el atributo data-formulario-transformer
        const data_formulario_yolov5 = document.querySelector('[data-formulario-yolov5]');
        
        if (data_formulario_yolov5 && data_formulario_yolov5.hasAttribute('data-formulario-yolov5')) {
            var nombre = data_formulario_yolov5.id.split('-')[1];
            nombre = nombre.charAt(0).toUpperCase() + nombre.slice(1);
            // Hacer algo relacionado con data-formulario-yolov5
        } else {
            // Verificar si existe el atributo data-formulario-yolov7
            const data_formulario_yolov7 = document.querySelector('[data-formulario-yolov7]');
            
            if (data_formulario_yolov7 && data_formulario_yolov7.hasAttribute('data-formulario-yolov7')) {
                var nombre = data_formulario_yolov7.id.split('-')[1];
                nombre = nombre.charAt(0).toUpperCase() + nombre.slice(1);
                // Hacer algo relacionado con data-formulario-yolov7
            }
        }
    }
}


const validarCampoFile = (expresion, input, campo, error) => {
    var extension = input.value.split('.')[1]

    if(expresion.test(input.value) || expresion.test('.'+extension)){
        document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto')
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto')
        document.querySelector(`#help-text-${campo}`).innerHTML = '';
        nombre == 'Dataset' ? camposDataset[campo] = true : nombre == 'ModeloTransformer' ? camposModeloTransformer[campo] = true : '';
    }else{
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto')
        document.querySelector(`#help-text-${campo}`).innerHTML = error;
        nombre == 'Dataset' ? camposDataset[campo] = false : nombre == 'ModeloTransformer' ? camposModeloTransformer[campo] = false : '';
    }
}

export default validarCampoFile;