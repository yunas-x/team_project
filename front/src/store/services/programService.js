import {mapProgramDTOToModel, ProgramDTO} from "../dto/programDTO";
import {fetchPrograms, fetchFilteredPrograms} from "../../api/fetchPrograms";
import FilterServiceBase from "../base/filterServiceBase";
import {FieldOfStudyDTO} from "../dto/fieldOfStudyDTO";
import {programs} from "../../helpers/mock";
import {action, computed, makeObservable, observable} from "mobx";

export class ProgramService extends FilterServiceBase {
    constructor() {
        super();

        makeObservable({
            getTotalProgramCount: computed,
        })
    }

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

    load() {
        this.store.setNewItems(programs);
    }

    tempLoadByFilter(universityModel, fieldOfStudyIdList, degreeIdList) {
        this.setIsLoading(true)
        if (!universityModel) {
            this.store.setNewItems([]);

            this.setIsLoading(false)

            return;
        }

        //let resultPrograms = [programs.filter(program => universityModel.allProgramDataList.filter(data => data.programId === program.id).length > 0)]
        let resultPrograms = programs.filter(program => universityModel.allProgramDataList.filter(data => data.programId === program.id).length > 0)

        if (fieldOfStudyIdList && fieldOfStudyIdList.length !== 0) {
            resultPrograms = [resultPrograms.filter(program => universityModel.allProgramDataList
                .filter(data => data.programId === program.id && fieldOfStudyIdList.includes(data.fieldOfStudyId)).length > 0)]
        }

        if (degreeIdList && degreeIdList.length !== 0) {
            resultPrograms = [resultPrograms.filter(program => universityModel.allProgramDataList
                .filter(data => data.programId === program.id && fieldOfStudyIdList.includes(data.fieldOfStudyId) && degreeIdList.includes(data.degreeId)).length > 0)]
        }

        this.store.setNewItems(resultPrograms)
        this.setIsLoading(false)
    }

    getTotalProgramsCount() {
        return this.store.items.length;
    }

    getProgramsByOffset(countToSkip, count) {
        return this.store.items.slice(countToSkip, countToSkip + count)
    }

    getProgramModel(id) {
        return this.store.items.find(program => program.id === id);
    }

    mapDTOToModel(dto) {
        return mapProgramDTOToModel(dto);
    }
}