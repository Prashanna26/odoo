/** @odoo-module */

import { Component } from "@odoo/owl";

export class Todo extends Component {
    setup() {
        this.todo = {id: 3, description: 'buy milk', done: false};
    }
}

Todo.template = "owlpractise.todo"