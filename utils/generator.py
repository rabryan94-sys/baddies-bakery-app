"""
Baddie's Bakery - Générateur de Contenu
"""

import streamlit as st
import requests
from utils.prompts import BRAND_IDENTITY, PROMPTS, PLATFORM_GUIDELINES


def generate_post(post_type: str, platform: str, **kwargs) -> str:
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except KeyError:
        return "❌ Clé API non trouvée ! Configure tes secrets."
    
    if post_type not in PROMPTS:
        return f"❌ Type de post '{post_type}' non reconnu"
    
    prompt_template = PROMPTS[post_type]
    platform_guidelines = PLATFORM_GUIDELINES.get(platform, "")
    
    prompt = prompt_template.format(
        brand_identity=BRAND_IDENTITY,
        platform=platform,
        platform_guidelines=platform_guidelines,
        **kwargs
    )
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-instant-1.2",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["content"][0]["text"]
        else:
            error_detail = response.text
            return f"❌ Erreur API {response.status_code}: {error_detail}"
            
    except Exception as e:
        return f"❌ Erreur : {str(e)}"


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
