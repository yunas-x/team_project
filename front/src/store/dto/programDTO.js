import ProgramModel from "../../models/programModel";

export class ProgramDTO {
    program_id;
    program_name;
    degree_id;
    degree;
    duration;
    field; // FieldDTO
    university; // UniversityDTO
}

export function mapProgramDTOToModel(dto) {
    return new ProgramModel(dto.program_id, dto.program_name, dto.university.university_id, dto.field.field_code,
        dto.degree_id, dto.duration);
}