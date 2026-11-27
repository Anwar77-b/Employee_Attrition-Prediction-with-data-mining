# Guide utilisateur — Console Attrition RH

Cette console Streamlit expose huit écrans autour d'un jeu synthétique de 10 000 collaborateurs. Elle affiche les résultats produits par le pipeline ; elle ne réentraîne pas les modèles et ne recalcule pas les métriques.

> [!WARNING]
> Jeu académique et fictif. Aucune prédiction ne doit fonder une décision RH réelle.

---

## 1. Installation et lancement

Depuis la racine du dépôt :

```bash
python -m venv venv
venv\Scripts\activate          # Linux/macOS : source venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app/Home.py
```

Ouvrir ensuite `http://localhost:8501`. Si le port est occupé, Streamlit propose `http://localhost:8502`, ou lancer :

```bash
python -m streamlit run app/Home.py --server.port 8502
```

Les dépendances sont celles du projet ; aucune installation supplémentaire n'est requise pour l'interface. La configuration visuelle se trouve dans `.streamlit/config.toml` et la charte dans [`app/theme.py`](../app/theme.py).

---

## 2. Les huit écrans

| Écran | Fichier | Contenu |
|---|---|---|
| Accueil | [`app/Home.py`](../app/Home.py) | KPI globaux (10 000 collaborateurs, 9,03 % d'attrition, salaire et ancienneté moyens) et navigation vers les sept autres écrans. |
| Qualité & outliers | [`app/pages/0_Qualite_Donnees.py`](../app/pages/0_Qualite_Donnees.py) | Manquants, doublons, plages et lecture de [`results/outliers_report.csv`](../results/outliers_report.csv) (Z-score, IQR, Isolation Forest, LOF). |
| Exploration RH | [`app/pages/1_Dashboard.py`](../app/pages/1_Dashboard.py) | Filtres Department / OverTime / promotion / âge / revenu, distributions, fréquences, corrélations de Spearman et tests statistiques. |
| Prédiction individuelle | [`app/pages/2_Prediction.py`](../app/pages/2_Prediction.py) | Formulaire des 12 variables, jauge de risque, badge coloré, recommandations et simulation « What-if ». |
| Performance modèles | [`app/pages/3_Performance_Modeles.py`](../app/pages/3_Performance_Modeles.py) | Comparaison des six algorithmes, validation croisée à 5 plis, ROC/PR et matrices de confusion. |
| Facteurs de démission | [`app/pages/4_Facteurs_Demission.py`](../app/pages/4_Facteurs_Demission.py) | Importance des variables et explications SHAP. |
| Prédiction en lot | [`app/pages/5_Prediction_en_lot.py`](../app/pages/5_Prediction_en_lot.py) | Trame CSV, téléversement, contrôle des colonnes, aperçu et export des scores. |
| À propos | [`app/pages/6_A_Propos.py`](../app/pages/6_A_Propos.py) | CRISP-DM, dictionnaire des variables, contrat modèle, éthique et limites. |

Chaque écran applique la même charte : fond sombre, grille discrète, panneaux, en-têtes avec séparateur lumineux, cartes de métriques, onglets, alertes et pied de page identique.

---

## 3. Saisie manuelle des 12 variables

Le formulaire de prédiction individuelle attend exactement les colonnes déclarées dans `src.preprocessing.FEATURE_COLS` :

| Type | Variables |
|---|---|
| Quantitatives | `Age`, `YearsAtCompany`, `MonthlyIncome`, `DistanceFromHome`, `TrainingHoursLastYear` |
| Ordinales | `JobLevel`, `JobSatisfaction`, `WorkLifeBalance`, `PerformanceRating` |
| Binaires | `OverTime`, `PromotionLast5Years` |
| Nominale | `Department` |

`EmployeeID` n'apparaît pas dans le formulaire et n'est jamais transmis au modèle. `Attrition` est la cible : elle n'est jamais proposée comme entrée. Le détail des échelles figure dans [`docs/data_dictionary.md`](data_dictionary.md).

Le résultat affiche une probabilité de départ, un libellé de risque (`Faible`, `Modéré`, `Élevé`) et des pistes d'action formulées à partir des variables saisies. Ces pistes sont des repères pédagogiques, pas des prescriptions.

---

## 4. Prédiction en lot

La trame téléchargeable contient uniquement les 12 colonnes ci-dessus. Si un fichier importé contient `EmployeeID` ou `Attrition`, ces colonnes sont retirées dès la lecture : elles ne sont jamais utilisées comme variables, affichées ni exportées.

- Taille maximale acceptée : 50 Mo (configuration Streamlit).
- Volume recommandé : 100 000 lignes maximum pour préserver la lisibilité de l'aperçu.
- Colonnes manquantes : signalées dans une alerte avant toute prédiction.
- Colonnes supplémentaires : ignorées après avertissement.
- Export : CSV des lignes avec probabilité, niveau de risque et sortie `Yes`/`No`.

Le tri s'effectue par probabilité de `Yes` décroissante.

---

## 5. Artefacts absents

Si `models/best_model.joblib` n'existe pas, les pages de prédiction affichent un avertissement et proposent la commande de régénération :

```bash
python scripts/train_pipeline.py
```

Le reste de la console reste utilisable : données, qualité, exploration, documentation et comparaison des fichiers de résultats présents. Aucun score n'est inventé. Pour régénérer le rapport outliers :

```bash
python scripts/run_outliers.py
```

La méthodologie associée est décrite dans [`docs/OUTLIERS.md`](OUTLIERS.md).

---

## 6. Éthique et limites

- Jeu synthétique : aucune donnée personnelle réelle n'est traitée.
- Aucun nom, prénom, matricule ni e-mail personnel n'est affiché ou enregistré par l'interface.
- Les scores sont associatifs, non causaux ; le signal prédictif reste faible (classe positive d'environ 9 %).
- Aucune décision RH n'est automatisée : la console est un outil d'aide à la réflexion.
- Les métriques affichées proviennent des artefacts existants et ne sont pas recalculées ; voir [`docs/METRIQUES.md`](METRIQUES.md).

---

## 7. Dépannage

| Symptôme | Action |
|---|---|
| `ModuleNotFoundError: app` | Lancer la commande depuis la racine du dépôt. |
| Port 8501 indisponible | Utiliser `--server.port 8502`. |
| `Employee_Attrition_DataSet.csv` introuvable | Vérifier `data/raw/` ; l'accueil affiche un avertissement explicite. |
| Modèle indisponible | Lancer `python scripts/train_pipeline.py`, puis rafraîchir la page. |
| Rapport outliers absent | Lancer `python scripts/run_outliers.py`. |
| CSV de lot invalide | Vérifier les 12 colonnes et les modalités `Yes`/`No` ; l'application liste les colonnes manquantes. |
| Graphiques vides | Ajuster les filtres de la barre latérale ; un effectif filtré à zéro est signalé par une alerte. |

La navigation latérale indique en continu si le jeu est chargé, si le modèle est disponible ou si un artefact de test explicite est détecté.
