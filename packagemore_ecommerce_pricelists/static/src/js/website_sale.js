odoo.define('packagemore_ecommerce_pricelists.website_sale_inherit', function (require) {
    'use strict';

    var websiteSaleWidget = require('website_sale.website_sale');

    websiteSaleWidget.WebsiteSale.include({

        /**
         * @override
         */
        start: function () {
            this._super.apply(this, arguments);
            var $qty = $('input[name="add_qty"]');
            var $min_qty = $('input[name="qty-input"]');
            $qty.val(
                $min_qty.val());
        },
        
        /**
         * @override
         */

        _onChangeCombination: function (ev, $parent, combination) {
            this._super.apply(this, arguments);
            var $qty = $('input[name="add_qty"]');
            var $min_qty = $('input[name="qty-input"]');

            const addToCart = $parent.find('#add_to_cart_wrap_2');
            if ($qty.val() < $min_qty.val()) {
                addToCart.removeClass('d-inline-flex').addClass('d-none');
            } else {
                addToCart.removeClass('d-none').addClass('d-inline-flex');
            }
        },
    });
});
