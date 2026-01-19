import streamlit as st
import requests
from utils.prompts import BRAND_IDENTITY, PROMPTS, PLATFORM_GUIDELINES


def generate_post(post_type, platform, **kwargs):
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except KeyError:
        return "Cle API non trouvee"
    
    if post_type not in PROMPTS:
        return "Type de post non reconnu"
    
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
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["content"][0]["text"]
        else:
            return "Erreur API " + str(response.status_code)
            
    except Exception as e:
        return "Erreur " + str(e)


def generate_launch_post(platform, product_name, product_type, scent, ingredients, benefits):
    return generate_post(
        post_type="lancement",
        platform=platform,
        product_name=product_name,
        product_type=product_type,
        scent=scent,
        ingredients=ingredients,
        benefits=benefits
    )


def generate_citation_post(platform, theme):
    return generate_post(
        post_type="citation",
        platform=platform,
        theme=theme
    )


def generate_educational_post(platform, topic):
    return generate_post(
        post_type="educatif",
        platform=platform,
        topic=topic
    )


def generate_video_script(platform, video_type, subject):
    return generate_post(
        post_type="script_video",
        platform=platform,
        video_type=video_type,
        subject=subject
    )
