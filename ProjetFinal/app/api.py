from flask import Flask, jsonify, request, abort, send_file
from src.Controlleur import *
import io
import sys
import os

app = Flask(__name__)

@app.get('/')
def index():
    return jsonify({
        "message": "Bienvenue à l'API d'analyse des données sportives et de productivité.",
        "endpoints": {
            "/api/v1/analyses/sport/lineaire": "Analyse des activités sportives linéaire",
            "/api/v1/analyses/sport/multivariee": "Analyse des activités sportives multivariée",
            "/api/v1/analyses/travail": "Analyse des données de productivité au travail",
            "/api/v1/analyses/images/regressionSimple/<string:activite>": "Obtenir l'image de la régression linéaire simple pour une activité donnée (course, velo, natation, productivite)",
            "/api/v1/analyses/images/regressionMultiple/<string:activite>": "Obtenir l'image de la régression linéaire multiple pour une activité donnée (course, velo, natation)",
            "/api/v1/analyses/images/polynome/<string:activite>": "Obtenir l'image de la régression polynomiale pour une activité donnée (productivite)",
            "/api/v1/analyses/sport-cafe-lendemain": "Analyse du sport et consommation de café le lendemain",
            "/api/v1/analyses/actif-productivite": "Analyse de l'activité physique vs productivité",
            "/api/v1/analyses/surcharge-productivite": "Analyse de la surcharge de travail vs productivité",
            "/api/v1/analyses/equilibre-temps-productivite": "Analyse de l'équilibre du temps vs productivité",
            "/api/v1/analyses/correlation-calories-cafe": "Analyse de la corrélation entre calories brûlées et consommation de café",
            "/api/v1/analyses/sportifs-consommation-cafe": "Analyse de la consommation de café chez les sportifs"
        }
    })


@app.get('/api/v1/analyses/sport/lineaire')
def routeAnalyseSportLineaire():
    try:
        res = analyseSportLineaire()
        
        return jsonify(res), 200
        
    except Exception as e:
       abort(400, description=str(e))


@app.get('/api/v1/analyses/sport/multivariee')
def routeAnalyseSportMultivariee():
    try:
        res = analyseSportMultivariee()
        
        return jsonify(res), 200
        
    except Exception as e:
       abort(400, description=str(e))


@app.get('/api/v1/analyses/travail')
def routeAnalyseTravail():
    try:
        res = analyseTravail()
        
        return jsonify(res), 200
        
    except Exception as e:
       abort(400, description=str(e))


@app.get('/api/v1/analyses/images/regressionSimple/<string:activite>')
def routeGetImageRegressionSimple(activite):
    try:
        print("Activité demandée :", activite)
        activite = activite.lower()

        if activite not in ['course', 'velo', 'natation', 'productivite']:
            abort(400, description="Activité invalide. Choisissez parmi 'course', 'velo', 'natation' ou 'productivite'.")

        # Chemin vers l'image
        image_path = f'./resultats/RegressionLineaire_{activite}.png'
        
        # Vérifier si le fichier existe
        if not os.path.exists(image_path):
            abort(404, description="Image not found")
        
        return send_file(image_path, mimetype='image/png')
        
    except FileNotFoundError:
        abort(404, description=f"Image RegressionLineaire_{activite}.png introuvable")
    except Exception as e:
        abort(500, description=str(e))


@app.get('/api/v1/analyses/images/regressionMultiple/<string:activite>')
def routeGetImageRegressionMultiple(activite):
    try:
        print("Activité demandée :", activite)
        activite = activite.lower()

        if activite not in ['course', 'velo', 'natation']:
            abort(400, description="Activité invalide. Choisissez parmi 'course', 'velo', ou 'natation'.")

        # Chemin vers l'image
        image_path = f'./resultats/RegressionLineaireMultivariée_{activite}.png'
        
        # Vérifier si le fichier existe
        if not os.path.exists(image_path):
            abort(404, description="Image not found")
        
        return send_file(image_path, mimetype='image/png')
        
    except FileNotFoundError:
        abort(404, description=f"Image RegressionLineaire_{activite}.png introuvable")
    except Exception as e:
        abort(500, description=str(e))


@app.get('/api/v1/analyses/images/polynome/<string:activite>')
def routeGetImagePolynome(activite):
    try:
        print("Activité demandée :", activite)
        activite = activite.lower()

        if activite not in ['productivite']:
            abort(400, description="Activité invalide. Choisissez parmi 'productivite'.")

        # Chemin vers l'image
        image_path = f'./resultats/RegressionPolynomiale_{activite}.png'
        
        # Vérifier si le fichier existe
        if not os.path.exists(image_path):
            abort(404, description="Image not found")
        
        return send_file(image_path, mimetype='image/png')
        
    except FileNotFoundError:
        abort(404, description=f"Image RegressionLineaire_{activite}.png introuvable")
    except Exception as e:
        abort(500, description=str(e))



@app.get('/api/v1/analyses/sport-cafe-lendemain')
def routeAnalyseSportEtCafeLendemain():
    try:
        res = analyseSportEtCafeLendemain()
        
        return jsonify(res), 200
        
    except Exception as e:
       abort(400, description=str(e))


@app.get('/api/v1/analyses/actif-productivite')
def routeAnalyseActifProductivite():
    try:
        res = analyseActifProductivite()
        
        return jsonify(res), 200
        
    except Exception as e:
       abort(400, description=str(e))


@app.get('/api/v1/analyses/surcharge-productivite')
def routeAnalyseSurchargeProductivite():
    try:
        res = analyseSurchargeProductivite()
        
        return jsonify(res), 200
        
    except Exception as e:
       abort(400, description=str(e))


@app.get('/api/v1/analyses/equilibre-temps-productivite')
def routeAnalyseEquilibreTempsProductivite():
    try:
        res = analyseEquilibreTempsProductivite()
        
        return jsonify(res), 200
        
    except Exception as e:
       abort(400, description=str(e))


@app.get('/api/v1/analyses/correlation-calories-cafe')
def routeAnalyseCorrelationCaloriesCafe():
    try:
        res = analyseCorrelationCaloriesCafe()
        
        return jsonify(res), 200
        
    except Exception as e:
       abort(400, description=str(e))


@app.get('/api/v1/analyses/sportifs-consommation-cafe')
def routeAnalyseeSportifsConsommationCafe():
    try:
        res = analyseeSportifsConsommationCafe()
        
        return jsonify(res), 200
        
    except Exception as e:
       abort(400, description=str(e))


@app.errorhandler(400)
def handle_bad_request(err):
    return jsonify(error=err.description or str(err)), err.code

@app.errorhandler(404)
def handle_not_found(err):
    return jsonify(error=err.description or str(err)), err.code

@app.errorhandler(500)
def handle_internal_error(err):
    return jsonify(error=err.description or str(err)), err.code


if __name__ == "__main__":
    print("### Starting API ###")
    app.run(host='0.0.0.0', port=5000, debug=True)