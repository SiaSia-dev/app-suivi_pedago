import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Classe pour gérer les données des apprenants
class SuiviPedagogique:
    def __init__(self):
        # Simulation de base de données des apprenants
        self.apprenants = pd.DataFrame(columns=[
            'id', 'nom', 'prenom', 'cours', 'progression', 
            'derniere_connexion', 'temps_total_etude', 
            'niveau_engagement', 'alertes'
        ])
    
    def generer_donnees_test(self):
        """Génère des données de test pour démonstration"""
        noms = ['Dupont', 'Martin', 'Dubois', 'Leroy', 'Moreau']
        prenoms = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Lucas']
        cours = ['Python Débutant', 'Data Science', 'Web Development', 'IA et Machine Learning']
        
        donnees = []
        for i in range(len(noms)):
            progression = np.random.randint(0, 101)
            temps_etude = np.random.randint(10, 500)
            derniere_connexion = datetime.now() - timedelta(days=np.random.randint(0, 30))
            
            # Calcul du niveau d'engagement
            if progression < 30:
                niveau_engagement = 'Faible'
                alertes = ['Progression très lente']
            elif progression < 60:
                niveau_engagement = 'Moyen'
                alertes = ['Progression à surveiller']
            else:
                niveau_engagement = 'Élevé'
                alertes = []
            
            donnees.append({
                'id': i+1,
                'nom': noms[i],
                'prenom': prenoms[i],
                'cours': np.random.choice(cours),
                'progression': progression,
                'derniere_connexion': derniere_connexion,
                'temps_total_etude': temps_etude,
                'niveau_engagement': niveau_engagement,
                'alertes': ', '.join(alertes) if alertes else 'Aucune'
            })
        
        self.apprenants = pd.DataFrame(donnees)
        return self.apprenants
    
    def generer_rapport_global(self):
        """Génère un rapport d'analyse global"""
        rapport = {
            'total_apprenants': len(self.apprenants),
            'progression_moyenne': self.apprenants['progression'].mean(),
            'repartition_engagement': self.apprenants['niveau_engagement'].value_counts(),
            'temps_moyen_etude': self.apprenants['temps_total_etude'].mean()
        }
        return rapport
    
    def identifier_apprenants_difficultes(self):
        """Identifie les apprenants ayant besoin de support"""
        return self.apprenants[
            (self.apprenants['progression'] < 30) | 
            (self.apprenants['derniere_connexion'] < datetime.now() - timedelta(days=15))
        ]

# Interface Streamlit
def main():
    st.title('Système de Suivi Pédagogique Personnalisé')
    
    # Initialisation du système de suivi
    if 'suivi' not in st.session_state:
        st.session_state.suivi = SuiviPedagogique()
        st.session_state.donnees = st.session_state.suivi.generer_donnees_test()
    
    # Menu de navigation
    menu = st.sidebar.selectbox('Navigation', [
        'Tableau de Bord Principal', 
        'Détails des Apprenants', 
        'Rapports et Analyses', 
        'Alertes et Accompagnement'
    ])
    
    if menu == 'Tableau de Bord Principal':
        st.header('Tableau de Bord Principal')
        
        # Statistiques globales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Total Apprenants', len(st.session_state.donnees))
        with col2:
            st.metric('Progression Moyenne', f"{st.session_state.donnees['progression'].mean():.1f}%")
        with col3:
            st.metric('Temps Moyen d\'Étude', f"{st.session_state.donnees['temps_total_etude'].mean():.0f} min")
        
        # Visualisation de la répartition des engagements
        st.subheader('Répartition des Niveaux d\'Engagement')
        fig, ax = plt.subplots()
        st.session_state.donnees['niveau_engagement'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
        st.pyplot(fig)
    
    elif menu == 'Détails des Apprenants':
        st.header('Liste des Apprenants')
        
        # Filtres interactifs
        col1, col2 = st.columns(2)
        with col1:
            cours_selectionne = st.selectbox('Filtrer par Cours', 
                ['Tous'] + list(st.session_state.donnees['cours'].unique()))
        with col2:
            niveau_engagement = st.selectbox('Filtrer par Niveau d\'Engagement', 
                ['Tous', 'Faible', 'Moyen', 'Élevé'])
        
        # Filtrage des données
        donnees_filtrees = st.session_state.donnees.copy()
        if cours_selectionne != 'Tous':
            donnees_filtrees = donnees_filtrees[donnees_filtrees['cours'] == cours_selectionne]
        if niveau_engagement != 'Tous':
            donnees_filtrees = donnees_filtrees[donnees_filtrees['niveau_engagement'] == niveau_engagement]
        
        st.dataframe(donnees_filtrees)
    
    elif menu == 'Rapports et Analyses':
        st.header('Rapports Détaillés')
        
        # Rapport global
        rapport = st.session_state.suivi.generer_rapport_global()
        st.subheader('Synthèse Globale')
        st.write(f"Nombre total d'apprenants : {rapport['total_apprenants']}")
        st.write(f"Progression moyenne : {rapport['progression_moyenne']:.1f}%")
        
        # Répartition des engagements
        st.subheader('Répartition des Engagements')
        st.bar_chart(rapport['repartition_engagement'])
    
    elif menu == 'Alertes et Accompagnement':
        st.header('Apprenants Nécessitant un Accompagnement')
        
        # Identification des apprenants en difficulté
        apprenants_difficultes = st.session_state.suivi.identifier_apprenants_difficultes()
        
        if len(apprenants_difficultes) > 0:
            st.warning(f"{len(apprenants_difficultes)} apprenants nécessitent un suivi personnalisé")
            st.dataframe(apprenants_difficultes)
            
            # Bouton d'action
            if st.button('Générer Rapport d\'Intervention'):
                st.success('Rapport d\'intervention généré pour les apprenants identifiés')
        else:
            st.success('Aucun apprenant ne nécessite actuellement un accompagnement spécifique')

# Point d'entrée de l'application
if __name__ == '__main__':
    main()

# Instructions d'installation
"""
Il s'agit d'un prototype d'application de suivi pédagogique personnalisé pour les apprenants.
"""
