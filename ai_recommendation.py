# Placeholder for AI song recommendation

import yaml
import openai
import os

def get_openai_api_key():
    with open('configs/key.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data.get('openai_api_key')

def suggest_songs(theme, rules, num_songs=5):
    api_key = get_openai_api_key()
    openai.api_key = api_key
    prompt = f"""
You are a music expert AI. Suggest {num_songs} songs for a party playlist with the following theme and rules.
Theme: {theme}
Rules: {rules}
For each song, provide:
- Title and artist
- A short rationale (1-2 sentences) for why it fits
Format:
1. Song Title - Artist: Rationale
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.8
        )
        text = response['choices'][0]['message']['content']
        suggestions = []
        for line in text.strip().split('\n'):
            if line.strip() and any(c.isdigit() for c in line[:3]):
                suggestions.append(line.strip())
        return suggestions
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return [] 