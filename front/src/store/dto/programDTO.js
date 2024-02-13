import ProgramModel from "../../models/programModel";

export class ProgramDTO {
    program_id;
    program_name;
    degree_id;
    degree;
    field_code;
    field_name;
    field_group_code;
    field_group_name;
}

export function mapProgramDTOToModel(dto) {
    return new ProgramModel(dto.program_id, dto.program_name, dto.field_code);
}