function validacionContacto() {
    valMsj = document.getElementById("validacion")
    valMsj.innerHTML = ""
    const validLetras = /^[a-zA-Z\s]*$/; // Verificacion solo letras
    const validNumPos = /^\d+$/; // Verificacion solo numeros
    const validMail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/; // Verificacion formato email
    const validLyN = /^[a-zA-Z0-9\s.,-]*$/; // Verificacion letras y numeros

    if ((!validLetras.test(document.getElementById('nombre').value)) || (document.contacto.nombre.value.length <= 2)) {
        document.contacto.nombre.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Nombre incorrecto"
        return
    }

    if ((!validMail.test(document.getElementById('correo').value)) || (document.contacto.correo.value.length < 5)) {
        document.contacto.correo.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Correo incorrecto"
        return
    }

    if ((!validNumPos.test(document.getElementById('telefono').value)) || (document.contacto.telefono.value.length != 10)) {
        document.contacto.telefono.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Telefono incorrecto"
        return
    }

    if ((!validLyN.test(document.getElementById('asunto').value)) || (document.contacto.asunto.value.length <= 2)) {
        document.contacto.asunto.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Asunto incorrecto"
        return
    }

    const mensajeInput = document.getElementById('mensaje').value;

    if (mensajeInput.length > 380) {
        document.contacto.mensaje.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Se ha excedido el maximo de caracteres permitidos como comentario. "
        return
    };
    if (mensajeInput.trim() === '') {
        document.contacto.mensaje.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "No se ha introducido ningun mensaje. "
        return
    };

    document.contacto.submit();

    document.contacto.reset();
}
