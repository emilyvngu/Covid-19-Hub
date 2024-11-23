"""
def get_theme():

    #Determines the current theme of the application (light or dark).
    #Returns:
    #    str: 'dark' if dark mode is active, otherwise 'default'.

    args = pn.state.session_args
    if "theme" in args and args["theme"][0] == b"dark":
        return "dark"
    return "default"

current_theme = get_theme()

background_color='#ffffff' if get_theme() == 'default' else '#181818'

theme=current_theme,  # Dynamically set the theme
    theme_toggle=True,  # Enable toggle for switching themes
"""