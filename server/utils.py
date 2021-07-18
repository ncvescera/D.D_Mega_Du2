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

    filename = secure_filename(file_name)   # prende il nome del file

    # crea il nuovo nome ({serie_id}_{stagione_id}_{episodio_id}.mp4)
    new_nome = f"{serie_id}_{stagione_id}_{episodio_id}"
    ext = filename.split('.')[-1]
    new_filename = f"{new_nome}.{ext}"

    # crea il path di dove andra' salvato il file
    file_path = os.path.join(save_dir, new_filename)

    return (new_filename, file_path)


def to_dict(array: list) -> list:
    """
    Applica il metodo as_dict() ad ogni elemento della lista
    """
    
    return [x.as_dict() for x in array]