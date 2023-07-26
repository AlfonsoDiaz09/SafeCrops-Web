(function(){
    const btnDelete = document.querySelectorAll('.btnDelete');

    btnDelete.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log(e.target.href);
            
            Swal.fire({
                title: '¿Estás seguro de eliminar este registro?',
                text: "¡No podrás revertir esto!",
                showCancelButton: true,
                confirmButtonText: 'Eliminar',
                confirmButtonColor: '#d33',
                icon: 'warning',
                iconColor: '#d33',
                backdrop: true,
                showLoaderOnConfirm: true,
                preConfirm: () => {
                    location.href = e.target.href;
                },
                allowOutsideClick: () => false,
                allowEscapeKey: () => false,
            });
        });
    });
})();