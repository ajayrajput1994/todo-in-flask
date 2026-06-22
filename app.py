from flask import Flask, render_template, request, jsonify, redirect, url_for
from extensions import db, migrate, login_manager
from models import Todo, User
from waitress import serve
from auth import auth_bp
import os

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",  
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config is not None:
      app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_form"  # redirect here if not logged in


    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))
    
    # register blueprints 
    app.register_blueprint(auth_bp)

    @app.route("/init-db")
    def init_db():
        with app.app_context():
            db.create_all()
        return "Database initialized"

    @app.route("/", methods=["GET"])
    def index(): 
        todolist = db.session.scalars(db.select(Todo)).all() 
        return render_template("index.html",todolist=todolist)
  
    @app.route("/add-todo", methods=["POST"])
    def add_todo():
        if request.method == "POST":
          title = request.form.get("title", "").strip()
          desc = request.form.get("desc", "").strip()
          
          if not title or not desc:
            return redirect(url_for("index"))
          
          todo = Todo(title=title, desc=desc)
          db.session.add(todo)
          db.session.commit()
        return redirect(url_for("index"))
    
    @app.route("/delete-todo/<int:sno>", methods=["GET"])
    def delete_todo(sno):
        todo = Todo.query.get_or_404(sno)
        if todo:
          db.session.delete(todo)
          db.session.commit()
        return redirect(url_for("index"))
    
    @app.route("/edit-todo/<int:sno>", methods=["GET", "POST"])
    def edit_todo(sno):
        todo = Todo.query.get_or_404(sno)
        if request.method == "POST":
          title = request.form.get("title", "").strip()
          desc = request.form.get("desc", "").strip()
          
          if not title or not desc:
            return redirect(url_for("index"))
          
          if todo:
            todo.title = title
            todo.desc = desc
            db.session.commit()
          return redirect(url_for("index"))
        
        return render_template("edit_todo.html", todo=todo)
    
    return app

app = create_app()

if __name__=="__main__":
    # app.run(debug=True,port=5000)
    print("app starting...")
    serve(app, host="0.0.0.0", port=8000)

