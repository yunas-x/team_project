import {action, makeObservable, observable} from "mobx";

export default class StoreBase {
    items = [];

    constructor() {
        makeObservable({
            items: observable,
            setNewItems: action,
        })
    }

    setNewItems(items) {
        this.items = items;
    }
}