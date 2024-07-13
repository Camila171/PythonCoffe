function validarPedidos(){
    valMsj = document.getElementById("validacion")
    valMsj.innerHTML = ""
    const validLetras = /^[a-zA-Z\s]*$/; // Verificacion solo letras
    const validNumPos = /^\d+$/; // Verificacion solo numeros
    const validMail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/; // Verificacion formato email
    const validDir = /^[a-zA-Z0-9\s.,-]*$/; // Verificacion letras y numeros

    if ((!validLetras.test(document.getElementById('nombre').value)) || (document.pedidos.nombre.value.length <=2)) {
        document.pedidos.nombre.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Nombre incorrecto"
        return
    }

    if ((!validLetras.test(document.getElementById('apellido').value)) || (document.pedidos.apellido.value.length <=2)) {
        document.pedidos.apellido.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Apellido incorrecto"
        return
    }

    if ((!validNumPos.test(document.getElementById('telefono').value)) || (document.pedidos.telefono.value.length !=10)) {
        document.pedidos.telefono.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Telefono incorrecto"
        return
    }

    if ((!validMail.test(document.getElementById('correo').value)) || (document.pedidos.correo.value.length < 5)) {
        document.pedidos.correo.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Correo incorrecto"
        return
    }

    if ((!validDir.test(document.getElementById('calle').value)) || (document.pedidos.correo.value.length < 8)) {
        document.pedidos.calle.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Calle incorrecta"
        return
    }

    if(isNaN(parseInt(document.pedidos.cp.value)) || (document.pedidos.cp.value.length !=4) || (!validNumPos.test(document.getElementById('cp').value))){
        document.pedidos.cp.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Codigo Postal Incorrecto"
        return
    }

    const cafeSelect = document.getElementById('cafe').value;
    if (cafeSelect === 'nonsel') {
        document.pedidos.cafe.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Selecciona un tipo de cafe valido."
        return
    }

    //Simulacion de Stock
    const productos = [
        { id: 'cafe1', nombre: 'Espresso', stock: 5 },
        { id: 'cafe2', nombre: 'Americano', stock: 0 },
        { id: 'cafe3', nombre: 'Cortado', stock: 2 },
        { id: 'cafe4', nombre: 'Macchiato', stock: 4 },
        { id: 'cafe5', nombre: 'Lagrima', stock: 50 },
        { id: 'cafe6', nombre: 'Capuchino', stock: 10 },
    ];

    const prodSel = productos.find(producto => producto.id === cafeSelect);
    if (!(cafeSelect && prodSel.stock >= document.getElementById('cafecnt').value)) {
        document.pedidos.cafecnt.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Lamentablemente no hay suficiente stock del cafe "+ prodSel.nombre + "."
        return
    }

    if ((parseInt(document.pedidos.cafecnt.value) > 10) || (parseInt(document.pedidos.cafecnt.value) < 1)) {
        document.pedidos.cafecnt.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "La cantidad de cafe seleccionada debe ser entre 1 y 10. "
        return
    }

    //Simulacion de pagos por debito no disponibles
    const metodoPago = document.querySelector('input[name="metpago"]:checked');

    if (metodoPago.value === 'debcard') {
        document.pedidos.metpago.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Lamentablemente los pagos por tarjeta de debito se encuentran desactivados temporalmente, por favor, intentelo mas tarde. "
        return
    }


    const comentariosInput = document.getElementById('comentarios').value;

    if (comentariosInput.length > 380) {
        document.pedidos.comentarios.focus()
        valMsj.style.color = "red"
        valMsj.innerHTML = "Se ha excedido el maximo de caracteres permitidos como comentario. "
        return
    };

    document.pedidos.submit()
}

// Autoseleccionar cafe si se accede desde menu
const urlParams = new URLSearchParams(window.location.search);

const cafeSeleccionado = urlParams.get('cafe')?document.getElementById('cafe').value=urlParams.get('cafe'):urlParams.get('nonsel');

// Obtener y autoseleccionar comidas si se accede desde menu

const platosSeleccionados = urlParams.getAll('com');

// Marcar las casillas correspondientes
platosSeleccionados.forEach(cbox => {
    const check = document.querySelector(`input[value="${cbox}"]`);
    if (check) {
        check.checked = true;
    }
});