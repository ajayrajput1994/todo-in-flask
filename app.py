from flask import Flask, render_template, request, jsonify, redirect
from extensions import db
from models import Todo

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",  
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    @app.route("/init-db")
    def init_db():
        with app.app_context():
            db.create_all()
        return "Database initialized"

    @app.route("/", methods=["GET", "POST"])
    def index():
        name = None
        if request.method == "POST":
            name = request.form.get("name", "").strip() or None
            
        todolist = db.session.scalars(db.select(Todo)).all() 
        return render_template("index.html",todolist=todolist)

    # @app.route("/greet/<name>")
    # def greet(name):
    #     return render_template("greet.html", name=name)
    
    @app.route("/add-todo", methods=["GET", "POST"])
    def add_todo():
        if request.method == "POST":
          title = request.form.get("title", "").strip()
          desc = request.form.get("desc", "").strip()
          
          if not title or not desc:
            return redirect("/")
          
          todo = Todo(title=title, desc=desc)
          db.session.add(todo)
          db.session.commit()
        return redirect("/")
    
    @app.route("/delete-todo/<int:sno>", methods=["GET", "POST"])
    def delete_todo(sno):
        todo = Todo.query.filter_by(sno=sno).first()
        if todo:
          db.session.delete(todo)
          db.session.commit()
        return redirect("/")
    
    @app.route("/edit-todo/<int:sno>", methods=["GET", "POST"])
    def ceate_update_todo(sno):
        todo = Todo.query.filter_by(sno=sno).first()
        if request.method == "POST":
          title = request.form.get("title", "").strip()
          desc = request.form.get("desc", "").strip()
          
          if not title or not desc:
            return redirect("/")
          
          if todo:
            todo.title = title
            todo.desc = desc
            db.session.commit()
          return redirect("/")
        
        return render_template("edit_todo.html", todo=todo)
    
    return app

app = create_app()

if __name__=="__main__":
    app.run(debug=True,port=5000)

