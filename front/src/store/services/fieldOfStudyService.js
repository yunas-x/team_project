import ServiceBase from "../base/serviceBase";
import {FieldOfStudyDTO, mapFieldOfStudyDTOToModel} from "../dto/fieldOfStudyDTO";
import fetchFieldsOfStudy from "../../api/fetchFieldsOfStudy";

export class FieldOfStudyService extends ServiceBase {
    async _doLoadToStore() {
        const fieldRawData = await fetchFieldsOfStudy();
        const fieldDTOList = fieldRawData.map(json => Object.assign(new FieldOfStudyDTO(), json))

        const fieldModels = fieldDTOList.map(mapFieldOfStudyDTOToModel);

        this.store.setNewItems(fieldModels);
    }

    getFieldOfStudyModel(id) {
        return this.store.items.find(fieldOfStudy => fieldOfStudy.id === id);
    }
}