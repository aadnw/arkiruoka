from sqlalchemy.sql import text
from db import db
from flask import session

def get_recipe():
    sql = """SELECT R.name, C.name FROM recipes R, categories C
            WHERE R.id=C.id ORDER BY R.id"""
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_all_recipes():
    sql = "SELECT id, name FROM recipes WHERE visible=1 ORDER BY name"
    return db.session.execute(text(sql)).fetchall()

def get_recipe_info(recipe_id):
    sql = """SELECT R.name, U.username, R.time, R.ingredients, R.instructions
            FROM recipes R, users U WHERE
            R.id=:recipe_id AND R.creator_id=U.id"""
    return db.session.execute(text(sql), {"recipe_id":recipe_id}).fetchone()

def get_my_recipes(user_id):
    sql = """SELECT id, name FROM recipes
            WHERE creator_id=:user_id AND visible=1 ORDER BY name"""
    return db.session.execute(text(sql), {"user_id":user_id}).fetchall()

def new_recipe(name, time, ingredients, instructions, creator_id):
    sql = """INSERT INTO recipes (creator_id, name, time, ingredients, instructions, created_at, visible)
            VALUES (:creator_id, :name, :time, :ingredients, :instructions, NOW(), 1) RETURNING id"""
    recipe_id = db.session.execute(text(sql), {"creator_id":creator_id, "name":name, "time":time, "ingredients":ingredients, "instructions":instructions}).fetchone()[0]
    db.session.commit()
    return recipe_id

def remove_recipe(recipe_id, user_id):
    sql = "UPDATE recipes SET visible=0 WHERE id=:id AND creator_id=:user_id"
    db.session.execute(text(sql), {"id":recipe_id, "user_id":user_id})
    db.session.commit()

def remove_recipe_admin(recipe_id):
    sql = "UPDATE recipes SET visible=0 WHERE id=:id"
    db.session.execute(text(sql), {"id":recipe_id})
    db.session.commit()

def get_categories():
    sql = "SELECT id, name FROM categories WHERE visible=1 ORDER BY name"
    return db.session.execute(text(sql)).fetchall()

def get_category_recipes(category_id):
    sql = """SELECT id, name FROM recipes
            WHERE id=:category_id AND visible=1"""
    return db.session.execute(text(sql), {"category_id":category_id}).fetchall()

def get_category_id(category_name):
    sql = "SELECT id FROM categories WHERE category_name=:category_name"
    return db.session.execute(text(sql), {"category_name":category_name}).fetchone()

def get_category_info(category_id):
    sql = "SELECT name, id FROM categories WHERE id=:category_id"
    return db.session.execute(text(sql), {"category_id":category_id}).fetchone()[0]

def new_category(name):
    sql = "INSERT INTO categories (name, visible) VALUES(:name, 1) RETURNING id"
    category_id = db.session.execute(text(sql), {"name":name}).fetchone()[0]
    db.session.commit()
    return category_id

def remove_category(category_id):
    sql = "UPDATE categories SET visible=0 WHERE id=:id"
    db.session.execute(text(sql), {"id":category_id})
    db.session.commit()

def add_review(recipe_id, user_id, stars, comment):
    sql = """INSERT INTO reviews (recipe_id, user_id, stars, comment)
            VALUES (:recipe_id, :user_id, :stars, :comment)"""
    review_id = db.session.execute(text(sql), {"recipe_id":recipe_id, "user_id":user_id, "stars":stars, "comment":comment})
    db.session.commit()
    return review_id

def get_reviews(recipe_id):
    sql = """SELECT U.username, R.stars, R.comment FROM reviews R, users U
            WHERE R.user_id=U.id AND R.recipe_id=:recipe_id ORDER BY R.id"""
    return db.session.execute(text(sql), {"recipe_id":recipe_id}).fetchall()

def result(query):
    sql = "SELECT id, name FROM recipes WHERE name LIKE :query OR ingredients LIKE :query OR instructions LIKE :query AND visible=1"
    return db.session.execute(text(sql), {"query":"%"+query+"%"}).fetchall()

def add_favorite(recipe_id, user_id):
    sql = """INSERT INTO favorites (recipe_id, user_id)
           VALUES (:recipe_id, :user_id)"""
    favorite_id = db.session.execute(text(sql), {"recipe_id":recipe_id, "user_id":user_id})
    db.session.commit()
    return favorite_id 

def favorites(user_id):
    sql = """SELECT R.id, R.name, U.id FROM recipes R, favorites F, users U
            WHERE R.id = F.recipe_id AND F.user_id=U.id AND U.id=:user_id AND visible=1
            ORDER BY R.name"""
    return db.session.execute(text(sql), {"user_id":user_id}).fetchall()