/** @odoo-module **/
import { registry } from "@web/core/registry";

import { Component } from  "@odoo/owl";

class MyClientAction extends Component {}
MyClientAction.template = "estate.MyClientAction";

registry.category("actions").add("estate.MyClientAction", MyClientAction);
