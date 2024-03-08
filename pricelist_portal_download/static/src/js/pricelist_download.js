odoo.define('pricelist_portal_download.pricelist_portal_download', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;
    if ($.blockUI) {
        $.blockUI.defaults.baseZ = 2147483647;
        $.blockUI.defaults.css.border = '0';
        $.blockUI.defaults.css["background-color"] = '';
        $.blockUI.defaults.overlayCSS["opacity"] = '0.9';
    }
    publicWidget.registry.captchaAuth = publicWidget.Widget.extend({
        selector: '#pricelist_portal_download',
        events: { 'submit #pricelist_download': '_getPricelist' },

        _getPricelist: function (ev) {
            ev.preventDefault()
            var form = $(ev.currentTarget)
            var actionUrl = form.attr('action');
            var formData = form.serializeArray()
            var objIndex = formData.findIndex((obj => obj.name == "pricelist_product_categ"));
            if(objIndex && formData[objIndex]){ formData[objIndex].value = $("#pricelist_product_categ").val()}
            if ($.blockUI) {
                var msg = _t("Downloading....");
                $.blockUI({
                    'message': '<h2 class="text-white"><img src="/web/static/img/spin.png" class="fa-pulse"/>' +
                        '    <br />' + msg +
                        '</h2>'
                });
            }
            $.ajax({
                type: "POST",
                url: actionUrl,
                data: formData, // serializes the form's elements.
                xhrFields: { responseType: 'blob' },
                success: function (blob, status, xhr) {
                    var filename = "";
                    var extension = $("#pricelist_file_type").val() == "pdf" ? ".pdf" : ".xlsx"
                    filename = "Product Pricelist - " + new Date().toLocaleDateString() + extension
                    if (typeof window.navigator.msSaveBlob !== 'undefined') {
                        window.navigator.msSaveBlob(blob, filename);
                    } else {
                        var URL = window.URL || window.webkitURL;
                        var downloadUrl = URL.createObjectURL(blob);
                        if (filename) {
                            var a = document.createElement("a");
                            if (typeof a.download === 'undefined') { window.location.href = downloadUrl;
                            } else {
                                a.href = downloadUrl;
                                a.download = filename;
                                document.body.appendChild(a);
                                a.click();
                            }
                        } else {window.location.href = downloadUrl;}
                        setTimeout(function () { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
                    }
                    if ($.blockUI) {  $.unblockUI(); }
                },
                error: function (request, status, error) {
                    if ($.blockUI) { $.unblockUI();}
                    alert(error);
                }
            });
        },
    })
})