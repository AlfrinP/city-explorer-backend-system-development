

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
    categories = {
        'sunny': ("Bask in the sunshine and have a picnic at the park!", 'leisure.park'),
        'clear': ("Sip a refreshing drink at an outdoor cafe and enjoy the clear skies.", {'leisure.picnic','leisure.picnic.picnic_site','leisure.picnic.picnic_table','leisure.picnic.bbq'}),
        'rain': ("Dive into adventure at a museum or aquarium - rain can't stop the fun!", 'entertainment.museum'),
        'drizzle': ("Embark on a cultural journey at an art gallery or catch a live performance at a theater!", 'entertainment.culture.gallery'),
        'snow': ("Hit the slopes and carve your way through fresh powder at a ski resort!", 'commercial.outdoor_and_sport.ski'),
        'mist': ("Melt away stress with a relaxing spa day - let the misty ambiance whisk you to tranquility.", 'service.beauty.spa'),
        'smoke': ("Unwind and detoxify in a sauna - let the steamy atmosphere rejuvenate your body and mind.", 'service.beauty.spa'),
        'haze': ("Immerse yourself in cinematic magic at a movie theater or rack up points at an arcade - haze won't dull the excitement!", 'entertainment.cinema'),
        'fog': ("Embrace retail therapy and explore the latest trends at a bustling shopping mall - foggy weather won't dampen your shopping spirit!", 'commercial.shopping_mall'),
        'dust': ("Embark on a culinary adventure and shop for essentials at a supermarket - even dusty days call for delicious meals!", 'commercial.supermarket'),
        'sand': ("Bowl a strike or challenge your friends to arcade games at an indoor amusement park - sandstorm? More like funstorm!", 'entertainment.bowling_alley'),
        'ash': ("Retreat to the comfort of a cozy hotel or guesthouse - let the ash outside add a touch of adventure to your indoor retreat!", 'accommodation.hotel'),
        'squall': ("Cozy up in a snug hostel or bed-and-breakfast and ride out the storm in style!", 'accommodation.hostel'),
        'tornado': ("Take shelter and relax in the welcoming ambiance of a motel or inn - let the storm rage while you stay safe and sound!", 'accommodation.motel'),
        'thunderstorm': ("Snuggle up in a rustic cabin or chalet and let the thunderstorm provide the soundtrack to your cozy retreat!", 'accommodation.chalet')
    }

    weather_condition = weather_condition.lower()
    if weather_condition in categories:
        description, category = categories[weather_condition]
        return description, category
    else:
        return ("No specific recommendation for this weather condition.", None)

