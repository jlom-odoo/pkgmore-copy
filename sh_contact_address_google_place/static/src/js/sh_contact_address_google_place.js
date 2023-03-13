/** @odoo-module **/
/* global checkVATNumber */

// import { AutoComplete } from "@web/core/autocomplete/autocomplete";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { CharField } from "@web/views/fields/char/char_field";
import { useInputField } from "@web/views/fields/input_field_hook";
import { loadJS } from "@web/core/assets";
const { onMounted, useRef, Component, useState, onWillStart, onWillUpdateProps } = owl;
import { useService } from "@web/core/utils/hooks";

export class sh_contact_address_google_place_autocomplete_char_field extends CharField {
    /**
     * The purpose of this extension
     * is to allow initialize component
     * @override
     */
    setup() {
        super.setup();

        this._rpc = useService("rpc");

        onWillStart(async () => {
            await this._fetchData();
        });

        this.inputRef = useRef("input");

        onMounted(this.onMounted);
        useInputField({ getValue: () => this.props.value || "", parse: (v) => this.parse(v), ref: this.inputRef });
    }

    /**
     * The purpose of this extension
     * is to represented component
     * in the view
     * @override
     */
    onMounted() {
        var self = this;

        // initial meter update when re-editing
        if (typeof google !== "object" || typeof google.maps !== "object") {
            return;
        }

        // mention fields which need to get from google place autocomplete object
        self.autocomplete = new google.maps.places.Autocomplete(this.inputRef.el, {
            fields: ["address_components", "geometry"],
            types: ["address"],
        });

        google.maps.event.addListener(self.autocomplete, "place_changed", self._onPlaceChanged.bind(self));
    }
    /**
     * Fetches the data.
     * Google Map API key
     * @private
     */
    async _fetchData() {
        const res = await this._rpc("/sh_get_google_api_key", {});
        this.google_api_key = res.api_key || false;
        await this.loadLibs();
    }

    /**
     * Loads the google libraries.
     *
     */
    async loadLibs() {
        if (this.google_api_key) {
            var URL = "https://maps.googleapis.com/maps/api/js?v=3&key=" + this.google_api_key + "&sensor=false&libraries=places";
            this._google_map_ready = await loadJS(URL);
        }
        return false;
    }

    /**
     * Get data when change place and
     * assign to input
     * for trigger python method
     * @private
     * @param {Event} ev
     */
    async _onPlaceChanged(ev) {
        let postcode = "";
        let street = "";
        let street2 = "";
        let city = "";
        let country = false;
        let state = false;
        let country_name = "";
        let state_name = "";
        let place_dic = {
            postcode: "",
            street: "",
            street2: "",
            city: "",
            country: false,
            state: false,
        };
        const gmapPlace = this.autocomplete.getPlace();
        if (gmapPlace.address_components !== undefined) {
            for (const component of gmapPlace.address_components) {
                const componentType = Object.values(component.types)[0];

                switch (componentType) {
                    case "postal_code": {
                        postcode = `${component.long_name}${postcode}`;
                        break;
                    }
                    case "postal_code_suffix": {
                        postcode = `${postcode}-${component.long_name}`;
                        break;
                    }

                    case "street_number": {
                        street += component.long_name;
                        break;
                    }
                    case "route": {
                        street += component.long_name;
                        break;
                    }
                    case "sublocality_level_3": {
                        street += ", " + component.long_name;
                        break;
                    }
                    case "sublocality_level_2": {
                        street += ", " + component.long_name;
                        break;
                    }
                    case "sublocality_level_1":
                        street2 = component.long_name;
                        break;
                    case "locality":
                        city = component.long_name;
                        break;
                    case "country":
                        await this._rpc("/sh_get_country_state_code", {
                            country_name: component.long_name,
                        }).then(function (data) {
                            if (data.country_code) {
                                country = data.country_code;
                            }
                            if (data.country_name) {
                                country_name = data.country_name;
                            }
                        });
                        break;
                    case "administrative_area_level_1":
                        await this._rpc("/sh_get_country_state_code", {
                            state_name: component.long_name,
                        }).then(function (data) {
                            if (data.state_code) {
                                setTimeout(function () {
                                    $("select#state_id").val(data.state_code);
                                }, 600);
                            }
                            if (data.state_code) {
                                state = data.state_code;
                            }
                            if (data.state_name) {
                                state_name = data.state_name;
                            }
                        });
                        break;
                }
            }
            place_dic.postcode = postcode;
            place_dic.street = street;
            place_dic.street2 = street2;
            place_dic.city = city;
            place_dic.country = country;
            place_dic.state = state;
            console.log("\n\n place_dic", place_dic);
            var main_string = "";
            if (street) {
                main_string += street;
            }
            if (street2) {
                main_string += ", " + street2;
            }
            if (city) {
                main_string += ", " + city;
            }
            if (state_name) {
                main_string += ", " + state_name;
            }
            if (country_name) {
                main_string += ", " + country_name;
            }
            if (postcode) {
                main_string += ", " + postcode;
            }
            console.log("\n\n place_dic", place_dic);
            var sh_place_dic = JSON.stringify(place_dic);

            // -------------------------------------
            // Write value in input and Trigger Input Change
            // -------------------------------------
            var el = document.getElementById("sh_contact_place_text");
            if (el) {
                el.value = sh_place_dic;
                el.dispatchEvent(new InputEvent("input", { bubbles: true }));
                el.dispatchEvent(new InputEvent("enter", { bubbles: true }));
                el.dispatchEvent(new InputEvent("change", { bubbles: true }));
            }
            // -------------------------------------
            // Write value in input and Trigger Input Change
            // -------------------------------------

            // -------------------------------------
            // Write value in input and Trigger Input Change
            // -------------------------------------
            var el = document.getElementById("sh_contact_place_text_main_string");
            if (el) {
                el.value = main_string;
                el.dispatchEvent(new InputEvent("input", { bubbles: true }));
                el.dispatchEvent(new InputEvent("enter", { bubbles: true }));
                el.dispatchEvent(new InputEvent("change", { bubbles: true }));
            }
            // -------------------------------------
            // Write value in input and Trigger Input Change
            // -------------------------------------
        }
    }
}

sh_contact_address_google_place_autocomplete_char_field.template = "sh_contact_address_google_place.char_field";
sh_contact_address_google_place_autocomplete_char_field.components = {
    ...CharField.components,
    //  AutoComplete,
};

registry.category("fields").add("sh_contact_address_google_place_autocomplete_char_field", sh_contact_address_google_place_autocomplete_char_field);
