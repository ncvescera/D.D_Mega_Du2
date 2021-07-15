from werkzeug.utils import secure_filename
import os

def check_required_data(dati: tuple) -> bool:
    """
    Ritorna True se tutti i dati passati non sono None o stringa vuota
    """

    result = True
    for elem in dati:
        if elem is None:
            result = False
            break

        tmp = elem.strip(' \n\r')
        if tmp == '':
            result = False
            break

    return result


def process_file(file_name: str, save_dir: str, episodio_id: str, stagione_id: str, serie_id: str) -> tuple:
    """
    Ritorna il nuovo nome del file e i path dove andra' salvato
    """

    # serie_id = Stagione.query.filter_by(id=stagione_id).first().serie_id
    filename = secure_filename(file_name)

    new_nome = f"{serie_id}_{stagione_id}_{episodio_id}"
    ext = filename.split('.')[-1]
    new_filename = f"{new_nome}.{ext}"

    file_path = os.path.join(save_dir, new_filename)

    return (new_filename, file_path)