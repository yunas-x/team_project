import StoreBase from "./storeBase";
import {action, makeObservable, observable} from "mobx";

export default class ServiceBase {
    isLoading = false;

    constructor() {
        this.store = this.createStore();

        makeObservable(this, {
            isLoading: observable,
            loadData: action,
            setIsLoading: action,
        });
    }

    /**
     * Makes request to obtain the data to store it.
     */
    loadData() {
        this._startLoading();

        this.fetchData().then(response => {
            console.log("after fetch " + response[0]?.name)
            this.store.setNewItems(response.map(dto => this.mapDTOToModel(dto)));

            this.setIsLoading(false);
        })
    }

    loadDataById(idList) {
        this._startLoading();

        this.fetchDataById(idList).then(response => {
            console.log("after fetch " + response[0]?.name)
            this.store.setNewItems(response.map(dto => this.mapDTOToModel(dto)));

            this.setIsLoading(false);
        })
    }

    _startLoading() {
        this.store.setNewItems([]);
        this.setIsLoading(true);
    }

    /**
     * Obtains the data and returns a list of dto
     */
    async fetchData() {
        throw new Error("Method 'fetchData()' must be implemented.");
    }

    /**
     * Obtains the data filtered by ids and returns a list of dto
     */
    async fetchDataById(idList) {
        throw new Error("Method 'fetchDataById()' must be implemented.");
    }

    mapDTOToModel(dto) {
        throw new Error("Method 'mapDTOToModel()' must be implemented.");
    }

    createStore() {
        return new StoreBase();
    }

    setIsLoading(isLoading: boolean) {
        this.isLoading = isLoading;
    }
}