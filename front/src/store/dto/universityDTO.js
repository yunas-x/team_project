import UniversityModel from "../../models/universityModel";
import {AllProgramData} from "../../models/allProgramData";

export class UniversityDTO {
    university_id;
    university_name;
    city;

    constructor(id, name, cityName) {
        this.university_id = id;
        this.university_name = name;
        this.city = cityName;
    }
}

export function mapUniversityDTOToModel(dto, programModelList) {
    const universityPrograms = programModelList.filter(programModel => programModel.universityId === dto.university_id);

    const allProgramDataList = universityPrograms.map(programModel => new AllProgramData(programModel.id, programModel.fieldId,
        programModel.degreeId, programModel.yearCount))

    return new UniversityModel(dto.university_id, dto.university_name, dto.city, allProgramDataList);
}