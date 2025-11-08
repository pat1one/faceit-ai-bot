# Color scheme based on Faceit's branding
colors = {
    'primary': {
        'main': '#FF5500',  # Faceit Orange
        'light': '#FF7733',
        'dark': '#CC4400',
    },
    'secondary': {
        'main': '#1F1F1F',  # Dark Gray
        'light': '#2D2D2D',
        'dark': '#171717',
    },
    'background': {
        'default': '#121212',  # Dark theme background
        'paper': '#1E1E1E',
    },
    'text': {
        'primary': '#FFFFFF',
        'secondary': '#B3B3B3',
    },
    'success': {
        'main': '#4CAF50',
        'light': '#81C784',
        'dark': '#388E3C',
    },
    'error': {
        'main': '#F44336',
        'light': '#E57373',
        'dark': '#D32F2F',
    },
}

# Typography
typography = {
    'fontFamily': '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    'h1': {
        'fontSize': '2.5rem',
        'fontWeight': 600,
        'lineHeight': 1.2,
    },
    'h2': {
        'fontSize': '2rem',
        'fontWeight': 600,
        'lineHeight': 1.3,
    },
    'h3': {
        'fontSize': '1.75rem',
        'fontWeight': 600,
        'lineHeight': 1.4,
    },
    'body1': {
        'fontSize': '1rem',
        'fontWeight': 400,
        'lineHeight': 1.5,
    },
    'body2': {
        'fontSize': '0.875rem',
        'fontWeight': 400,
        'lineHeight': 1.43,
    },
    'button': {
        'fontSize': '0.875rem',
        'fontWeight': 500,
        'lineHeight': 1.75,
        'textTransform': 'uppercase',
    },
}

# Borders and shadows
shape = {
    'borderRadius': '4px',
    'boxShadow': '0px 2px 4px rgba(0, 0, 0, 0.25)',
}

# Custom styles for components
components = {
    'button': {
        'borderRadius': '4px',
        'padding': '8px 16px',
        'transition': 'all 0.2s ease-in-out',
        'textTransform': 'uppercase',
        'fontWeight': 500,
    },
    'card': {
        'borderRadius': '8px',
        'backgroundColor': '#1E1E1E',
        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.15)',
    },
    'input': {
        'backgroundColor': '#2D2D2D',
        'borderRadius': '4px',
        'border': 'none',
        'color': '#FFFFFF',
    },
}

# Export theme configuration
theme = {
    'colors': colors,
    'typography': typography,
    'shape': shape,
    'components': components,
}