from app import db

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    follower_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    following_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    status = db.Column(db.String(20), default="pending")  
    # pending / accepted

    created_at = db.Column(db.DateTime, default=db.func.now())