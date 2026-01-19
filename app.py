"""
🧁 Baddie's Bakery - Générateur de Posts
Application principale Streamlit
"""

import streamlit as st
from utils.generator import (
    generate_launch_post, 
    generate_citation_post, 
    generate_educational_post,
    generate_video_script
)
from utils.prompts import CITATION_THEMES, EDUCATIONAL_TOPICS, VIDEO_TYPES
from utils.database import save_post

st.set_page_config(
    page_title="Baddie's Bakery - Générateur de Posts",
    page_icon="🧁",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #FFE4EC 0%, #FFF5F8 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: #E91E8C;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: #666;
        font-size: 1.1rem;
    }
    .result-card {
        background: white;
        border: 2px solid #FFE4EC;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(233, 30, 140, 0.1);
    }
    .stButton > button {
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    .platform-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: #E91E8C;
        color: white;
        border-radius: 15px;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🧁 Baddie's Bakery</h1>
    <p>Génère des posts irrésistibles pour tes réseaux sociaux</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎯 Type de contenu")
    post_type = st.radio(
        "Que veux-tu créer ?",
        options=["🚀 Lancement produit", "💖 Citation inspirante", "📚 Post éducatif", "🎬 Script vidéo"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### 📱 Plateforme")
    platform = st.selectbox(
        "Pour quelle plateforme ?",
        options=["Instagram", "TikTok", "Facebook", "Twitter"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### 📊 Statistiques")
    from utils.database import get_stats
    stats = get_stats()
    st.metric("Posts générés", stats["total"])

st.markdown(f"### {post_type}")

if "generated_content" not in st.session_state:
    st.session_state.generated_content = None

# LANCEMENT PRODUIT
if "Lancement" in post_type:
    with st.form("launch_form"):
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("Nom du produit", placeholder="Ex: Strawberry Dream")
            product_type = st.selectbox("Type de produit", ["Crème corporelle", "Baume à lèvres", "Huile corporelle", "Gommage", "Beurre corporel", "Brume parfumée"])
            scent = st.text_input("Senteur principale", placeholder="Ex: Fraise, vanille, chantilly")
        with col2:
            ingredients = st.text_area("Ingrédients clés", placeholder="Ex: Beurre de karité, huile de coco", height=100)
            benefits = st.text_area("Bénéfices", placeholder="Ex: Hydratation intense, peau douce", height=100)
        submitted = st.form_submit_button("✨ Générer le post", use_container_width=True)
        if submitted:
            if not product_name or not scent:
                st.error("Remplis au moins le nom du produit et la senteur !")
            else:
                with st.spinner("Création de ton post magique... 🧁"):
                    content = generate_launch_post(platform=platform, product_name=product_name, product_type=product_type, scent=scent, ingredients=ingredients or "Ingrédients naturels", benefits=benefits or "Peau douce et parfumée")
                    st.session_state.generated_content = content
                    st.session_state.post_type_key = "lancement"
                    st.session_state.post_metadata = {"product_name": product_name, "product_type": product_type, "scent": scent}

# CITATION INSPIRANTE
elif "Citation" in post_type:
    with st.form("citation_form"):
        theme = st.selectbox("Thème de la citation", options=CITATION_THEMES)
        custom_theme = st.text_input("Ou écris ton propre thème", placeholder="Ex: Se sentir belle même les mauvais jours")
        submitted = st.form_submit_button("✨ Générer la citation", use_container_width=True)
        if submitted:
            final_theme = custom_theme if custom_theme else theme
            with st.spinner("Création de ton post inspirant... 💖"):
                content = generate_citation_post(platform=platform, theme=final_theme)
                st.session_state.generated_content = content
                st.session_state.post_type_key = "citation"
                st.session_state.post_metadata = {"theme": final_theme}

# POST ÉDUCATIF
elif "éducatif" in post_type:
    with st.form("educational_form"):
        topic = st.selectbox("Sujet à expliquer", options=EDUCATIONAL_TOPICS)
        custom_topic = st.text_input("Ou écris ton propre sujet", placeholder="Ex: Les bienfaits de l'aloe vera")
        submitted = st.form_submit_button("✨ Générer le post éducatif", use_container_width=True)
        if submitted:
            final_topic = custom_topic if custom_topic else topic
            with st.spinner("Création de ton post éducatif... 📚"):
                content = generate_educational_post(platform=platform, topic=final_topic)
                st.session_state.generated_content = content
                st.session_state.post_type_key = "educatif"
                st.session_state.post_metadata = {"topic": final_topic}

# SCRIPT VIDÉO
elif "Script" in post_type:
    with st.form("video_form"):
        video_type = st.selectbox("Type de vidéo", options=VIDEO_TYPES)
        subject = st.text_area("Sujet de la vidéo", placeholder="Ex: Présentation de notre nouvelle crème Girl Boss à la cerise", height=100)
        submitted = st.form_submit_button("🎬 Générer le script", use_container_width=True)
        if submitted:
            if not subject:
                st.error("Décris le sujet de ta vidéo !")
            else:
                with st.spinner("Création de ton script vidéo... 🎬"):
                    content = generate_video_script(platform=platform, video_type=video_type, subject=subject)
                    st.session_state.generated_content = content
                    st.session_state.post_type_key = "script_video"
                    st.session_state.post_metadata = {"video_type": video_type, "subject": subject}

# AFFICHAGE DU RÉSULTAT
if st.session_state.generated_content:
    st.markdown("---")
    st.markdown("### 📝 Ton contenu est prêt !")
    st.markdown(f'<span class="platform-badge">{platform}</span>', unsafe_allow_html=True)
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.generated_content)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Copier", use_container_width=True):
            st.code(st.session_state.generated_content, language=None)
            st.success("Copie le texte ci-dessus !")
    with col2:
        if st.button("🔄 Régénérer", use_container_width=True):
            st.session_state.generated_content = None
            st.rerun()
    with col3:
        if st.button("💾 Sauvegarder", use_container_width=True):
            post_id = save_post(
                content=st.session_state.generated_content, 
                post_type=st.session_state.get("post_type_key", "post"), 
                platform=platform, 
                metadata=st.session_state.get("post_metadata", {})
            )
            st.success(f"✅ Sauvegardé ! (ID: {post_id})")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #999;'>Made with 💖 for Baddie's Bakery</p>", unsafe_allow_html=True)
