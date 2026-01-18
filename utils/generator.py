"""
Baddie's Bakery - Générateur de Contenu
"""

import anthropic
import streamlit as st
from utils.prompts import BRAND_IDENTITY, PROMPTS, PLATFORM_GUIDELINES


def get_client():
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        return anthropic.Anthropic(api_key=api_key)
    except KeyError:
        st.error("❌ Clé API non trouvée ! Configure ton fichier secrets.")
        return None


def generate_post(post_type: str, platform: str, **kwargs) -> str:
    client = get_client()
    if client is None:
        return "Erreur : Impossible de se connecter à l'API"
    
    if post_type not in PROMPTS:
        return f"Erreur : Type de post '{post_type}' non reconnu"
    
    prompt_template = PROMPTS[post_type]
    platform_guidelines = PLATFORM_GUIDELINES.get(platform, "")
    
    prompt = prompt_template.format(
        brand_identity=BRAND_IDENTITY,
        platform=platform,
        platform_guidelines=platform_guidelines,
        **kwargs
    )
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except anthropic.APIConnectionError:
        return "❌ Erreur de connexion. Vérifie ta connexion internet."
    except anthropic.RateLimitError:
        return "❌ Limite d'appels API atteinte. Réessaie dans quelques minutes."
    except anthropic.APIStatusError as e:
        return f"❌ Erreur API : {e.message}"
    except Exception as e:
        return f"❌ Erreur inattendue : {str(e)}"


def generate_launch_post(platform: str, product_name: str, product_type: str, 
                         scent: str, ingredients: str, benefits: str) -> str:
    return generate_post(
        post_type="lancement",
        platform=platform,
        product_name=product_name,
        product_type=product_type,
        scent=scent,
        ingredients=ingredients,
        benefits=benefits
    )


def generate_citation_post(platform: str, theme: str) -> str:
    return generate_post(
        post_type="citation",
        platform=platform,
        theme=theme
    )


def generate_educational_post(platform: str, topic: str) -> str:
    return generate_post(
        post_type="educatif",
        platform=platform,
        topic=topic
    )
