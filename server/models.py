from app import db


class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)
    descrizione = db.Column(db.Text)
    tag = db.Column(db.String(80))

    def as_dict(self):
        return {
            'id': self.id,
            'name': str(self.name),
            'description': str(self.description),
            'tag': str(self.tag)
        }


class Episodio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    descrizione = db.Column(db.Text)
    tag = db.Column(db.String(80))
    path = db.Column(db.String(100), nullable=False)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('nome', 'path', name='_episodio_uc'),)