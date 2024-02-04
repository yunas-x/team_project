import ModelBase from "./base/modelBase";

export default class FieldOfStudyModel extends ModelBase {
    universityId;

    constructor(id, name, universityId) {
        super(id, name);

        this.universityId = universityId;
    }
}