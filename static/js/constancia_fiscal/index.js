
$(document).on("change", "#input-archivo", fnRevisarExtension);
$(document).on("click", "#btn-submit", ajaxCargarArchivo);

function fnRevisarExtension( _event ) {
   console.log( "arriba", $(this) );

   let extension = $(this).val().split(".").pop();
   let nombreArchivo = $(this).val();
   if (extension == "pdf" || extension == "PDF"){
      if (nombreArchivo.substring(3,11) == "fakepath") {
         nombreArchivo = nombreArchivo.substring(12);
      }
   }
   else{
      aviso( "advertencia",{
         titulo: "Extensión del archivo no válida",
         contenido: "Sólo se aceptan archivos con extensión .pdf",
         tiempo: 3000
      });
      resetInputArchivo();
   }
   _event.preventDefault();
}

function resetInputArchivo(){
   let input = $("#input-archivo");
   input.replaceWith(input.val("").clone(true));
}

function ajaxCargarArchivo(){
   let archivo = document.getElementById("input-archivo"),
       formulario = new FormData();
   $.ajax({
      url: '/cargar_pdf',
      type: "POST",
      contentType:false,
      data: formulario,
      processData:false,
      cache:false,
      dataType: "JSON"
   }).done(function(respuesta){
      if ( respuesta.exito ){
         console.log("funciona");
      }else{
         swal("Error", "Favor de intentar mas tarde", "error");
         resetInputArchivo();
      }
   }).always(function(){
      resetInputArchivo();
   }).fail(function(){
      swal("Error", "Favor de intentar mas tarde", "error");
   });
}