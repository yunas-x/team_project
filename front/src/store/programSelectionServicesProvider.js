import {UniversityService} from "./services/universityService";
import {FieldOfStudyService} from "./services/fieldOfStudyService";
import {ProgramService} from "./services/programService";
import StoreBase from "./base/storeBase";
import {degrees} from "../helpers/mock";

export default class ProgramSelectionServicesProvider {
    universityService;
    fieldOfStudyService = new FieldOfStudyService();
    programService = new ProgramService();
    degreeStore = new StoreBase();

    constructor() {
        this.universityService = new UniversityService(this.programService);
    }

    loadServices() {
        this.universityService.setIsLoading(true);

        this.fieldOfStudyService.loadAllData();
        this.programService.loadAllData().then(() =>
            this.universityService.loadAllData());

        this.#initDegreeStore()
    }

    #initDegreeStore() {
        this.degreeStore.setNewItems(degrees);
    }
}