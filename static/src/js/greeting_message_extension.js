odoo.define('extended_attendance.greeting_message', function (require) {
    "use strict";
    console.log("Iniciando extended_attendance.greeting_message");

    const { patch } = require('@web/core/utils/patch');
    const GreetingMessage = require('hr_attendance.greeting_message');

    console.log("GreetingMessage importado:", GreetingMessage);

    patch(GreetingMessage.prototype, 'extended_attendance.greeting_message', {
        welcome_message: function() {
            console.log("welcome_message llamado");
            this._setQuickTimeout();
        },
        farewell_message: function() {
            console.log("farewell_message llamado");
            this._setQuickTimeout();
        },
        _setQuickTimeout: function() {
            console.log("_setQuickTimeout llamado");
            var self = this;
            this.return_to_main_menu = setTimeout(function() {
                console.log("Ejecutando acción después del timeout");
                self.do_action(self.next_action, {clear_breadcrumbs: true});
            }, 1000);
        }
    });

    console.log("Patch aplicado a GreetingMessage");
    return GreetingMessage;
});
