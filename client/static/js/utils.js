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

function elimina_stagione(id) {
    $.ajax({
        url: server_ip + '/stagione/'+ id,
        type: 'DELETE',
        
        success: function (response) {
            alert(response.message);
            location.reload();
        },

        error: function (error) {
            alert(error.responseJSON.error);
        }

    });
}

function elimina_episodio(id) {
    $.ajax({
        url: server_ip + '/episodio/'+ id,
        type: 'DELETE',
        
        success: function (response) {
            alert(response.message);
            location.reload();
        },

        error: function (error) {
            alert(error.responseJSON.error);
        }

    });
}