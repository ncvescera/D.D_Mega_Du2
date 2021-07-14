from app import db


class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)
    descrizione = db.Column(db.Text)
    tag = db.Column(db.String(80))

    def as_dict(self):
        return {
            'id': self.id,
            'nome': str(self.nome),
            'descrizione': str(self.descrizione),
            'tag': str(self.tag)
        }


class Stagione(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    descrizione = db.Column(db.Text)
    tag = db.Column(db.String(80))
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('nome', 'serie_id', name='_stagione_uc_'),)

    def as_dict(self):
        return {
            'id': self.id,
            'nome': str(self.nome),
            'descrizione': str(self.descrizione),
            'tag': str(self.tag),
            'serie_id': self.serie_id
        }


class Episodio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    descrizione = db.Column(db.Text)
    tag = db.Column(db.String(80))
    path = db.Column(db.String(100), unique=True ,nullable=False)
    stagione_id = db.Column(db.Integer, db.ForeignKey('stagione.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('nome', 'stagione_id', name='_episodio_uc'),)