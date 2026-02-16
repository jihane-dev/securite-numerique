import streamlit as st
import re
import json
from PIL import Image
from streamlit_lottie import st_lottie
from streamlit_extras.let_it_rain import rain

# === PAGE CONFIG ===
st.set_page_config(page_title="Sécurité numérique", page_icon="🪪", layout="wide")

# === LOAD LOGO ===
logo = Image.open("assets/hack.JPG")

# === LOAD CSS ===
st.markdown("""
<style>
/* Titre principal */
h2.title {
    font-size: 32px;
    margin-top: 0px;  /* plus d'espace inutile en haut */
    text-align: center;
    color: white;
}

/* Card standard */
.card {
    background: #fff;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-top: 15px;
    transition: all 0.3s ease;
}

/* Card active avec halo vert/animé */
.card.active {
    border: 2px solid #2e0333;
    animation: glow 1.5s infinite alternate;
}

/* Animation glow */
@keyframes glow {
    0% { box-shadow: 0 0 10px 2px rgba(21, 92, 184, 0.5); }
    100% { box-shadow: 0 0 25px 8px rgba(150, 14, 192, 0.8); }
}

/* Logo fixe en haut à gauche */
.logo-fixed {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 100;
}

/* Container padding */
.block-container {
    padding-top: 0rem !important;
}
</style>
""", unsafe_allow_html=True)

# === LOGO FIXE ===
st.markdown('<div class="logo-fixed">', unsafe_allow_html=True)
st.image(logo, width=60)
st.markdown('</div>', unsafe_allow_html=True)

# === LOAD LOTTIE ===
def load_lottie(filepath):
    """Charge un fichier Lottie JSON"""
    with open(filepath, "r") as f:
        return json.load(f)

lottie_security = load_lottie("assets/Cybersecurity.json")

# === SESSION STATE ===
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# === FUNCTIONS ===
def verifier_password(pw: str) -> list:
    """Retourne les erreurs de sécurité du mot de passe"""
    erreurs = []
    if len(pw) < 8: erreurs.append("❌ Minimum 8 caractères")
    if not re.search(r"[A-Z]", pw): erreurs.append("❌ Une majuscule nécessaire")
    if not re.search(r"[a-z]", pw): erreurs.append("❌ Une minuscule nécessaire")
    if not re.search(r"[0-9]", pw): erreurs.append("❌ Un chiffre nécessaire")
    if not re.search(r"[@#$%^&*!]", pw): erreurs.append("❌ Caractère spécial nécessaire")
    return erreurs

def score_password(pw: str) -> int:
    """Calcule un score de sécurité sur 5"""
    score = 0
    checks = [r".{8,}", r"[A-Z]", r"[a-z]", r"[0-9]", r"[@#$%^&*!]"]
    for check in checks:
        if re.search(check, pw):
            score += 1
    return score

def temps_piratage(score: int) -> str:
    """Retourne un temps estimé de piratage"""
    return {
        0: "⏱️ Quelques secondes 🔓",
        1: "⏱️ Quelques secondes 🔓",
        2: "⏱️ Quelques minutes",
        3: "⏱️ Quelques heures",
        4: "⏱️ Plusieurs jours",
        5: "⏱️ Plusieurs années 🔐"
    }[score]

def run_key_animation():
    """Animation de pluie de clés"""
    rain(emoji="🗝️", font_size=20, falling_speed=5, animation_length="infinite")

# === LOGIN SCREEN ===
if not st.session_state.access_granted:
    run_key_animation()
    
    st.markdown("<h2 class='title'>🔐 Comment créer mon Password ?</h2>", unsafe_allow_html=True)
    st_lottie(lottie_security, height=250)

    if st.button("Entrer"):
        st.session_state.show_login = True

    if st.session_state.show_login:
        card_class = "card active"
        with st.container():
            st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
            st.markdown("### 🔑 Identifiants requis")
            id_input = st.text_input("ID", key="login_id")
            pw_input = st.text_input("Mot de passe", type="password", key="login_pw")
            if st.button("Valider les identifiants"):
                if id_input == "admin" and pw_input == "8520jiJi@":
                    st.success("✅ Accès accordé !")
                    st.session_state.access_granted = True
                    st.rerun()
                else:
                    st.error("❌ Identifiant ou mot de passe incorrect !")
            st.markdown("</div>", unsafe_allow_html=True)

# === MAIN APP ===
else:
    col1, col2 = st.columns([4,1])
    with col1:
        st.markdown("<h2 class='title'>🔐 Sécurité Numérique</h2>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("Essayez de créer un mot de passe solide 👇")
        password = st.text_input("Entrez votre mot de passe :", type="password")
        if password:
            erreurs = verifier_password(password)
            score = score_password(password)
            st.subheader("Force du mot de passe :")
            st.progress(score / 5)

            # Feedback visuel amélioré
            if score <= 2:
                st.error("🔴 Mot de passe FAIBLE")
            elif score <= 4:
                st.warning("🟠 Mot de passe MOYEN")
            else:
                st.success("🟢 Mot de passe SOLIDE !")

            st.info(f"Temps estimé pour pirater : {temps_piratage(score)}")

            if erreurs:
                st.markdown("### Améliorations nécessaires :")
                for e in erreurs:
                    st.write(f"- {e}")
        st.markdown("</div>", unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
<hr>
**Partagé par [Professeure de SVT : J.Jait 🧠]**

© all rights reserved - 2026
""", unsafe_allow_html=True)
