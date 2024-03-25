import {action, computed, makeObservable} from "mobx";
import {ProgramSelectionModel} from "../../models/programSelectionModel";

export class ProgramSelectionService {
    selectedUniversityModel;
    selectedFieldOfStudyIdList = [];
    selectedDegreeIdList = [];

    constructor(universityService, fieldOfStudyService, programService, degreeStore) {
        this.universityService = universityService;
        this.fieldOfStudyService = fieldOfStudyService;
        this.programService = programService;
        this.degreeStore = degreeStore;

        makeObservable({
            getPrograms: computed,
            updateSelectedInfo: action,
        })
    }

    getPrograms(countToSkip, countToTake) {
        if (!this.selectedUniversityModel) {
            return [];
        }

        const programModelIdListOfUniversity = this.programService.store.items.map(program => program.id);
        let fullProgramInfoList = this.selectedUniversityModel.allProgramDataList.filter(data => programModelIdListOfUniversity.includes(data.programId))

        fullProgramInfoList = fullProgramInfoList.slice(countToSkip, countToSkip + countToTake);

        if (this.selectedFieldOfStudyIdList.length + this.selectedDegreeIdList.length === 0) {
            return this.#createSelectionModels(fullProgramInfoList)
        }

        let fullFillData = [...fullProgramInfoList]

        if (this.selectedFieldOfStudyIdList.length !== 0) {
            fullFillData = [...fullFillData, this.selectedUniversityModel.allProgramDataList.filter(data => this.selectedFieldOfStudyIdList.includes(data.fieldOfStudyId))]
        }

        if (this.selectedDegreeIdList.length !== 0) {
            fullFillData = [...fullFillData, this.selectedUniversityModel.allProgramDataList.filter(data => this.selectedDegreeIdList.includes(data.degreeId))]
        }

        return this.#createSelectionModels(fullFillData);
    }

    updateSelectedInfo(universityId, fieldOfStudyIdList, degreeIdList) {
        this.selectedUniversityModel = this.universityService.getUniversityModel(universityId);
        this.selectedFieldOfStudyIdList = [...fieldOfStudyIdList];
        this.selectedDegreeIdList = [...degreeIdList];
    }

    #createSelectionModels(allProgramDataList) {
        return allProgramDataList.map(data => new ProgramSelectionModel(this.selectedUniversityModel,
            this.fieldOfStudyService.getFieldOfStudyModel(data.fieldOfStudyId),
            this.programService.getProgramModel(data.programId),
            this.degreeStore.items.find(model => model.id === data.degreeId),
            data.yearCount))
    }
}