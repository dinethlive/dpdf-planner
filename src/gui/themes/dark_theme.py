"""
Dark Theme - Modern dark theme styling for the application

Provides a cohesive color palette and styling utilities for Tkinter widgets.
"""


class DarkTheme:
    """
    Modern dark theme with vibrant accents.
    """
    
    # Color Palette
    COLORS = {
        # Backgrounds
        'bg_primary': '#1a1a2e',       # Deep navy - main background
        'bg_secondary': '#16213e',     # Slightly lighter - panels
        'bg_tertiary': '#0f3460',      # Card backgrounds
        'bg_input': '#1f2940',         # Input field background
        'bg_hover': '#2a3f5f',         # Hover state
        
        # Accent colors
        'accent': '#e94560',           # Vibrant coral - primary action
        'accent_hover': '#ff6b6b',     # Lighter coral - hover
        'accent_light': '#ff8585',     # Even lighter - active
        
        # Text colors
        'text_primary': '#ffffff',     # White - main text
        'text_secondary': '#a0aec0',   # Gray - secondary text
        'text_muted': '#718096',       # Muted gray - hints
        'text_disabled': '#4a5568',    # Disabled text
        
        # Status colors
        'success': '#48bb78',          # Green
        'success_bg': '#1a3a2a',       # Green background
        'warning': '#ed8936',          # Orange
        'warning_bg': '#3a2a1a',       # Orange background
        'error': '#fc8181',            # Red
        'error_bg': '#3a1a1a',         # Red background
        'info': '#63b3ed',             # Blue
        'info_bg': '#1a2a3a',          # Blue background
        
        # Border colors
        'border': '#2d3748',           # Default border
        'border_focus': '#e94560',     # Focused border
        'border_hover': '#4a5568',     # Hover border
        
        # Scrollbar colors
        'scrollbar_bg': '#1a1a2e',
        'scrollbar_thumb': '#4a5568',
        'scrollbar_thumb_hover': '#718096',
    }
    
    # Font settings
    FONTS = {
        'family': 'Segoe UI',
        'size_small': 9,
        'size_normal': 10,
        'size_large': 12,
        'size_title': 14,
        'size_header': 18,
    }
    
    # Spacing
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 12,
        'lg': 16,
        'xl': 24,
        'xxl': 32,
    }
    
    # Border radius (for ttk, we simulate with padding and colors)
    RADIUS = {
        'sm': 4,
        'md': 8,
        'lg': 12,
    }
    
    @classmethod
    def configure_root(cls, root):
        """
        Configure the root window with dark theme colors.
        
        Args:
            root: The Tkinter root window
        """
        root.configure(bg=cls.COLORS['bg_primary'])
    
    @classmethod
    def configure_ttk_style(cls, style):
        """
        Configure ttk styles for the dark theme.
        
        Args:
            style: ttk.Style instance
        """
        # Configure the base theme
        style.theme_use('clam')
        
        # Frame styles
        style.configure(
            'TFrame',
            background=cls.COLORS['bg_primary']
        )
        
        style.configure(
            'Card.TFrame',
            background=cls.COLORS['bg_secondary']
        )
        
        # Label styles
        style.configure(
            'TLabel',
            background=cls.COLORS['bg_primary'],
            foreground=cls.COLORS['text_primary'],
            font=(cls.FONTS['family'], cls.FONTS['size_normal'])
        )
        
        style.configure(
            'Title.TLabel',
            background=cls.COLORS['bg_primary'],
            foreground=cls.COLORS['text_primary'],
            font=(cls.FONTS['family'], cls.FONTS['size_header'], 'bold')
        )
        
        style.configure(
            'Secondary.TLabel',
            background=cls.COLORS['bg_primary'],
            foreground=cls.COLORS['text_secondary'],
            font=(cls.FONTS['family'], cls.FONTS['size_small'])
        )
        
        style.configure(
            'Card.TLabel',
            background=cls.COLORS['bg_secondary'],
            foreground=cls.COLORS['text_primary'],
            font=(cls.FONTS['family'], cls.FONTS['size_normal'])
        )
        
        style.configure(
            'Success.TLabel',
            background=cls.COLORS['bg_primary'],
            foreground=cls.COLORS['success'],
            font=(cls.FONTS['family'], cls.FONTS['size_normal'])
        )
        
        style.configure(
            'Error.TLabel',
            background=cls.COLORS['bg_primary'],
            foreground=cls.COLORS['error'],
            font=(cls.FONTS['family'], cls.FONTS['size_normal'])
        )
        
        # Button styles
        style.configure(
            'TButton',
            background=cls.COLORS['bg_tertiary'],
            foreground=cls.COLORS['text_primary'],
            font=(cls.FONTS['family'], cls.FONTS['size_normal']),
            padding=(cls.SPACING['md'], cls.SPACING['sm']),
            borderwidth=0
        )
        
        style.map(
            'TButton',
            background=[
                ('active', cls.COLORS['bg_hover']),
                ('disabled', cls.COLORS['bg_secondary'])
            ],
            foreground=[
                ('disabled', cls.COLORS['text_disabled'])
            ]
        )
        
        # Primary action button (accent color)
        style.configure(
            'Accent.TButton',
            background=cls.COLORS['accent'],
            foreground=cls.COLORS['text_primary'],
            font=(cls.FONTS['family'], cls.FONTS['size_large'], 'bold'),
            padding=(cls.SPACING['lg'], cls.SPACING['md']),
            borderwidth=0
        )
        
        style.map(
            'Accent.TButton',
            background=[
                ('active', cls.COLORS['accent_hover']),
                ('disabled', cls.COLORS['bg_secondary'])
            ]
        )
        
        # Secondary button
        style.configure(
            'Secondary.TButton',
            background=cls.COLORS['bg_secondary'],
            foreground=cls.COLORS['text_secondary'],
            font=(cls.FONTS['family'], cls.FONTS['size_small']),
            padding=(cls.SPACING['sm'], cls.SPACING['xs']),
            borderwidth=1
        )
        
        # Entry styles
        style.configure(
            'TEntry',
            fieldbackground=cls.COLORS['bg_input'],
            foreground=cls.COLORS['text_primary'],
            insertcolor=cls.COLORS['text_primary'],
            padding=cls.SPACING['sm'],
            borderwidth=1,
            relief='flat'
        )
        
        style.map(
            'TEntry',
            fieldbackground=[
                ('focus', cls.COLORS['bg_input']),
                ('disabled', cls.COLORS['bg_secondary'])
            ],
            bordercolor=[
                ('focus', cls.COLORS['border_focus']),
                ('!focus', cls.COLORS['border'])
            ]
        )
        
        # Spinbox styles
        style.configure(
            'TSpinbox',
            fieldbackground=cls.COLORS['bg_input'],
            foreground=cls.COLORS['text_primary'],
            arrowcolor=cls.COLORS['text_secondary'],
            insertcolor=cls.COLORS['text_primary'],
            padding=cls.SPACING['sm'],
            borderwidth=1
        )
        
        # Progressbar
        style.configure(
            'TProgressbar',
            background=cls.COLORS['accent'],
            troughcolor=cls.COLORS['bg_secondary'],
            borderwidth=0,
            thickness=8
        )
        
        # Separator
        style.configure(
            'TSeparator',
            background=cls.COLORS['border']
        )
        
        # Scrollbar
        style.configure(
            'TScrollbar',
            background=cls.COLORS['scrollbar_thumb'],
            troughcolor=cls.COLORS['scrollbar_bg'],
            borderwidth=0,
            arrowsize=0
        )
        
        style.map(
            'TScrollbar',
            background=[
                ('active', cls.COLORS['scrollbar_thumb_hover'])
            ]
        )
    
    @classmethod
    def get_font(cls, size: str = 'normal', bold: bool = False) -> tuple:
        """
        Get a font tuple for the specified size.
        
        Args:
            size: 'small', 'normal', 'large', 'title', or 'header'
            bold: Whether the font should be bold
            
        Returns:
            Font tuple (family, size, weight)
        """
        size_key = f'size_{size}'
        font_size = cls.FONTS.get(size_key, cls.FONTS['size_normal'])
        weight = 'bold' if bold else 'normal'
        return (cls.FONTS['family'], font_size, weight)
