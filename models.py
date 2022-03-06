from app import db

class Names(db.Model):
  __tablename__ = "User"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)

  def __repr__(self):
    return "<Names: {}>".format(self.name)