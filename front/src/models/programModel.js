import ModelBase from "./base/modelBase";

export default class ProgramModel extends ModelBase {
    constructor(id, name, universityId, fieldId, degreeId, yearCount) {
        super(id, name);

        this.universityId = universityId;
        this.fieldId = fieldId;
        this.degreeId = degreeId;
        this.yearCount = yearCount;
    }
}