import FieldOfStudyModel from "./fieldOfStudyModel";

export default class ProgramModel extends FieldOfStudyModel {
    fieldOfStudy;

    constructor(id, name, university, fieldOfStudy) {
        super(id, name, university);

        this.fieldOfStudy = fieldOfStudy;
    }
}