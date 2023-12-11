// const inputFile = document.getElementById("upload_img");
// const previewDiv = document.getElementById("img_preview");
// const reader = new FileReader();

// inputFile.addEventListener('change', handleFileChange(e));

// reader.addEventListener('load', showPreview(e));

// function handleFileChange(e){
//   const [imageFile] = e.currentTarget.files;
//   reader.readAsDataURL(imageFile);
// }

// function showPreview(e){
//   const previewImage = new Image();
//   previewImage.src = e.currentTarget.result;
//   previewDiv.appendChild(previewImage);
// }

(function(){
  const btnMenu = document.getElementById("iconMenu");

      btnMenu.addEventListener('click', (e) => {
          const nameClass = document.getElementById("header").className;
          if(nameClass == "w-6_5"){
            const header = document.getElementById("header");
            const beforeHeader = document.querySelector(".before_header");

            header.classList.replace("w-6_5", "w-18");
            beforeHeader.style.width = "20%";
            document.querySelectorAll('.nav__span').forEach(span =>{
              span.style.display = "inline-block";
             })
          }
          if(nameClass == "w-18"){
            const header = document.getElementById("header");
            const beforeHeader = document.querySelector(".before_header");

            header.classList.replace("w-18", "w-6_5");
            beforeHeader.style.width = "5.5%";
            document.querySelectorAll('.nav__span').forEach(span =>{
              span.style.display = "none";
             })
          }

          // Guardar la clase en el localStorage
          localStorage.setItem("headerWidthClass", header.className);
      });

      // Restaurar la clase desde el localStorage
      const storedClass = localStorage.getItem("headerWidthClass");
      if (storedClass) {
        header.className = storedClass;
        if (storedClass === "w-6_5") {
          const header = document.getElementById("header");
          const beforeHeader = document.querySelector(".before_header");

          header.classList.replace("w-18", "w-6_5");
          beforeHeader.style.width = "5.5%";
          document.querySelectorAll('.nav__span').forEach(span =>{
            span.style.display = "none";
            })
        }
      }
})();

(function(){
  const btnProfile = document.getElementById("iconProfile");

      btnProfile.addEventListener('click', (e) => {
          const nameClass = document.getElementById("userContainer").className;
          if(nameClass == "displayNone"){
            const Profile = document.getElementById("userContainer");

            Profile.classList.replace("displayNone", "displayFlex");
            Profile.style.display = "flex";
          }
          if(nameClass == "displayFlex"){
            const Profile = document.getElementById("userContainer");

            Profile.classList.replace("displayFlex", "displayNone");
            Profile.style.display = "none";
          }
      });
})();


(function(){
  const btnCollapse = document.getElementById("iconCollapse-user");

      btnCollapse.addEventListener('click', (e) => {
          const nameClass = document.getElementById("userCollapse").className;
          if(nameClass == "displayNone"){
            const collapse = document.getElementById("userCollapse");
            const collapseIcon = document.getElementById("row_collapse-user");

            collapse.classList.replace("displayNone", "displayFlex");
            collapse.style.display = "flex";
            collapse.style.flexDirection = "column";
            collapseIcon.classList.replace("fa-chevron-right", "fa-chevron-down");
          }
          if(nameClass == "displayFlex"){
            const collapse = document.getElementById("userCollapse");
            const collapseIcon = document.getElementById("row_collapse-user");

            collapse.classList.replace("displayFlex", "displayNone");
            collapse.style.display = "none";
            collapseIcon.classList.replace("fa-chevron-down", "fa-chevron-right");
          }

          // Guardar la clase en el localStorage
          localStorage.setItem("userCollapseClass", userCollapse.className);
      });

      // Restaurar la clase desde el localStorage
      const storedClass = localStorage.getItem("userCollapseClass");
      if (storedClass) {
        userCollapse.className = storedClass;
        if (storedClass === "displayFlex") {
          const collapse = document.getElementById("userCollapse");
          const collapseIcon = document.getElementById("row_collapse-user");
          
          collapse.classList.replace("displayNone", "displayFlex");
          collapse.style.display = "flex";
          collapse.style.flexDirection = "column";
          collapseIcon.classList.replace("fa-chevron-right", "fa-chevron-down");
        }
      }
})();

// Aplicar estilo al contenedor del checkbox seleccionado
(function(){
  console.log("Hola");
  const checkboxes = document.querySelectorAll("#container_referencia input[type='checkbox']");
  console.log(checkboxes);

  checkboxes.forEach((input) => {
    console.log(input);
    input.addEventListener('click', (e) => {
      console.log("target");
      console.log(e.target.parentElement.parentElement.parentElement);
      const container_img = e.target.parentElement.parentElement.parentElement;
      const container_check = e.target.parentElement.querySelector("input");
      const icon_check = e.target.nextElementSibling;
      console.log(icon_check);

      // Desactivar todos los demás checkboxes
      checkboxes.forEach((otherCheckbox) => {
        if (otherCheckbox !== input) {
          otherCheckbox.checked = false;
          const otherContainer_img = otherCheckbox.parentElement.parentElement.parentElement;
          const otherContainer_check = otherCheckbox.parentElement.querySelector("input");
          const otherIcon_check = otherCheckbox.nextElementSibling;

          otherContainer_img.classList.remove("container__img_selected");
          otherContainer_check.style.opacity = "0";
          otherIcon_check.style.display = "none";
          otherIcon_check.style.opacity = "0";
        }
      });

      // Activar el checkbox seleccionado
      container_img.classList.toggle("container__img_selected");

      // container_check.style.opacity = "1";
      // icon_check.style.display = "block";
      // icon_check.style.opacity = "1";

      if (container_check.checked) {
        container_check.style.opacity = "1";
        icon_check.style.display = "block";
        icon_check.style.opacity = "1";
      } else {
        container_check.style.opacity = "0";
        icon_check.style.display = "none";
        icon_check.style.opacity = "0";
      }


    });
    container = input.parentElement.parentElement.parentElement;
    // Mostrar el checkbox solo cuando el mouse está sobre su contenedor
    container.addEventListener('mouseenter', (e) => {
      const container_check = e.target.children[0].children[0].children[0];
      console.log("probando");
      console.log(container_check);
      const icon_check = e.target.children[0].children[0].children[1];
      console.log("probando 2");
      console.log(icon_check);
      container_check.style.opacity = "1";
      icon_check.style.opacity = "1";
    });

    container.addEventListener('mouseleave', (e) => {
      const container_check = e.target.children[0].children[0].children[0];
      const icon_check = e.target.children[0].children[0].children[1];
      if (!container_check.checked) {
        container_check.style.opacity = "0";
        icon_check.style.opacity = "0";
      }
    });
  });
})();