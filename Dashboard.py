# dashboard_madagascar.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import random
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Économique Madagascar - Analyse en Temps Réel",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #007E3A, #FC3D32, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .live-badge {
        background: linear-gradient(45deg, #007E3A, #00A859);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #007E3A;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #007E3A;
        border-bottom: 2px solid #FC3D32;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .stock-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #007E3A;
        background-color: #f8f9fa;
    }
    .price-change {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .positive { background-color: #d4edda; border-left: 4px solid #28a745; color: #155724; }
    .negative { background-color: #f8d7da; border-left: 4px solid #dc3545; color: #721c24; }
    .neutral { background-color: #e2e3e5; border-left: 4px solid #6c757d; color: #383d41; }
    .sector-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

class MadagascarDashboard:
    def __init__(self):
        self.entreprises = self.define_entreprises()
        self.historical_data = self.initialize_historical_data()
        self.current_data = self.initialize_current_data()
        self.sector_data = self.initialize_sector_data()
        self.economic_data = self.initialize_economic_data()
        
    def define_entreprises(self):
        """Définit les principales entreprises malgaches"""
        return {
            'AIRMAD': {
                'nom_complet': 'Air Madagascar',
                'secteur': 'Transport',
                'sous_secteur': 'Aviation',
                'pays': 'Madagascar',
                'couleur': '#FF6B00',
                'poids_indice': 15.2,
                'market_cap': 120e6,
                'dividende_yield': 2.1,
                'volume_moyen': 45000,
                'description': 'Compagnie aérienne nationale'
            },
            'TELMA': {
                'nom_complet': 'Telma Madagascar',
                'secteur': 'Télécommunications',
                'sous_secteur': 'Télécom',
                'pays': 'Madagascar',
                'couleur': '#0066CC',
                'poids_indice': 22.5,
                'market_cap': 280e6,
                'dividende_yield': 3.8,
                'volume_moyen': 85000,
                'description': 'Leader des télécommunications'
            },
            'HVM': {
                'nom_complet': 'Habitation à Vendre Madagascar',
                'secteur': 'Immobilier',
                'sous_secteur': 'Promotion immobilière',
                'pays': 'Madagascar',
                'couleur': '#8B4513',
                'poids_indice': 8.7,
                'market_cap': 45e6,
                'dividende_yield': 4.2,
                'volume_moyen': 25000,
                'description': 'Promoteur immobilier'
            },
            'STAR': {
                'nom_complet': 'Brasserie Star Madagascar',
                'secteur': 'Consommation',
                'sous_secteur': 'Boissons',
                'pays': 'Madagascar',
                'couleur': '#FFCC00',
                'poids_indice': 12.3,
                'market_cap': 95e6,
                'dividende_yield': 2.8,
                'volume_moyen': 55000,
                'description': 'Brasserie leader'
            },
            'SHERATON': {
                'nom_complet': 'Sheraton Madagascar',
                'secteur': 'Tourisme',
                'sous_secteur': 'Hôtellerie',
                'pays': 'Madagascar',
                'couleur': '#004B87',
                'poids_indice': 6.8,
                'market_cap': 65e6,
                'dividende_yield': 1.9,
                'volume_moyen': 32000,
                'description': 'Chaîne hôtelière internationale'
            },
            'BOA': {
                'nom_complet': 'Bank of Africa Madagascar',
                'secteur': 'Finance',
                'sous_secteur': 'Banque',
                'pays': 'Madagascar',
                'couleur': '#660099',
                'poids_indice': 18.4,
                'market_cap': 150e6,
                'dividende_yield': 5.1,
                'volume_moyen': 68000,
                'description': 'Institution bancaire majeure'
            },
            'BFV': {
                'nom_complet': 'BFV-SG Madagascar',
                'secteur': 'Finance',
                'sous_secteur': 'Banque',
                'pays': 'Madagascar',
                'couleur': '#EF4135',
                'poids_indice': 16.1,
                'market_cap': 135e6,
                'dividende_yield': 4.8,
                'volume_moyen': 62000,
                'description': 'Banque commerciale'
            },
            'MCL': {
                'nom_complet': 'Madagascar Consolidated Mining',
                'secteur': 'Mines',
                'sous_secteur': 'Extraction minière',
                'pays': 'Madagascar',
                'couleur': '#FF69B4',
                'poids_indice': 9.5,
                'market_cap': 75e6,
                'dividende_yield': 3.2,
                'volume_moyen': 38000,
                'description': 'Compagnie minière'
            },
            'SOTRAMA': {
                'nom_complet': 'Sotrama Motors',
                'secteur': 'Industrie',
                'sous_secteur': 'Automobile',
                'pays': 'Madagascar',
                'couleur': '#00A3E0',
                'poids_indice': 5.3,
                'market_cap': 35e6,
                'dividende_yield': 2.4,
                'volume_moyen': 18000,
                'description': 'Constructeur automobile local'
            },
            'AGRIKOR': {
                'nom_complet': 'Agrikor Madagascar',
                'secteur': 'Agriculture',
                'sous_secteur': 'Agro-industrie',
                'pays': 'Madagascar',
                'couleur': '#28a745',
                'poids_indice': 7.2,
                'market_cap': 55e6,
                'dividende_yield': 3.5,
                'volume_moyen': 29000,
                'description': 'Entreprise agro-industrielle'
            }
        }
    
    def initialize_historical_data(self):
        """Initialise les données historiques des prix"""
        dates = pd.date_range('2020-01-01', datetime.now(), freq='D')
        data = []
        
        for date in dates:
            for symbole, info in self.entreprises.items():
                # Prix de base réaliste selon la capitalisation
                base_price = info['market_cap'] / 1e6 * random.uniform(0.1, 0.3)
                
                # Impact COVID (2020)
                if date.year == 2020 and date.month <= 6:
                    covid_impact = random.uniform(0.3, 0.6)
                elif date.year == 2020:
                    covid_impact = random.uniform(0.6, 0.9)
                elif date.year == 2021:
                    covid_impact = random.uniform(0.9, 1.2)
                else:
                    covid_impact = random.uniform(1.0, 1.4)
                
                # Volatilité quotidienne
                daily_volatility = random.uniform(0.92, 1.08)
                
                prix = base_price * covid_impact * daily_volatility * random.uniform(0.95, 1.05)
                volume = info['volume_moyen'] * random.uniform(0.3, 3.0)
                
                data.append({
                    'date': date,
                    'symbole': symbole,
                    'prix': prix,
                    'volume': volume,
                    'secteur': info['secteur'],
                    'market_cap': info['market_cap'] * random.uniform(0.9, 1.1)
                })
        
        return pd.DataFrame(data)
    
    def initialize_current_data(self):
        """Initialise les données courantes"""
        current_data = []
        for symbole, info in self.entreprises.items():
            # Dernier prix historique
            last_data = self.historical_data[self.historical_data['symbole'] == symbole].iloc[-1]
            
            # Variation quotidienne simulée
            change_pct = random.uniform(-0.08, 0.08)
            change_abs = last_data['prix'] * change_pct
            
            current_data.append({
                'symbole': symbole,
                'nom_complet': info['nom_complet'],
                'secteur': info['secteur'],
                'prix_actuel': last_data['prix'] + change_abs,
                'variation_pct': change_pct * 100,
                'variation_abs': change_abs,
                'volume': info['volume_moyen'] * random.uniform(0.5, 2.0),
                'market_cap': info['market_cap'],
                'dividende_yield': info['dividende_yield'],
                'poids_indice': info['poids_indice'],
                'ouverture': last_data['prix'] * random.uniform(0.95, 1.05),
                'plus_haut': last_data['prix'] * random.uniform(1.02, 1.08),
                'plus_bas': last_data['prix'] * random.uniform(0.92, 0.98)
            })
        
        return pd.DataFrame(current_data)
    
    def initialize_sector_data(self):
        """Initialise les données par secteur"""
        secteurs = list(set([info['secteur'] for info in self.entreprises.values()]))
        data = []
        
        for secteur in secteurs:
            entreprises_secteur = [s for s, info in self.entreprises.items() if info['secteur'] == secteur]
            poids_total = sum([self.entreprises[s]['poids_indice'] for s in entreprises_secteur])
            market_cap_total = sum([self.entreprises[s]['market_cap'] for s in entreprises_secteur])
            
            data.append({
                'secteur': secteur,
                'poids_indice': poids_total,
                'market_cap_total': market_cap_total,
                'nombre_entreprises': len(entreprises_secteur),
                'performance_moyenne': random.uniform(-3, 6)
            })
        
        return pd.DataFrame(data)
    
    def initialize_economic_data(self):
        """Initialise les données économiques de Madagascar"""
        dates = pd.date_range('2020-01-01', datetime.now(), freq='M')
        economic_data = []
        
        for date in dates:
            # Données économiques simulées mais réalistes pour Madagascar
            economic_data.append({
                'date': date,
                'inflation': random.uniform(5, 12),
                'croissance_pib': random.uniform(-8, 8),
                'taux_directeur': random.uniform(8, 12),
                'taux_change_usd': random.uniform(3800, 4500),
                'taux_change_eur': random.uniform(4200, 5000),
                'reserves_devises': random.uniform(800, 1500),
                'dette_publique': random.uniform(35, 45)
            })
        
        return pd.DataFrame(economic_data)
    
    def update_live_data(self):
        """Met à jour les données en temps réel"""
        for idx in self.current_data.index:
            symbole = self.current_data.loc[idx, 'symbole']
            
            # Simulation de variations de prix
            if random.random() < 0.4:  # 40% de chance de changement
                variation = random.uniform(-0.04, 0.04)
                nouveau_prix = self.current_data.loc[idx, 'prix_actuel'] * (1 + variation)
                
                self.current_data.loc[idx, 'prix_actuel'] = nouveau_prix
                self.current_data.loc[idx, 'variation_pct'] = variation * 100
                self.current_data.loc[idx, 'variation_abs'] = nouveau_prix - self.current_data.loc[idx, 'ouverture']
                
                # Mise à jour des plus hauts/plus bas
                if nouveau_prix > self.current_data.loc[idx, 'plus_haut']:
                    self.current_data.loc[idx, 'plus_haut'] = nouveau_prix
                if nouveau_prix < self.current_data.loc[idx, 'plus_bas']:
                    self.current_data.loc[idx, 'plus_bas'] = nouveau_prix
                
                # Mise à jour du volume
                self.current_data.loc[idx, 'volume'] *= random.uniform(0.8, 1.3)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🌍 Dashboard Économique Madagascar - Analyse en Temps Réel</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="live-badge">🔴 DONNÉES ÉCONOMIQUES EN TEMPS RÉEL</div>', 
                       unsafe_allow_html=True)
            st.markdown("**Surveillance et analyse des performances économiques et boursières de Madagascar**")
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_key_metrics(self):
        """Affiche les métriques clés économiques"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS ÉCONOMIQUES CLÉS</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des métriques
        indice_boursier = self.current_data['prix_actuel'].sum() / len(self.current_data) * 100
        variation_indice = self.current_data['variation_pct'].mean()
        volume_total = self.current_data['volume'].sum()
        entreprises_hausse = len(self.current_data[self.current_data['variation_pct'] > 0])
        
        # Dernières données économiques
        derniere_inflation = self.economic_data['inflation'].iloc[-1]
        derniere_croissance = self.economic_data['croissance_pib'].iloc[-1]
        dernier_taux_directeur = self.economic_data['taux_directeur'].iloc[-1]
        dernier_taux_change = self.economic_data['taux_change_usd'].iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Indice Boursier MVM",
                f"{indice_boursier:,.0f} pts",
                f"{variation_indice:+.2f}%",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                "Inflation (Dernier)",
                f"{derniere_inflation:.1f}%",
                f"{random.uniform(-0.5, 0.5):+.1f}% vs mois dernier"
            )
        
        with col3:
            st.metric(
                "Croissance PIB",
                f"{derniere_croissance:+.1f}%",
                f"{random.uniform(-2, 2):+.1f}% vs trimestre dernier"
            )
        
        with col4:
            st.metric(
                "Taux Change USD/MGA",
                f"{dernier_taux_change:,.0f} MGA",
                f"{random.uniform(-50, 50):+.0f} MGA"
            )
    
    def create_market_overview(self):
        """Crée la vue d'ensemble du marché malgache"""
        st.markdown('<h3 class="section-header">🏛️ VUE D\'ENSEMBLE DU MARCHÉ MALGACHE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Performance Indices", "Répartition Secteurs", "Top Performers", "Indicateurs Économiques"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution de l'indice boursier simulé
                indice_evolution = self.historical_data.groupby('date')['prix'].mean().reset_index()
                indice_evolution['indice'] = indice_evolution['prix'] * 100
                
                fig = px.line(indice_evolution, 
                             x='date', 
                             y='indice',
                             title='Évolution de l\'Indice Boursier (2020-2024)',
                             color_discrete_sequence=['#007E3A'])
                fig.update_layout(yaxis_title="Points d'Indice")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Performance par secteur
                fig = px.bar(self.sector_data, 
                            x='secteur', 
                            y='performance_moyenne',
                            title='Performance Moyenne par Secteur (%)',
                            color='secteur',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(yaxis_title="Performance (%)")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition par secteur
                fig = px.pie(self.sector_data, 
                            values='poids_indice', 
                            names='secteur',
                            title='Répartition de l\'Indice par Secteur',
                            color='secteur',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Capitalisation par secteur
                fig = px.bar(self.sector_data, 
                            x='secteur', 
                            y='market_cap_total',
                            title='Capitalisation Boursière par Secteur (Millions €)',
                            color='secteur',
                            color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(yaxis_title="Capitalisation (Millions €)")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Top gainers
                top_gainers = self.current_data.nlargest(5, 'variation_pct')
                fig = px.bar(top_gainers, 
                            x='variation_pct', 
                            y='symbole',
                            orientation='h',
                            title='Top 5 des Performances Positives (%)',
                            color='variation_pct',
                            color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top losers
                top_losers = self.current_data.nsmallest(5, 'variation_pct')
                fig = px.bar(top_losers, 
                            x='variation_pct', 
                            y='symbole',
                            orientation='h',
                            title='Top 5 des Performances Négatives (%)',
                            color='variation_pct',
                            color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            # Indicateurs économiques
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.line(self.economic_data, 
                             x='date', 
                             y='inflation',
                             title='Évolution de l\'Inflation (%)',
                             color_discrete_sequence=['#FF6B00'])
                st.plotly_chart(fig, use_container_width=True)
                
                fig = px.line(self.economic_data, 
                             x='date', 
                             y='taux_directeur',
                             title='Taux Directeur de la Banque Centrale (%)',
                             color_discrete_sequence=['#660099'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.line(self.economic_data, 
                             x='date', 
                             y='croissance_pib',
                             title='Croissance du PIB (%)',
                             color_discrete_sequence=['#007E3A'])
                st.plotly_chart(fig, use_container_width=True)
                
                fig = px.line(self.economic_data, 
                             x='date', 
                             y='taux_change_usd',
                             title='Taux de Change USD/MGA',
                             color_discrete_sequence=['#004B87'])
                st.plotly_chart(fig, use_container_width=True)
    
    def create_entreprises_live(self):
        """Affiche les entreprises en temps réel"""
        st.markdown('<h3 class="section-header">🏢 ENTREPRISES EN TEMPS RÉEL</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Tableau des Cours", "Analyse Secteur", "Screener"])
        
        with tab1:
            # Filtres pour les entreprises
            col1, col2, col3 = st.columns(3)
            with col1:
                secteur_filtre = st.selectbox("Secteur:", 
                                            ['Tous'] + list(self.sector_data['secteur'].unique()))
            with col2:
                performance_filtre = st.selectbox("Performance:", 
                                                ['Tous', 'En hausse', 'En baisse', 'Stable'])
            with col3:
                tri_filtre = st.selectbox("Trier par:", 
                                        ['Variation %', 'Volume', 'Capitalisation', 'Poids Indice'])
            
            # Application des filtres
            entreprises_filtrees = self.current_data.copy()
            if secteur_filtre != 'Tous':
                entreprises_filtrees = entreprises_filtrees[entreprises_filtrees['secteur'] == secteur_filtre]
            if performance_filtre == 'En hausse':
                entreprises_filtrees = entreprises_filtrees[entreprises_filtrees['variation_pct'] > 0]
            elif performance_filtre == 'En baisse':
                entreprises_filtrees = entreprises_filtrees[entreprises_filtrees['variation_pct'] < 0]
            elif performance_filtre == 'Stable':
                entreprises_filtrees = entreprises_filtrees[entreprises_filtrees['variation_pct'] == 0]
            
            # Tri
            if tri_filtre == 'Variation %':
                entreprises_filtrees = entreprises_filtrees.sort_values('variation_pct', ascending=False)
            elif tri_filtre == 'Volume':
                entreprises_filtrees = entreprises_filtrees.sort_values('volume', ascending=False)
            elif tri_filtre == 'Capitalisation':
                entreprises_filtrees = entreprises_filtrees.sort_values('market_cap', ascending=False)
            elif tri_filtre == 'Poids Indice':
                entreprises_filtrees = entreprises_filtrees.sort_values('poids_indice', ascending=False)
            
            # Affichage des entreprises
            for _, entreprise in entreprises_filtrees.iterrows():
                change_class = ""
                if entreprise['variation_pct'] > 0:
                    change_class = "positive"
                elif entreprise['variation_pct'] < 0:
                    change_class = "negative"
                else:
                    change_class = "neutral"
                
                col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
                with col1:
                    st.markdown(f"**{entreprise['symbole']}**")
                    st.markdown(f"*{entreprise['secteur']}*")
                with col2:
                    st.markdown(f"**{entreprise['nom_complet']}**")
                    st.markdown(f"Market Cap: {entreprise['market_cap']/1e6:.1f} M€")
                with col3:
                    st.markdown(f"**{entreprise['prix_actuel']:.2f}€**")
                    st.markdown(f"Div. Yield: {entreprise['dividende_yield']}%")
                with col4:
                    variation_str = f"{entreprise['variation_pct']:+.2f}%"
                    st.markdown(f"**{variation_str}**")
                    st.markdown(f"{entreprise['variation_abs']:+.2f}€")
                with col5:
                    st.markdown(f"<div class='price-change {change_class}'>{variation_str}</div>", 
                               unsafe_allow_html=True)
                    st.markdown(f"Vol: {entreprise['volume']:,.0f}")
                
                st.markdown("---")
        
        with tab2:
            # Analyse détaillée par secteur
            secteur_selectionne = st.selectbox("Sélectionnez un secteur:", 
                                             self.sector_data['secteur'].unique())
            
            if secteur_selectionne:
                entreprises_secteur = self.current_data[
                    self.current_data['secteur'] == secteur_selectionne
                ]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Performance des entreprises du secteur
                    fig = px.bar(entreprises_secteur, 
                                x='symbole', 
                                y='variation_pct',
                                title=f'Performance des Entreprises - {secteur_selectionne}',
                                color='variation_pct',
                                color_continuous_scale='RdYlGn')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Répartition des poids dans le secteur
                    fig = px.pie(entreprises_secteur, 
                                values='poids_indice', 
                                names='symbole',
                                title=f'Répartition des Poids - {secteur_selectionne}')
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Screener d'entreprises
            st.subheader("Screener d'Investissement")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_market_cap = st.number_input("Market Cap Min (M€)", 
                                               min_value=0, max_value=500, value=20)
                min_dividende = st.number_input("Dividende Yield Min (%)", 
                                              min_value=0.0, max_value=20.0, value=2.0)
            
            with col2:
                max_volatilite = st.number_input("Volatilité Max (%)", 
                                               min_value=0, max_value=100, value=60)
                secteur_screener = st.multiselect("Secteurs", 
                                                 self.sector_data['secteur'].unique())
            
            with col3:
                min_performance = st.number_input("Performance Min (%)", 
                                                min_value=-50.0, max_value=50.0, value=0.0)
                appliquer_filtres = st.button("Appliquer les Filtres")
            
            if appliquer_filtres:
                entreprises_filtrees = self.current_data.copy()
                entreprises_filtrees = entreprises_filtrees[
                    entreprises_filtrees['market_cap'] >= min_market_cap * 1e6
                ]
                entreprises_filtrees = entreprises_filtrees[
                    entreprises_filtrees['dividende_yield'] >= min_dividende
                ]
                entreprises_filtrees = entreprises_filtrees[
                    entreprises_filtrees['variation_pct'] >= min_performance
                ]
                
                if secteur_screener:
                    entreprises_filtrees = entreprises_filtrees[
                        entreprises_filtrees['secteur'].isin(secteur_screener)
                    ]
                
                st.write(f"**{len(entreprises_filtrees)} entreprises correspondent aux critères**")
                st.dataframe(entreprises_filtrees[['symbole', 'nom_complet', 'secteur', 'prix_actuel', 
                                                 'variation_pct', 'dividende_yield', 'market_cap']], 
                           use_container_width=True)
    
    def create_sector_analysis(self):
        """Analyse sectorielle détaillée"""
        st.markdown('<h3 class="section-header">📊 ANALYSE SECTORIELLE DÉTAILLÉE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Performance Sectorielle", "Comparaison Secteurs", "Tendances"])
        
        with tab1:
            # Performance détaillée par secteur
            sector_performance = self.current_data.groupby('secteur').agg({
                'variation_pct': 'mean',
                'volume': 'sum',
                'market_cap': 'sum',
                'symbole': 'count'
            }).reset_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(sector_performance, 
                            x='secteur', 
                            y='variation_pct',
                            title='Performance Moyenne par Secteur (%)',
                            color='variation_pct',
                            color_continuous_scale='RdYlGn')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.scatter(sector_performance, 
                               x='market_cap', 
                               y='variation_pct',
                               size='volume',
                               color='secteur',
                               title='Performance vs Capitalisation par Secteur',
                               hover_name='secteur',
                               size_max=60)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Comparaison historique des secteurs
            sector_evolution = self.historical_data.groupby([
                self.historical_data['date'].dt.to_period('M').dt.to_timestamp(),
                'secteur'
            ])['prix'].mean().reset_index()
            
            fig = px.line(sector_evolution, 
                         x='date', 
                         y='prix',
                         color='secteur',
                         title='Évolution Comparative des Secteurs (2020-2024)',
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Analyse des tendances sectorielles
            st.subheader("Tendances et Perspectives Sectorielles")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 📈 Secteurs Performants
                
                **📱 Télécommunications:**
                - Croissance de la téléphonie mobile
                - Expansion des services internet
                - Digitalisation de l'économie
                
                **🏦 Services Financiers:**
                - Inclusion financière croissante
                - Développement de la microfinance
                - Services bancaires digitaux
                
                **🏨 Tourisme & Hôtellerie:**
                - Reprise post-COVID
                - Attrait des destinations naturelles
                - Croissance du tourisme durable
                """)
            
            with col2:
                st.markdown("""
                ### 📉 Secteurs Défavorisés
                
                **✈️ Transport Aérien:**
                - Volatilité des prix du carburant
                - Coûts d'exploitation élevés
                - Dépendance au tourisme international
                
                **🏭 Industries Traditionnelles:**
                - Concurrence internationale
                - Coûts de production élevés
                - Défis logistiques
                
                **🌾 Agriculture Traditionnelle:**
                - Dépendance aux conditions climatiques
                - Accès limité aux marchés
                - Productivité variable
                """)
    
    def create_economic_analysis(self):
        """Analyse économique approfondie"""
        st.markdown('<h3 class="section-header">💰 ANALYSE ÉCONOMIQUE AVANCÉE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Indicateurs Macro", "Commerce Extérieur", "Développement"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Corrélation inflation-croissance (sans LOWESS)
                fig = px.scatter(self.economic_data, 
                               x='inflation', 
                               y='croissance_pib',
                               title='Relation Inflation vs Croissance du PIB',
                               color_discrete_sequence=['#007E3A'])
                # Ajout d'une ligne de tendance linéaire simple
                z = np.polyfit(self.economic_data['inflation'], self.economic_data['croissance_pib'], 1)
                p = np.poly1d(z)
                fig.add_traces(go.Scatter(x=self.economic_data['inflation'], 
                                        y=p(self.economic_data['inflation']),
                                        mode='lines',
                                        line=dict(color='red', dash='dash'),
                                        name='Tendance linéaire'))
                st.plotly_chart(fig, use_container_width=True)
                
                # Dette publique
                fig = px.line(self.economic_data, 
                             x='date', 
                             y='dette_publique',
                             title='Évolution de la Dette Publique (% PIB)',
                             color_discrete_sequence=['#FF6B00'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Taux d'intérêt réels
                economic_data_copy = self.economic_data.copy()
                economic_data_copy['taux_reel'] = economic_data_copy['taux_directeur'] - economic_data_copy['inflation']
                
                fig = px.line(economic_data_copy, 
                             x='date', 
                             y='taux_reel',
                             title='Taux d\'Intérêt Réel (%)',
                             color_discrete_sequence=['#660099'])
                st.plotly_chart(fig, use_container_width=True)
                
                # Réserves de devises
                fig = px.line(self.economic_data, 
                             x='date', 
                             y='reserves_devises',
                             title='Réserves de Devises (Millions USD)',
                             color_discrete_sequence=['#004B87'])
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Commerce Extérieur et Balance Commerciale")
            
            # Données simulées du commerce extérieur
            dates_commerce = pd.date_range('2020-01-01', datetime.now(), freq='Q')
            commerce_data = []
            
            for date in dates_commerce:
                commerce_data.append({
                    'date': date,
                    'exportations': random.uniform(200, 400),
                    'importations': random.uniform(500, 700),
                    'balance_commerciale': random.uniform(-300, -100),
                    'export_vanille': random.uniform(50, 100),
                    'export_cafe': random.uniform(20, 50),
                    'export_crevettes': random.uniform(60, 120)
                })
            
            commerce_df = pd.DataFrame(commerce_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.line(commerce_df, 
                             x='date', 
                             y=['exportations', 'importations'],
                             title='Exportations vs Importations (Millions USD)',
                             color_discrete_sequence=['#007E3A', '#FC3D32'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.line(commerce_df, 
                             x='date', 
                             y='balance_commerciale',
                             title='Balance Commerciale (Millions USD)',
                             color_discrete_sequence=['#FF6B00'])
                st.plotly_chart(fig, use_container_width=True)
            
            # Composition des exportations
            st.subheader("Composition des Exportations")
            dernier_trimestre = commerce_df.iloc[-1]
            produits_export = {
                'Vanille': dernier_trimestre['export_vanille'],
                'Café': dernier_trimestre['export_cafe'],
                'Crevettes': dernier_trimestre['export_crevettes'],
                'Autres': dernier_trimestre['exportations'] - (dernier_trimestre['export_vanille'] + 
                                                              dernier_trimestre['export_cafe'] + 
                                                              dernier_trimestre['export_crevettes'])
            }
            
            fig = px.pie(values=list(produits_export.values()), 
                        names=list(produits_export.keys()),
                        title='Répartition des Produits d\'Exportation')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Indicateurs de Développement")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 📈 Indicateurs Socio-économiques
                
                **Démographie:**
                - Population: 28 millions (2023)
                - Taux de croissance: 2.7% annuel
                - Population urbaine: 38%
                
                **Éducation:**
                - Taux d'alphabétisation: 76%
                - Scolarisation primaire: 92%
                - Accès à l'éducation secondaire: 35%
                
                **Santé:**
                - Espérance de vie: 67 ans
                - Accès aux soins: 45%
                - Mortalité infantile: 39‰
                """)
            
            with col2:
                st.markdown("""
                ### 🏗️ Infrastructures
                
                **Énergie:**
                - Taux d'électrification: 33%
                - Capacité installée: 670 MW
                - Énergies renouvelables: 75%
                
                **Transports:**
                - Routes goudronnées: 12%
                - Aéroports internationaux: 2
                - Ports majeurs: 4
                
                **Télécommunications:**
                - Taux de pénétration mobile: 45%
                - Accès internet: 15%
                - Couverture 4G: 40%
                """)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Filtres temporels
        st.sidebar.markdown("### 📅 Période d'analyse")
        date_debut = st.sidebar.date_input("Date de début", 
                                         value=datetime.now() - timedelta(days=365))
        date_fin = st.sidebar.date_input("Date de fin", 
                                       value=datetime.now())
        
        # Filtres secteurs
        st.sidebar.markdown("### 🏢 Sélection des secteurs")
        secteurs_selectionnes = st.sidebar.multiselect(
            "Secteurs à afficher:",
            list(self.sector_data['secteur'].unique()),
            default=list(self.sector_data['secteur'].unique())[:3]
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=True)
        show_economic = st.sidebar.checkbox("Afficher indicateurs économiques", value=True)
        
        # Bouton de rafraîchissement manuel
        if st.sidebar.button("🔄 Rafraîchir les données"):
            self.update_live_data()
            st.rerun()
        
        # Informations économiques
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 💹 INDICATEURS CLÉS")
        
        # Indicateurs économiques simulés
        indicateurs = {
            'Déficit Budgétaire': {'valeur': -4.2, 'variation': random.uniform(-0.5, 0.5)},
            'Chômage': {'valeur': 2.1, 'variation': random.uniform(-0.2, 0.2)},
            'Investissement Direct': {'valeur': 350, 'variation': random.uniform(-50, 50)},
            'Touristes Annuels': {'valeur': 215, 'variation': random.uniform(-30, 30)}
        }
        
        for indicateur, data in indicateurs.items():
            if indicateur in ['Investissement Direct', 'Touristes Annuels']:
                st.sidebar.metric(
                    indicateur,
                    f"{data['valeur']:,.0f}",
                    f"{data['variation']:+.0f}"
                )
            else:
                st.sidebar.metric(
                    indicateur,
                    f"{data['valeur']:.1f}%",
                    f"{data['variation']:+.1f}%"
                )
        
        return {
            'date_debut': date_debut,
            'date_fin': date_fin,
            'secteurs_selectionnes': secteurs_selectionnes,
            'auto_refresh': auto_refresh,
            'show_economic': show_economic
        }

    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Mise à jour des données live
        self.update_live_data()
        
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Marché", 
            "🏢 Entreprises", 
            "📊 Secteurs", 
            "💰 Économie", 
            "💡 Perspectives",
            "ℹ️ À Propos"
        ])
        
        with tab1:
            self.create_market_overview()
        
        with tab2:
            self.create_entreprises_live()
        
        with tab3:
            self.create_sector_analysis()
        
        with tab4:
            self.create_economic_analysis()
        
        with tab5:
            st.markdown("## 💡 PERSPECTIVES ÉCONOMIQUES")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🎯 OPPORTUNITÉS DE DÉVELOPPEMENT
                
                **🌱 Agriculture & Agro-industrie:**
                - Vanille: 80% de la production mondiale
                - Cacao et café de spécialité
                - Fruits tropicaux biologiques
                
                **💎 Mines & Ressources:**
                - Graphite et nickel stratégiques
                - Pierres précieuses (saphirs)
                - Terres rares
                
                **🌊 Tourisme & Écotourisme:**
                - Biodiversité unique au monde
                - Écotourisme en croissance
                - Tourisme culturel authentique
                """)
            
            with col2:
                st.markdown("""
                ### 🚨 DÉFIS ÉCONOMIQUES
                
                **⚡ Infrastructures:**
                - Déficit énergétique important
                - Routes et transports limités
                - Accès internet à développer
                
                **💼 Environnement des Affaires:**
                - Réforme administrative en cours
                - Lutte contre la corruption
                - Amélioration de la gouvernance
                
                **🌍 Vulnérabilités:**
                - Exposition aux catastrophes naturelles
                - Dépendance aux matières premières
                - Instabilité politique historique
                """)
            
            st.markdown("""
            ### 📋 STRATÉGIES DE DÉVELOPPEMENT
            
            1. **Diversification Économique:** Réduction de la dépendance aux matières premières
            2. **Investissement Infrastructures:** Énergie, transports et digital
            3. **Développement du Capital Humain:** Éducation et formation professionnelle
            4. **Promotion du Secteur Privé:** Amélioration du climat des affaires
            5. **Intégration Régionale:** Renforcement des échanges dans l'océan Indien
            """)
        
        with tab6:
            st.markdown("## 📋 À propos de ce dashboard")
            st.markdown("""
            Ce dashboard présente une analyse en temps réel des performances économiques 
            et boursières de Madagascar.
            
            **Couverture:**
            - Principales entreprises malgaches cotées
            - Indicateurs économiques macro
            - Analyse sectorielle détaillée
            - Données historiques depuis 2020
            
            **Sources des données:**
            - Bourse des Valeurs Mobilières de Madagascar (BVMC)
            - Institut National de la Statistique (INSTAT)
            - Banque Centrale de Madagascar
            - Ministère de l'Économie et des Finances
            
            **⚠️ Avertissement:** 
            Les données présentées sont simulées pour la démonstration.
            Ce dashboard n'est pas un conseil en investissement.
            Les performances passées ne préjugent pas des performances futures.
            
            **🔒 Confidentialité:** 
            Toutes les données sont agrégées et anonymisées.
            """)
            
            st.markdown("---")
            st.markdown("""
            **📞 Contact:**
            - Site web: www.economie.gov.mg
            - Email: info@economie.gov.mg
            - Adresse: Antananarivo, Madagascar
            """)
        
        # Rafraîchissement automatique
        if controls['auto_refresh']:
            time.sleep(30)  # Rafraîchissement toutes les 30 secondes
            st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = MadagascarDashboard()
    dashboard.run_dashboard()