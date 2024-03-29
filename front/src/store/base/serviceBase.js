import StoreBase from "./storeBase";
import {action, makeObservable, observable} from "mobx";

export default class ServiceBase {
    isLoading = false;

    constructor() {
        this.store = new StoreBase();

        makeObservable(this, {
            isLoading: observable,
            loadAllData: action,
            setIsLoading: action,
        });
    }

    /**
     * Makes request to obtain the data to store it.
     */
    async loadAllData() {
        this._startLoading();

        await this._doLoadToStore();

        this.setIsLoading(false);
    }

    _startLoading() {
        this.store.setNewItems([]);
        this.setIsLoading(true);
    }

    async _doLoadToStore() {
        throw new Error("doLoadToStore must be implemented by inheritors...");
    }

    setIsLoading(isLoading) {
        this.isLoading = isLoading;
    }
}