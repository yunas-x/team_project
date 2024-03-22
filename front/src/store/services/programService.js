import {mapProgramDTOToModel, ProgramDTO} from "../dto/programDTO";
import {fetchPrograms, fetchFilteredPrograms} from "../../api/fetchPrograms";
import FilterServiceBase from "../base/filterServiceBase";
import {FieldOfStudyDTO} from "../dto/fieldOfStudyDTO";

export class ProgramService extends FilterServiceBase {
    async fetchData(offset, count) {
        //const programsJSON = await fetchPrograms(offset, count);
        //console.log(programsJSON)
        //return programsJSON.map(json => Object.assign(new ProgramDTO(), json))

        if (offset > 2) {
            return new Promise(resolve => resolve([]));
        }
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve([new ProgramDTO(1, "Program1"), new ProgramDTO(2, "Program2")])
            }, 1000)
        });
    }

    async fetchFilteredData(filterObject, offset, count) {
        //const programsJSON = await fetchFilteredPrograms(filterObject, offset, count);

        //return programsJSON.map(json => Object.assign(new ProgramDTO(), json))
        return []
    }

    mapDTOToModel(dto) {
        return mapProgramDTOToModel(dto);
    }
}