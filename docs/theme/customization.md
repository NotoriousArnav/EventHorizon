# Customizing the Theme

Event Horizon is built with **Tailwind CSS**, allowing for rapid and scalable customization.

## modifying the Color Scheme

To change the primary colors (e.g., from Blue/Cyan to Green/Emerald), edit `tailwind.config.js` (if building from source) or override the utility classes in your templates.

## overriding Templates

The project uses Django's template inheritance system.
- `base.html`: The master template containing the layout, navigation, and footer.
- `home.html`: The landing page.
- `events/event_list.html`: The mission board.

To customize a page, look for the template blocks labeled "content" in the respective file.

## Static Assets

Images, fonts, and custom CSS are located in the `static/` directory.
- `static/css/`: Custom overrides.
- `static/img/`: Logos and backgrounds.

## Adding Custom JavaScript

You can add custom scripts to `templates/base.html` before the closing `</body>` tag, or link external JS files in the `<head>`.
