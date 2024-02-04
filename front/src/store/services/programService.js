import ServiceBase from "../base/serviceBase";
import {mapProgramDTOToModel, ProgramDTO} from "../dto/programDTO";

export class ProgramService extends ServiceBase {
    async fetchDataById(idList) {
        return new Promise((resolve) => {
            setTimeout(() => {
                let filtered = [new ProgramDTO(1, "Жёсткая программа", 1, 1),
                    new ProgramDTO(2, "Жёсткая программа2", 1, 1),
                    new ProgramDTO(3, "Не такая жёсткая программа", 2, 2)]
                    .filter(dto => dto.universityId === idList[0]);

                if (idList.length === 2) {
                    filtered = filtered.filter(dto => dto.fieldOfStudyId === idList[1])
                }

                resolve(filtered)
            }, 1000)
        });

        //return (await fetchUniversities()).map(json => Object.assign(new UniversityDTO(), json));
    }

    mapDTOToModel(dto) {
        return mapProgramDTOToModel(dto);
    }
}