import re
import json

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    else:
        return False

def validate_password(password):
    pattern = r'^(?=.*[a-zA-Z0-9])(?=.*[!@#$%^&*()-_=+])[a-zA-Z0-9!@#$%^&*()-_=+]{8,}$'
    
    if re.match(pattern, password):
        return True
    else:
        return False

def activity_data(data):
    filtered_data = []
    for feature in data['features']:
        properties = feature['properties']
        filtered_feature = {
            'name': properties.get('name', ''),
            'district': properties.get('district', ''),
            'street': properties.get('street', ''),
            'Address': properties.get('formatted', ''),
            'phone': properties.get('contact', {}).get('phone', ''),
            'opening_hours': properties.get('opening_hours', '')
        }
        filtered_data.append(filtered_feature)

    return filtered_data

def recommend_activity(weather_condition):
    if weather_condition.lower() in ['sunny', 'clear']:
        return "Outdoor activities like visiting parks or outdoor cafes are recommended."
    elif weather_condition.lower() in ['rain', 'drizzle']:
        return "Indoor activities such as visiting museums, galleries, or indoor arenas are recommended."
    elif weather_condition.lower() in ['snow']:
        return "Enjoy activities like skiing or building a snowman outdoors."
    elif weather_condition.lower() in ['mist', 'smoke', 'haze', 'fog']:
        return "Take precautions and consider indoor activities due to poor visibility."
    elif weather_condition.lower() in ['dust', 'sand']:
        return "Stay indoors and avoid outdoor activities due to dusty conditions."
    elif weather_condition.lower() in ['ash']:
        return "Remain indoors and protect yourself from ashfall."
    elif weather_condition.lower() in ['squall', 'tornado']:
        return "Seek shelter immediately and stay indoors until the weather improves."
    elif weather_condition.lower() in ['thunderstorm']:
        return "Stay indoors and avoid outdoor activities until the thunderstorm passes."
    else:
        return "No specific recommendation for this weather condition."