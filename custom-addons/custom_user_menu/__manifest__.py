{
    'name': 'Custom User Menu',
    'version': '1.0',
    'depends': ['web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'custom_user_menu/static/src/js/remove_menu_item.js',
        ],
        'web.assets_common': [
            'custom_user_menu/static/src/manifest.json',
            'custom_user_menu/static/src/img/icon-192x192.png',
            'custom_user_menu/static/src/img/icon-512x512.png',
        ],
    },
    'installable': True,
}