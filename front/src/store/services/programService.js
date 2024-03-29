import {mapProgramDTOToModel, ProgramDTO} from "../dto/programDTO";
import {fetchPrograms} from "../../api/fetchPrograms";
import ServiceBase from "../base/serviceBase";

export class ProgramService extends ServiceBase {
    async _doLoadToStore() {
        const programsRawData = await fetchPrograms();
        const programDTOList = programsRawData.map(json => Object.assign(new ProgramDTO(), json))

        const programModels = programDTOList.map(mapProgramDTOToModel);

        this.store.setNewItems(programModels);
    }

    getProgramModel(id) {
        return this.store.items.find(program => program.id === id);
    }
}