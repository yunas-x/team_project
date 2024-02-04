import {UniversityService} from "./services/universityService";
import {FieldOfStudyService} from "./services/fieldOfStudyService";
import {ProgramService} from "./services/programService";

export default class ProgramSelectionServicesProvider {
    universityService = new UniversityService();
    fieldOfStudyService = new FieldOfStudyService();
    programService = new ProgramService();
}