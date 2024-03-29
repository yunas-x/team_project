import ServiceBase from "../base/serviceBase";
import {mapUniversityDTOToModel, UniversityDTO} from "../dto/universityDTO";
import fetchUniversities from "../../api/fetchUniversities";

export class UniversityService extends ServiceBase {
    constructor(programService) {
        super();

        this.programService = programService;
    }

    async _doLoadToStore() {
        // this.store.setNewItems(universities); // mock universities, import {universities} from "../../helpers/mock";

        const universitiesRawData = await fetchUniversities();
        const universityDTOList = universitiesRawData.map(json => Object.assign(new UniversityDTO(), json));

        const allProgramModels = this.programService.store.items;

        const universityModels = universityDTOList.map(dto => mapUniversityDTOToModel(dto, allProgramModels))

        this.store.setNewItems(universityModels);
    }

    getUniversityModel(id) {
        return this.store.items.find(university => university.id === id);
    }
}