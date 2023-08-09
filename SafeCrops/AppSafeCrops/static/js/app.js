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
            // nav__span.style.display = "inline-flex";
          }
          if(nameClass == "w-18"){
            const header = document.getElementById("header");
            const beforeHeader = document.querySelector(".before_header");

            header.classList.replace("w-18", "w-6_5");
            beforeHeader.style.width = "5.5%";
            document.querySelectorAll('.nav__span').forEach(span =>{
              span.style.display = "none";
             })
            // nav__span.style.display = "none";
          }
      });
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
  const btnCollapse = document.getElementById("iconCollapse");

      btnCollapse.addEventListener('click', (e) => {
          const nameClass = document.getElementById("userCollapse").className;
          console.log(nameClass);
          if(nameClass == "displayNone"){
            const collapse = document.getElementById("userCollapse");
            const collapseIcon = document.getElementById("row_collapse");

            collapse.classList.replace("displayNone", "displayFlex");
            collapse.style.display = "flex";
            collapse.style.flexDirection = "column";
            collapseIcon.classList.replace("fa-chevron-right", "fa-chevron-down");
          }
          if(nameClass == "displayFlex"){
            const collapse = document.getElementById("userCollapse");
            const collapseIcon = document.getElementById("row_collapse");

            collapse.classList.replace("displayFlex", "displayNone");
            collapse.style.display = "none";
            collapseIcon.classList.replace("fa-chevron-down", "fa-chevron-right");
          }
      });
})();


  




