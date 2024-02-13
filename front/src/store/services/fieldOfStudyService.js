import ServiceBase from "../base/serviceBase";
import {FieldOfStudyDTO, mapFieldOfStudyDTOToModel} from "../dto/fieldOfStudyDTO";
import fetchFieldsOfStudy from "../../api/fetchFieldsOfStudy";

export class FieldOfStudyService extends ServiceBase {
    async fetchData(offset, count) {
        const fieldsJSON = await fetchFieldsOfStudy(offset, count);

        return fieldsJSON.map(json => Object.assign(new FieldOfStudyDTO(), json))
    }

    mapDTOToModel(dto) {
        return mapFieldOfStudyDTOToModel(dto);
    }
}