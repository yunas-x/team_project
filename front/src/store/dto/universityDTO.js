import UniversityModel from "../../models/universityModel";

export class UniversityDTO {
    id;
    name;

    constructor(id, name) {
        this.id = id;
        this.name = name;
    }
}

export function mapUniversityDTOToModel(dto) {
    return new UniversityModel(dto.id, dto.name);
}