import {mapProgramDTOToModel, ProgramDTO} from "../dto/programDTO";
import {fetchPrograms} from "../../api/fetchPrograms";
import FilterServiceBase from "../base/filterServiceBase";
import {programs} from "../../helpers/mock";

export class ProgramService extends FilterServiceBase {
    async _doLoadToStore() {
        const programsRawData = await fetchPrograms();
        const programDTOList = programsRawData.map(json => Object.assign(new ProgramDTO(), json))

        const programModels = programsRawData.map(mapProgramDTOToModel);

        this.store.setNewItems(programModels);
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

        // if (fieldOfStudyIdList && fieldOfStudyIdList.length !== 0) {
        //     resultPrograms = [resultPrograms.filter(program => universityModel.allProgramDataList
        //         .filter(data => data.programId === program.id && fieldOfStudyIdList.includes(data.fieldOfStudyId)).length > 0)]
        // }
        //
        // if (degreeIdList && degreeIdList.length !== 0) {
        //     resultPrograms = [resultPrograms.filter(program => universityModel.allProgramDataList
        //         .filter(data => data.programId === program.id && fieldOfStudyIdList.includes(data.fieldOfStudyId) && degreeIdList.includes(data.degreeId)).length > 0)]
        // }

        this.store.setNewItems(resultPrograms)
        this.setIsLoading(false)
    }

    getProgramModel(id) {
        return this.store.items.find(program => program.id === id);
    }
}