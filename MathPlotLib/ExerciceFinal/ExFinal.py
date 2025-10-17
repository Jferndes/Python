"""
Exercice Final - Analyse du dataset environnemental
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit

# ============================================================================
# 1. CHARGEMENT ET NETTOYAGE DES DONNÉES
# ============================================================================

print("="*80)
print("1. NETTOYAGE DES DONNÉES")
print("="*80)

# Charger les données
df = pd.read_csv('../Data/environment_dataset.csv')

print("\nAperçu des données brutes:")
print(df.head())
print(f"\nDimensions: {df.shape}")
print(f"\nValeurs manquantes:\n{df.isnull().sum()}")

# Convertir la date en datetime
df['Date'] = pd.to_datetime(df['Date'])

# Remplacer les NaN par la moyenne par ville
df['Température'] = df.groupby('Ville')['Température'].transform(
    lambda x: x.fillna(x.mean())
)
df['Pollution'] = df.groupby('Ville')['Pollution'].transform(
    lambda x: x.fillna(x.mean())
)

# Trier par date
df = df.sort_values('Date').reset_index(drop=True)

print(f"\nAprès nettoyage - Valeurs manquantes:\n{df.isnull().sum()}")

# ============================================================================
# 2. STATISTIQUES DE BASE
# ============================================================================

print("\n" + "="*80)
print("2. STATISTIQUES DE BASE")
print("="*80)

# Statistiques par ville
stats_by_city = df.groupby('Ville').agg({
    'Température': ['mean', 'std', 'min', 'max'],
    'Pollution': ['mean', 'std', 'min', 'max']
})

print("\nStatistiques par ville:")
print(stats_by_city)

# Journée la plus chaude
jour_plus_chaud = df.loc[df['Température'].idxmax()]
print(f"\nJournée la plus chaude:")
print(f"Date: {jour_plus_chaud['Date']}, Ville: {jour_plus_chaud['Ville']}, Temp: {jour_plus_chaud['Température']:.2f}°C")

# Journée la plus polluée
jour_plus_pollue = df.loc[df['Pollution'].idxmax()]
print(f"\nJournée la plus polluée:")
print(f"Date: {jour_plus_pollue['Date']}, Ville: {jour_plus_pollue['Ville']}, Pollution: {jour_plus_pollue['Pollution']:.2f}")

# Corrélation température/pollution
correlation = df['Température'].corr(df['Pollution'])
print(f"\nCorrélation Température vs Pollution: {correlation:.4f}")

# ============================================================================
# 3. VISUALISATIONS
# ============================================================================

print("\n" + "="*80)
print("3. VISUALISATIONS")
print("="*80)

# Préparer les données mensuelles
df['Mois'] = df['Date'].dt.to_period('M')
monthly_data = df.groupby('Mois').agg({
    'Température': 'mean',
    'Pollution': 'mean'
}).reset_index()
monthly_data['Mois'] = monthly_data['Mois'].dt.to_timestamp()

# Graphique 1: Évolution mensuelle
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.plot(monthly_data['Mois'], monthly_data['Température'], 'r-', linewidth=2, marker='o')
ax1.set_xlabel('Mois')
ax1.set_ylabel('Température (°C)', color='r')
ax1.set_title('Évolution mensuelle moyenne de la température')
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='y', labelcolor='r')

ax2.plot(monthly_data['Mois'], monthly_data['Pollution'], 'b-', linewidth=2, marker='s')
ax2.set_xlabel('Mois')
ax2.set_ylabel('Pollution', color='b')
ax2.set_title('Évolution mensuelle moyenne de la pollution')
ax2.grid(True, alpha=0.3)
ax2.tick_params(axis='y', labelcolor='b')

plt.tight_layout()
plt.savefig('evolution_mensuelle.png', dpi=300, bbox_inches='tight')
plt.show()

# Graphique 2: Nuage de points avec régression linéaire
fig, ax = plt.subplots(figsize=(10, 6))

# Nuage de points
ax.scatter(df['Température'], df['Pollution'], alpha=0.5, s=20)

# Régression linéaire
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Température'], df['Pollution'])
x_line = np.array([df['Température'].min(), df['Température'].max()])
y_line = slope * x_line + intercept

ax.plot(x_line, y_line, 'r-', linewidth=2, label=f'y = {slope:.2f}x + {intercept:.2f}\nR² = {r_value**2:.4f}')

ax.set_xlabel('Température (°C)')
ax.set_ylabel('Pollution')
ax.set_title('Température vs Pollution avec régression linéaire')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('temperature_vs_pollution.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================================================
# 4. STATISTIQUES AVANCÉES
# ============================================================================

print("\n" + "="*80)
print("4. STATISTIQUES AVANCÉES")
print("="*80)

# Test t entre deux villes
villes = df['Ville'].unique()
if len(villes) >= 2:
    ville1, ville2 = villes[0], villes[1]
    pollution_ville1 = df[df['Ville'] == ville1]['Pollution']
    pollution_ville2 = df[df['Ville'] == ville2]['Pollution']
    
    t_stat, p_value = stats.ttest_ind(pollution_ville1, pollution_ville2)
    print(f"\nTest t - Pollution {ville1} vs {ville2}:")
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.4f}")
    print(f"Différence significative: {'Oui' if p_value < 0.05 else 'Non'} (α=0.05)")

# Test de normalité (Shapiro-Wilk)
shapiro_stat, shapiro_p = stats.shapiro(df['Pollution'].sample(min(5000, len(df))))
print(f"\nTest de Shapiro-Wilk (normalité de la pollution):")
print(f"Statistique: {shapiro_stat:.4f}")
print(f"p-value: {shapiro_p:.4f}")
print(f"Distribution normale: {'Oui' if shapiro_p > 0.05 else 'Non'} (α=0.05)")

# Corrélation de Pearson
pearson_corr, pearson_p = stats.pearsonr(df['Température'], df['Pollution'])
print(f"\nCorrélation de Pearson:")
print(f"Coefficient: {pearson_corr:.4f}")
print(f"p-value: {pearson_p:.4f}")

# ============================================================================
# 5. MODÉLISATION SIMPLE
# ============================================================================

print("\n" + "="*80)
print("5. MODÉLISATION SINUSOÏDALE")
print("="*80)

# Fonction sinusoïdale: T(t) = A * sin(2π/365 * t + φ) + B
def temp_model(t, A, phi, B):
    return A * np.sin(2 * np.pi / 365 * t + phi) + B

# Calculer le jour de l'année
df['Jour_annee'] = df['Date'].dt.dayofyear

# Température moyenne par jour de l'année
temp_by_day = df.groupby('Jour_annee')['Température'].mean().reset_index()

# Ajuster le modèle
popt, pcov = curve_fit(temp_model, temp_by_day['Jour_annee'], temp_by_day['Température'], 
                       p0=[10, 0, 15])

A, phi, B = popt
print(f"\nParamètres du modèle sinusoïdal:")
print(f"Amplitude (A): {A:.2f}")
print(f"Phase (φ): {phi:.2f}")
print(f"Température moyenne (B): {B:.2f}")

# Visualisation
fig, ax = plt.subplots(figsize=(12, 6))

# Données réelles
ax.scatter(temp_by_day['Jour_annee'], temp_by_day['Température'], 
          alpha=0.5, s=20, label='Données observées')

# Modèle
t_model = np.linspace(1, 365, 365)
temp_pred = temp_model(t_model, A, phi, B)
ax.plot(t_model, temp_pred, 'r-', linewidth=2, 
       label=f'Modèle: {A:.2f}sin(2π/365*t + {phi:.2f}) + {B:.2f}')

ax.set_xlabel('Jour de l\'année')
ax.set_ylabel('Température (°C)')
ax.set_title('Modèle sinusoïdal de la température')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('modele_sinusoidal.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*80)
print("ANALYSE TERMINÉE")
print("="*80)