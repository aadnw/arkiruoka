from app import app
from flask import render_template, request, redirect, session
import recipes
import users

@app.route("/")
def index():
    list = recipes.get_categories()
    top_recipes = recipes.get_top_recipes()
    return render_template("index.html", categories=list, tops=top_recipes)

@app.route("/new/<int:category_id>")
def new(category_id):
    id = recipes.get_category_info(category_id)[1]
    return render_template("new.html", c_id=id)

@app.route("/create", methods=["POST"])
def create_recipe():
    users.require_role(1)
    users.check_csrf()

    category_id = request.form["category_id"]

    name = request.form["name"]
    if len(name) < 1:
        return render_template("error.html", message="Nimi ei ole tarpeeksi kuvaava", 
                               adress="/new/"+str(category_id))
    if len(name) > 50:
        return render_template("error.html", message="Nimi on liian pitkä", 
                               adress="/new"+str(category_id))
    
    time = request.form["time"]
    if not time:
        return render_template("error.html", message="Et asettanut reseptille valmistusaikaa", 
                               adress="/new"+str(category_id))

    ingredients = request.form["ingredients"].replace('\n', '<br>')
    if ingredients == "":
        return render_template("error.html", message="Ainesosien tekstikenttä on tyhjä", 
                               adress="/new/"+str(category_id))
    
    instructions = request.form["instructions"]
    if instructions == "":
        return render_template("error.html", message="Valmistusohjeiden tekstikenttä on tyhjä", 
                               adress="/new/"+str(category_id))
    
    recipe_id = recipes.new_recipe(name, time, ingredients, instructions, users.user_id(), category_id)
    return redirect("/recipe/"+str(recipe_id))
    
@app.route("/remove", methods=["GET", "POST"])
def remove_recipe():
    if request.method == "GET":
        users.require_role(1)
        my_recipes = recipes.get_my_recipes(users.user_id())
        return render_template("remove.html", list=my_recipes)

    if request.method == "POST":
        users.check_csrf()

        recipe = request.form["recipe"]
        recipes.remove_recipe(recipe, users.user_id())

        return redirect("/profile/"+str(users.user_id()))


@app.route("/admin_remove", methods=["GET", "POST"])
def admin_remove_recipe():
    users.require_role(2)

    if request.method == "GET":
        removable = recipes.get_all_recipes()
        return render_template("admin_remove.html", list=removable)
    
    if request.method == "POST":
        users.check_csrf()

        recipe = request.form["recipe"]
        recipes.remove_recipe_admin(recipe)

        return redirect("/")
    
@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    info = recipes.get_recipe_info(recipe_id)
    reviews = recipes.get_reviews(recipe_id)
    check = recipes.check_favorites(recipe_id)
    favorite = recipes.is_favorite(recipe_id, users.user_id())

    return render_template("recipe.html", id=recipe_id, name=info[0],
                           creator=info[1], time=info[2], 
                           ingredients=info[3].replace('<br>', '').replace('<br/>', ''), 
                           instructions=info[4].replace('<br>', '').replace('<br/>', ''), 
                           creator_id=info[5], visible=favorite, reviews=reviews, check_favorites=check)

@app.route("/new_cat", methods=["GET", "POST"])
def new_category():
    users.require_role(2)

    if request.method == "GET":
        return render_template("new_cat.html")
    
    if request.method == "POST":
        users.check_csrf()

        name = request.form["name"]
        if len(name) < 4:
            return render_template("error.html", message="Nimi ei ole tarpeeksi kuvaava", 
                                   adress="/new_cat")
        if len(name) > 50:
            return render_template("error.html", message="Nimi on liian pitkä", 
                                   adress="/new_cat")

        category_id = recipes.new_category(name)
        return redirect("/")
    
@app.route("/remove_cat", methods=["GET", "POST"])
def remove_category():
    users.require_role(2)

    if request.method == "GET":
        categories = recipes.categories_for_removal()
        return render_template("remove_cat.html", list=categories)
    
    if request.method == "POST":
        users.check_csrf()

        if "category" in request.form:
            category = request.form["category"]
            recipes.remove_category(category)

        return redirect("/")
    
@app.route("/category/<int:category_id>")
def show_category(category_id):
    info = recipes.get_category_info(category_id)
    category_recipes = recipes.get_category_recipes(category_id)
    return render_template("category.html", name=info[0], id=info[1], recipes=category_recipes)
        
@app.route("/review", methods=["POST"])
def review():
    users.require_role(1)
    users.check_csrf()

    recipe_id = request.form["recipe_id"]

    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("error.html", message="Virheellinen määrä tähtiä", adress="/review")
    
    comment = request.form["comment"]
    if len(comment) > 1000:
        return render_template("error.html", message="Kommentti on liian pitkä", adress="/review")
    if comment == "":
        comment = "-"
    
    review_id = recipes.add_review(recipe_id, users.user_id(), stars, comment)
    return redirect("/recipe/"+str(recipe_id))

@app.route("/result")
def result():
    query = request.args["query"]
    query = recipes.result(query)
    return render_template("result.html", results=query)

@app.route("/profile/<user_id>")
def show_profile(user_id):
    my_recipes = recipes.get_my_recipes(user_id)
    return render_template("profile.html", recipes=my_recipes)

@app.route("/add_favorite", methods=["POST"])
def add_fav():
    users.require_role(1)
    users.check_csrf()
    
    recipe_id = request.form["recipe_id"]
    favorite_id = recipes.add_favorite(recipe_id, users.user_id())
    return redirect("/recipe/"+str(recipe_id))

@app.route("/favorite", methods=["POST"])
def favorite():
    users.require_role(1)
    users.check_csrf()

    recipe_id = request.form["recipe_id"]
    recipes.favorite(recipe_id, users.user_id())

    return redirect("/recipe/"+str(recipe_id))

@app.route("/remove_fav", methods=["POST"])
def remove_favorite():
    users.require_role(1)
    users.check_csrf()

    recipe_id = request.form["recipe_id"]
    recipes.remove_favorite(recipe_id, users.user_id())

    return redirect("/recipe/"+str(recipe_id))

@app.route("/favorites/<user_id>")
def show_favorites(user_id):
    info = set(recipes.favorites(user_id))
    return render_template("favorites.html", favorites=info)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Annoit väärän tunnuksen tai salasanan", 
                                   adress="/login")
        return redirect("/")
    
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Käyttäjätunnuksessa tulee olle 1-20 merkkiä", 
                                   adress="/register")
        
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää", 
                                   adress="/register")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä", 
                                   adress="/register")
        
        if len(password1) < 7 or len(password1) > 20:
            return render_template("error.html", message="Salasanan tulee olla 7-20 merkkiä", 
                                   adress="/register")
        
        role = request.form["role"]
        
        if role not in ("1", "2"):
            return render_template("error.html", message="Tuntematon käyttäjärooli", 
                                   adress="/register")
        
        if not users.register(username, password1, role):
            return render_template("error.html", message="Rekisteröinti ei onnistunut", 
                                   adress="/register")
        return redirect("/")
    