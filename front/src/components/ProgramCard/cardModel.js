export class CardModel {
    programName;

    constructor(id, programName, fieldOfStudyName, universityName, degreeName, city, yearCount) {
        this.id = id;
        this.programName = programName;
        this.fieldOfStudyName = fieldOfStudyName;
        this.universityName = universityName;
        this.degreeName = degreeName;
        this.city = city;
        this.yearCount = yearCount;
    }
}