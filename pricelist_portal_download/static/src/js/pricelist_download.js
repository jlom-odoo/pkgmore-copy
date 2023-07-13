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
        events: {
            'submit #pricelist_download': '_getPricelist'
        },

//        start: function () {
            // $("#pricelist_product_categ").select2({
            //     placeholder: "Select Category", 
            //     multiple: true,
            // });
//            $("#pricelist_product_categ").select2({ placeholder: "Select Categories" });
//        },

        _getPricelist: function (ev) {

            ev.preventDefault()
            var form = $(ev.currentTarget)

            var actionUrl = form.attr('action');
            var formData = form.serializeArray()
            var objIndex = formData.findIndex((obj => obj.name == "pricelist_product_categ"));
            if(objIndex && formData[objIndex]){
                formData[objIndex].value = $("#pricelist_product_categ").val()
            }

            // formData.set("pricelist_product_categ", $("#pricelist_product_categ").val())
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
                xhrFields: {
                    responseType: 'blob' // to avoid binary data being mangled on charset conversion
                },
                success: function (blob, status, xhr) {
                    // console.log("blob", blob)
                    // check for a filename
                    var filename = "";

                    var extension = $("#pricelist_file_type").val() == "pdf" ? ".pdf" : ".xlsx"
                    filename = "Product Pricelist - " + new Date().toLocaleDateString() + extension
                    // var disposition = xhr.getResponseHeader('Content-Disposition');
                    // if (disposition && disposition.indexOf('attachment') !== -1) {
                    //     var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    //     var matches = filenameRegex.exec(disposition);
                    //     if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
                    // }

                    if (typeof window.navigator.msSaveBlob !== 'undefined') {
                        // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                        window.navigator.msSaveBlob(blob, filename);
                    } else {
                        var URL = window.URL || window.webkitURL;
                        var downloadUrl = URL.createObjectURL(blob);

                        if (filename) {
                            // use HTML5 a[download] attribute to specify filename
                            var a = document.createElement("a");
                            // safari doesn't support this yet
                            if (typeof a.download === 'undefined') {
                                window.location.href = downloadUrl;
                            } else {
                                a.href = downloadUrl;
                                a.download = filename;
                                document.body.appendChild(a);
                                a.click();
                            }
                        } else {
                            window.location.href = downloadUrl;
                        }

                        setTimeout(function () { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
                    }
                    if ($.blockUI) {
                        $.unblockUI();
                    }
                },
                error: function (request, status, error) {
                    if ($.blockUI) {
                        $.unblockUI();
                    }
                    alert(error);

                }
            });
        },
    })
})