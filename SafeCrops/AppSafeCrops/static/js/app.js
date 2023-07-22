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





