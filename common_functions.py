import config

def determine_user_language(user_id):
    return config.user_sessions.get(user_id, {'language': 'fr'}).get('language', 'fr')

def get_user_package_info(user_id):
    return