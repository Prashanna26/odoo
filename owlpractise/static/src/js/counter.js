/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import {registry} from "@web/core/registry"
import { Todo } from "./todo"; 

export class Counter extends Component {
    // static Component = { Todo }
    setup() {
        this.state = useState({ value: 0 });
    }
    
    increment() {
        this.state.value = this.state.value + 1;
    }
}
Counter.template = "owlpractise.counter"
Counter.components  = {Todo}

registry.category('actions').add('owlpractise.Counter',  Counter);