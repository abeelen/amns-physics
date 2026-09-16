import streamlit as st

st.write("# Bienvenue sur cette application interactive dédiée à l'AMNS Physique 👋")
st.markdown(
    """
 Elle a été conçue comme un support pour explorer et comprendre les concepts vu en cours d'Ondes et d'Optique Géométrique !
 
## 🎯 Objectifs 

- Comprendre le concept d'once progressive
- Les concept 
- Revoir les notions de base en optique géométrique.
- Visualiser le comportement des rayons lumineux dans différents dispositifs.
- Expérimenter de manière interactive pour mieux saisir les lois de formation des images.

## 📑 Contenu disponible 

1. 🪞 **Miroir sphérique** : Découvre la réflexion des rayons lumineux sur une surface courbe et l’effet de la concavité/convexité.
2. 📐 **Dioptre plan** : Étudie la réfraction à la traversée d’une surface plane séparant deux milieux transparents.
3. 🔎 **Lentille mince** : Explore la convergence et la divergence des rayons à travers une lentille, et comprends la formation des images réelles ou virtuelles.

## Comment utiliser l’application ? 🚀

👉 Utilise le menu latéral pour naviguer entre les différentes sections.

👉 Interagis avec les paramètres proposés (distance focale, position de l’objet, indices de réfraction, etc.) afin d’observer en direct l’évolution des tracés de rayons.

"""
)

st.sidebar.success("Selectionnez une page.")
