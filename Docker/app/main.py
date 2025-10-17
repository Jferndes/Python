from flask import Flask, jsonify, request, abort, send_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import io

app = Flask(__name__)

def load_data():
    # Charger les données depuis un fichier CSV
    df = pd.read_csv('app/score.csv')
    return df

@app.get('/api/v1/scores')
def get_scores():
    df = load_data()
    if df.empty:
        return abort(404, description="No data available")
    else:
        return jsonify(df.to_dict(orient='records')), 200

@app.get('/api/v1/scores/stats')
def get_stats():
    df = load_data()
    if df.empty:
        return abort(404, description="No data available")
    else:
        stats = {
            "mean": df['score'].mean(),
            "median": df['score'].median(),
            "std": df['score'].std() 
        }
        return jsonify(stats), 200

@app.get('/api/v1/scores/<int:score_id>')
def get_score_superior(score_id):
    df = load_data()
    if df.empty:
        return abort(404, description="No data available")
    else:
        filtered_df = df[df['score'] > score_id]
        if filtered_df.empty:
            return abort(404, description="No scores found above the given ID")
        return jsonify(filtered_df.to_dict(orient='records')), 200


@app.post('/api/v1/scores')
def add_newScore():
    data = request.get_json(silent=True) or {}
    nom = data.get("nom")
    age = data.get("age")
    score = data.get("score")

    if nom is None:
        abort(400, description="Champ 'nom' requis")
    if age is None:
        abort(400, description="Champ 'age' requis")
    if score is None:
        abort(400, description="Champ 'score' requis")
    

    df = load_data()
    new_id = int(df['id'].max() + 1) if not df.empty else 1

    new_entry = {"id": new_id, "nom": nom, "age": age, "score": score}
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv('app/score.csv', index=False)

    return jsonify(new_entry), 201

@app.get('/api/v1/scores/histogram')
def get_histogram():
    df = load_data()
    if df.empty:
        return abort(404, description="No data available")
    else:
        histogram, bin_edges = np.histogram(df['score'], bins=10, range=(0, 100))
        hist_data = {
            "histogram": histogram.tolist(),
            "bin_edges": bin_edges.tolist()
        }
        return jsonify(hist_data), 200

@app.get('/api/v2/scores/histogram')
def get_histogramV2():
    df = load_data()
    if df.empty:
        return abort(404, description="No data available")
    
    # Créer l'histogramme
    plt.figure(figsize=(10, 6))
    plt.hist(df['score'], bins=10, range=(0, 100), color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Score')
    plt.ylabel('Fréquence')
    plt.title('Distribution des Scores')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Sauvegarder le graphique dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return send_file(buf, mimetype='image/png')

@app.get('/api/v1/scores/regression')
def get_regression_plot():
    df = load_data()
    if df.empty:
        return abort(404, description="No data available")
    
    # Préparer les données pour la régression
    X = df['id'].values
    y = df['score'].values
    
    # Calculer la régression linéaire avec scipy
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)
    y_pred = slope * X + intercept
    
    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', alpha=0.6, label='Scores')
    plt.plot(X, y_pred, color='red', linewidth=2, label=f'Régression linéaire (y = {slope:.2f}x + {intercept:.2f}, R² = {r_value**2:.3f})')
    plt.xlabel('ID')
    plt.ylabel('Score')
    plt.title('Scores avec Régression Linéaire')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Sauvegarder le graphique dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)