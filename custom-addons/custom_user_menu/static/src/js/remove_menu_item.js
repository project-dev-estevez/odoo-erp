odoo.define('custom_user_menu.hide_documentation', [], function(require) {
    'use strict';
    
    const { registry } = require('@web/core/registry');
    const { session } = require('@web/session'); // Ruta correcta en Odoo 18
    
    // Sobrescribir el manifiesto de la PWA
    session.manifest = '/custom_user_menu/static/src/manifest.json';
    
    // Eliminar ítems del menú de usuario
    const userMenuRegistry = registry.category('user_menuitems');
    userMenuRegistry.remove('documentation');
    userMenuRegistry.remove('support');
    userMenuRegistry.remove('odoo_account');
});