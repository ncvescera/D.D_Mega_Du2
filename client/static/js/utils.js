function elimina_serie(id) {
   
    $.ajax({
        url: server_ip + '/serie/'+ id,
        type: 'DELETE',
        
        success: function (response) {
            alert(response.message);
            location.href = '/serie';
        },

        error: function (error) {
            alert(error.responseJSON.error);
        }

    });
}