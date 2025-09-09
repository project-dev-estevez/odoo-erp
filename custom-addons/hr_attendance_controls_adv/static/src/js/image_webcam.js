/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { ImageField } from '@web/views/fields/image/image_field';
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { ImageWebcamDialog } from "./image_webcam_dialog"

patch(ImageField.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.notificationService = useService("notification");
    },

    onWebcam(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        
        var self = this;
        if (window.location.protocol !== "https:") {
            this.notificationService.add(
                _t("https Failed: Warning! WEBCAM MAY ONLY WORKS WITH HTTPS CONNECTIONS. So your Odoo instance must be configured in https mode."), 
                { type: "danger" }
            );
            return;
        }else{
            self.dialog.add(ImageWebcamDialog, {
                uploadWebcamImage: (data) => this.uploadWebcamImage(data),
            });
        }    
    },

    async uploadWebcamImage({ data }) {
        if (data){
            data = data.split(',')[1];
            return this.props.record.update({ [this.props.name]: data || false });
        }
    }

});
