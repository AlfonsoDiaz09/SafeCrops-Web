const btn_YOLOv5 = document.querySelector('#btn_yolov5');
const formulario_yolov5 = document.querySelector('#formulario_yolov5');

const btn_YOLOv7 = document.querySelector('#btn_yolov7');
const formulario_yolov7 = document.querySelector('#formulario_yolov7');

const btn_transformer = document.querySelector('#btn_transformer');
const formulario_transformer = document.querySelector('#formulario_transformer');

function form_YOLOv5(){
    formulario_yolov5.classList.toggle("mostrar");
    btn_YOLOv5.classList.toggle("arquitectura_activa");

    //Remover las clases activas de las demas arquitecturas
    formulario_yolov7.classList.remove("mostrar");
    btn_YOLOv7.classList.remove("arquitectura_activa");

    formulario_transformer.classList.remove("mostrar");
    btn_transformer.classList.remove("arquitectura_activa");
}

function form_YOLOv7(){
    formulario_yolov7.classList.toggle("mostrar");
    btn_YOLOv7.classList.toggle("arquitectura_activa");

    //Remover las clases activas de las demas arquitecturas
    formulario_yolov5.classList.remove("mostrar");
    btn_YOLOv5.classList.remove("arquitectura_activa");

    formulario_transformer.classList.remove("mostrar");
    btn_transformer.classList.remove("arquitectura_activa");
}

function form_Transformer(){
    formulario_transformer.classList.toggle("mostrar");
    btn_transformer.classList.toggle("arquitectura_activa");

    //Remover las clases activas de las demas arquitecturas
    formulario_yolov5.classList.remove("mostrar");
    btn_YOLOv5.classList.remove("arquitectura_activa");

    formulario_yolov7.classList.remove("mostrar");
    btn_YOLOv7.classList.remove("arquitectura_activa");
}

btn_YOLOv5.addEventListener('click', form_YOLOv5);
btn_YOLOv7.addEventListener('click', form_YOLOv7);
btn_transformer.addEventListener('click', form_Transformer);