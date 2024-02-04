import {FieldOfStudyDTO} from "./fieldOfStudyDTO";
import ProgramModel from "../../models/programModel";

export class ProgramDTO extends FieldOfStudyDTO {
    fieldOfStudyId;

    constructor(id, name, universityId, fieldOfStudyId) {
        super(id, name, universityId);

        this.fieldOfStudyId = fieldOfStudyId;
    }
}

export function mapProgramDTOToModel(dto) {
    return new ProgramModel(dto.id, dto.name, dto.universityId, dto.fieldOfStudyId);
}