export class ProgramSelectionModel {
    constructor(id, universityModel, fieldOfStudyModel, programModel, degreeModel, yearCount) {
        this.id = id
        this.universityModel = universityModel;
        this.fieldOfStudyModel = fieldOfStudyModel;
        this.programModel = programModel;
        this.degreeModel = degreeModel;
        this.yearCount = yearCount;
    }
}