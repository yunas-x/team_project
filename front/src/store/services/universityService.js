import ServiceBase from "../base/serviceBase";
import {mapUniversityDTOToModel, UniversityDTO} from "../dto/universityDTO";
import {universities} from "../../helpers/mock";

export class UniversityService extends ServiceBase {
    async fetchData(offset, count) {
        if (offset > 2) {
            return new Promise(resolve => resolve([]));
        }
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve([new UniversityDTO(1, "НИУ ВШЭ"), new UniversityDTO(2, "ПНИПУ")])
            }, 1000)
        });

        //return (await fetchUniversities()).map(json => Object.assign(new UniversityDTO(), json));
    }

    load() {
        this.store.setNewItems(universities);
    }

    getUniversityModel(id) {
        return this.store.items.find(university => university.id === id);
    }

    mapDTOToModel(dto) {
        return mapUniversityDTOToModel(dto);
    }
}