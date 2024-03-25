import StoreBase from "./storeBase";
import {action, makeObservable, observable} from "mobx";
import {checkAreArraysEqual} from "../../helpers/listHelpers";
import {mockData} from "../../helpers/mock";

export default class ServiceBase {
    isLoading = false;

    constructor() {
        this.store = this.createStore();

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

        // const resultList = [];
        //
        // let offset = 0;
        // const count = 99;
        //
        // let previousData;
        //
        // while (true) {
        //     const data = await this.fetchData(offset, count);
        //
        //     if (!data || data.length === 0 || checkAreArraysEqual(previousData, data)) {
        //         break;
        //     }
        //
        //     previousData = data;
        //
        //     resultList.push(...data);
        //     offset += count;
        // }
        //
        // this.store.setNewItems(resultList.map(dto => this.mapDTOToModel(dto)));

        this.load();

        this.setIsLoading(false);
    }

    _startLoading() {
        this.store.setNewItems([]);
        this.setIsLoading(true);
    }

    /**
     * Obtains the data and returns a list of dto
     */
    async fetchData(offset, count) {
        throw new Error("Method 'fetchData()' must be implemented.");
    }

    load() {

    }

    mapDTOToModel(dto) {
        throw new Error("Method 'mapDTOToModel()' must be implemented.");
    }

    createStore() {
        return new StoreBase();
    }

    setIsLoading(isLoading) {
        this.isLoading = isLoading;
    }
}