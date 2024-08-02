# context_processors.py
def common_data(request):
    navigation = [
        {'label': 'Home', 'href': '/'},
        {'label': 'About', 'href': '/about'},
        {'label': 'Register', 'href': '/register'},
        
    ]

    socials = [
        {'label': 'Facebook', 'href': 'https://facebook.com', 'icon': 'fab fa-facebook-f'},
        {'label': 'Twitter', 'href': 'https://twitter.com', 'icon': 'fab fa-twitter'},
        {'label': 'Instagram', 'href': 'https://instagram.com', 'icon': 'fab fa-instagram'},
    ]

    return {
        'navigation': navigation,
        'socials': socials,
    }
