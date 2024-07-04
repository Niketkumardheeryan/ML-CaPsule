(document).ready(function(){
	('#btnSend').click(function(){
		var errores = '';

		//Validacion Nombre ----------------
		if (document.getElementById('names').val() == '' {
			errores += '<p>Escriba un Nombre</p>';
		}

		//Validacion Email ----------------
		if (document.getElementById('email')).val() == '' {
			errores += '<p>Inserte un Email</p>';
		}

		//Validacion Mensaje ----------------
		if (document.getElementById('mensaje')).val() == '' {
			errores += '<p>Escriba un mensaje</p>';
		}

		//alert(errores);

		//Enviando Mensaje --------------------

		if (errores == '' == false) {
			var mensajeModal = '<div class="modal_wrap">' +
									'<div class="mensaje_modal">' +
										'<h3>Errores encontrados</h3>' +
										errores +
										'<span id="btnClose">Cerrar</span>'+
									'</div>' +
			                   '</div>'

				$('body').append(mensajeModal);
		}

		$(document.getElementById('btnClose')).click(function){
			$(document.getElementById('.modal_wrap').remove()
		}
	});
});