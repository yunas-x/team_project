import FieldOfStudyModel from '../../models/fieldOfStudyModel'

export class FieldOfStudyDTO {
    id;
    name;
    universityId

    constructor(id, name, universityId) {
        this.id = id;
        this.name = name;
        this.universityId = universityId;
    }
}

export function mapFieldOfStudyDTOToModel(dto) {
    return new FieldOfStudyModel(dto.id, dto.name, dto.universityId);
}