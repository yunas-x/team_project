import FieldOfStudyModel from '../../models/fieldOfStudyModel'

export class FieldOfStudyDTO {
    field_code;
    field_name;
    field_group_code;
    field_group_name;
}

export function mapFieldOfStudyDTOToModel(dto) {
    return new FieldOfStudyModel(dto.field_code, dto.field_name, dto.field_group_code, dto.field_group_name);
}