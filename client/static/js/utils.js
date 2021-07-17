function elimina_serie(id) {
    $.ajax({
        url: `${server_ip}/serie/${id}`,
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
        url: `${server_ip}/stagione/${id}`,
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
        url: `${server_ip}/episodio/${id}`,
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

function plot_episodi(episodi) {
    var table = $("<table>").attr('class', 'table table-hover table-striped');
    var tbody = $('<tbody>');
    episodi.forEach(element => {
        var riga = $('<tr>');
        var nome = $('<td>').text(element.nome);
        var descrizione = $('<td>').text(element.descrizione);
        var tag = $('<td class="tag">').text(element.tag);
        var play = $('<td class="rigthalign">')
            .append(
                $('<a class="btn btn-sm btn-info" target="_blank">')    // bottone PLAY
                    .attr('href', `${server_ip}/play/${element.id}`)
                    .html(
                        $('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play-circle" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M6.271 5.055a.5.5 0 0 1 .52.038l3.5 2.5a.5.5 0 0 1 0 .814l-3.5 2.5A.5.5 0 0 1 6 10.5v-5a.5.5 0 0 1 .271-.445z"/></svg>')
                    ),
                $('<span>').text(' '),
                $('<a class="btn btn-sm btn-primary">')    // bottone modifica episodio
                    .attr('href', `/episodio/${element.id}`)
                    .html(
                        $('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16"><path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/><path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/></svg>')
                    ),
                    $('<span>').text(' '),
                $('<button class="btn btn-sm btn-danger">')     // bottone elimina episodio
                    .attr('onclick', `elimina_episodio(${element.id});`)
                    .html(
                        $('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/></svg>')
                    )
            );

        riga.append(nome, descrizione, tag, play);
        tbody.append(riga);    
        table.append(tbody);
    });

    return table;
}

function plot_stagioni(stagioni) {
    var table = $("<table>").attr('class', 'table table-hover table-striped');
    var tbody = $('<tbody>');

    stagioni.forEach(element => {
        var riga = $('<tr class="cliccabile">')
            .attr('onclick', `location.href='/serie/${element.serie_id}'`)
            .attr('onauxclick', `window.open("/serie/${element.serie_id}", "_blank")`);
        var nome = $('<td>').text(element.nome);
        var descrizione = $('<td>').text(element.descrizione);
        var tag = $('<td class="tag">').text(element.tag);
        
        riga.append(nome, descrizione, tag);
        tbody.append(riga);    
        table.append(tbody);
    });

    return table;
}

function plot_serie(serie) {
    var box = $('<div>');
                        
    serie.forEach(element => {
        // crea per ogni elemento dell'array la relativa carta
        var card = $('<div class="card">');

        var header = $('<div class="card-header">');    // card_header
        var tabella = $('<table style="width: 100;">')  // contenuto card_header
            .append(
                $('<tr style="width: 100%;">')
                    .append(
                        $('<td style="width: 100%; color: blue;">').text(element.tag),  // tag
                        $('<td style="width: auto;">')  
                            .append(
                                $('<button class="btn btn-danger btn-sm">') // bottone elimina serie
                                    .attr('onclick', `elimina_serie(${element.id});`)
                                    .html(
                                        $('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/></svg>')
                                    )
                            )
                    )
            )

        header.append(tabella);

        var card_body = $('<div class="card-body" style="cursor: pointer;">')
            .attr('onclick', `location.href='/serie/${element.id}'`)
            .attr('onauxclick', `window.open("/serie/${element.id}", "_blank")`)
            .append(
                $('<h5 class="card-title">').text(element.nome),
                $('<p class="card-text">').text(element.descrizione)
            );
        
        card.append(header, card_body);
        box.append(card);
        box.append($('<br>'));
    });

    return box;
}