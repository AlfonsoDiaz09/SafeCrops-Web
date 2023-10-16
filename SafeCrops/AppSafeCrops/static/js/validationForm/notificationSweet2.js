const notificationSweet2 = (title, text, icon, confirmButtonText) => {
    Swal.fire({
        title: title,
        text: text,
        icon: icon,
        confirmButtonText: confirmButtonText,
    });
};

export default notificationSweet2;