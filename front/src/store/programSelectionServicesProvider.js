import {UniversityService} from "./services/universityService";
import {FieldOfStudyService} from "./services/fieldOfStudyService";
import {ProgramService} from "./services/programService";
import StoreBase from "./base/storeBase";
import ModelBase from "../models/base/modelBase";

export default class ProgramSelectionServicesProvider {
    universityService = new UniversityService();
    fieldOfStudyService = new FieldOfStudyService();
    programService = new ProgramService();
    degreeLevelStore = new StoreBase();

    loadServices() {
        this.universityService.loadAllData();
        this.fieldOfStudyService.loadAllData();
        this.programService.loadAllData();

        this._initDegreeStore()
    }

    _initDegreeStore() {
        const items = [
            new ModelBase(3, "Бакалавриат"),
            new ModelBase(4, "Магистратура"),
            new ModelBase(5, "Специалитет"),
        ]

        this.degreeLevelStore.setNewItems(items);
    }
}