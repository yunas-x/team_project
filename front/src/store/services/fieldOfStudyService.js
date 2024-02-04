import ServiceBase from "../base/serviceBase";
import {FieldOfStudyDTO, mapFieldOfStudyDTOToModel} from "../dto/fieldOfStudyDTO";

export class FieldOfStudyService extends ServiceBase {
    async fetchDataById(idList) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve([new FieldOfStudyDTO(1, "01.02.03 Жёсткое направление", 1),
                    new FieldOfStudyDTO(2, "02.04.05 Не такое жёсткое", 2)].filter(dto => dto.universityId === idList[0]))
            }, 1000)
        });

        //return (await fetchUniversities()).map(json => Object.assign(new UniversityDTO(), json));
    }

    mapDTOToModel(dto) {
        return mapFieldOfStudyDTOToModel(dto);
    }
}