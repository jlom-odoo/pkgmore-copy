/** @odoo-module */
import publicWidget from 'web.public.widget';
publicWidget.registry.PortalHomeCounters.include({
    _getCountersAlwaysDisplayed() {
        return this._super(...arguments).concat(['pricelist_count']);
    },
});