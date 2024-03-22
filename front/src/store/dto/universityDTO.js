import UniversityModel from "../../models/universityModel";

export class UniversityDTO {
    id;
    name;
    field_of_studies; // [{field_code, field_name}]
    programs; // [{field_code, field_name}]

    constructor(id, name, field_of_studies, programs) {
        this.id = id;
        this.name = name;
    }
}

export function mapUniversityDTOToModel(dto) {
    return new UniversityModel(dto.id, dto.name);
}