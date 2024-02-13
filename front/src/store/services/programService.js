import {mapProgramDTOToModel, ProgramDTO} from "../dto/programDTO";
import {fetchPrograms, fetchFilteredPrograms} from "../../api/fetchPrograms";
import FilterServiceBase from "../base/filterServiceBase";

export class ProgramService extends FilterServiceBase {
    async fetchData(offset, count) {
        const programsJSON = await fetchPrograms(offset, count);
        console.log(programsJSON)
        return programsJSON.map(json => Object.assign(new ProgramDTO(), json))
    }

    async fetchFilteredData(filterObject, offset, count) {
        const programsJSON = await fetchFilteredPrograms(filterObject, offset, count);

        return programsJSON.map(json => Object.assign(new ProgramDTO(), json))
    }

    mapDTOToModel(dto) {
        return mapProgramDTOToModel(dto);
    }
}