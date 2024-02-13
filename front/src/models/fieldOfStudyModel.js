import ModelBase from "./base/modelBase";

export default class FieldOfStudyModel extends ModelBase {
    constructor(fieldCode, fieldName, fieldGroupCode, fieldGroupName) {
        super(fieldCode, fieldName, fieldCode + " " + fieldName);

        this.fieldGroupCode = fieldGroupCode;
        this.fieldGroupName = fieldGroupName;
    }
}