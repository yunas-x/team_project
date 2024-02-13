export class FilterProgram {
    field_code;
    field_group_code;
    degree_id;

    constructor(fieldOfStudyCodes, fieldOfStudyGroupCodes, degreesId) {
        this.field_code = fieldOfStudyCodes;
        this.field_group_code = fieldOfStudyGroupCodes
        this.degree_id = degreesId;
    }
}