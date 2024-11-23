import panel as pn

pn.extension()

# Function to get the current theme from session arguments
def get_theme():
    """
    Determines the current theme of the application (light or dark).
    Returns:
        str: 'dark' if dark mode is active, otherwise 'default'.
    """
    args = pn.state.session_args
    if "theme" in args and args["theme"][0] == b"dark":
        return "dark"
    return "default"

# Set the initial theme based on session arguments
current_theme = get_theme()

# Callback to toggle the theme
def toggle_theme(event):
    global current_theme
    current_theme = "dark" if current_theme == "default" else "default"
    print(f"Theme toggled to: {current_theme}")
    # You may also persist this state in session_args or a database if needed

# Add a manual toggle button
theme_toggle_button = pn.widgets.Button(name="Toggle Theme", button_type="primary")
theme_toggle_button.on_click(toggle_theme)

# Example content
example_content = pn.pane.Markdown("### Theme Toggle Example")

# Layout with dynamic theme
layout = pn.template.FastListTemplate(
    title="Theme Toggle Example",
    theme=current_theme,  # Set the initial theme
    main=[
        pn.Row(theme_toggle_button),
        example_content
    ],
    header_background="#343a40"
)

layout.servable()
