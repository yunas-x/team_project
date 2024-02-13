import ServiceBase from "./serviceBase";
import {action, makeObservable, observable} from "mobx";
import {checkAreArraysEqual} from "../../helpers/listHelpers";

export default class FilterServiceBase extends ServiceBase {
    constructor() {
        super();

        makeObservable(this, {
            loadFilteredData: action,
        });
    }

    async loadFilteredData(filterObject) {
        this._startLoading();

        const resultList = [];

        let offset = 0;
        const count = 99;

        let previousData;

        while (true) {
            const data = await this.fetchFilteredData(filterObject, offset, count);

            if (!data || data.length === 0 || checkAreArraysEqual(previousData, data)) {
                break;
            }

            previousData = data;

            resultList.push(...data);
            offset += count;
        }

        this.store.setNewItems(resultList.map(dto => this.mapDTOToModel(dto)));

        this.setIsLoading(false);
    }

    /**
     * Obtains the filtered data and returns a list of dto
     */
    async fetchFilteredData(filterObject, offset, count) {
        throw new Error("Method 'fetchFilteredData()' must be implemented.");
    }
}