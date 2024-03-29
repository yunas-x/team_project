import {action, computed, makeObservable, observable} from "mobx";
import {ProgramSelectionModel} from "../../models/programSelectionModel";

export class ProgramSelectionService {
    selectedUniversityModel;
    cachedPrograms = [];

    constructor(universityService, fieldOfStudyService, programService, degreeStore) {
        this.universityService = universityService;
        this.fieldOfStudyService = fieldOfStudyService;
        this.programService = programService;
        this.degreeStore = degreeStore;

        makeObservable(this, {
            cachedPrograms: observable,
            programCount: computed,
            updateSelectedInfo: action,
        })
    }

    getPrograms(countToSkip, countToTake) {
        if (!this.selectedUniversityModel) {
            return [];
        }

        const fullProgramInfoList = this.cachedPrograms.slice(countToSkip, countToSkip + countToTake);

        return this.#createSelectionModels(fullProgramInfoList, countToSkip);
    }

    get programCount() {
        if (!this.cachedPrograms) {
            return 0;
        }

        return this.cachedPrograms.length
    }

    updateSelectedInfo(universityId, fieldOfStudyIdList, degreeIdList) {
        this.selectedUniversityModel = this.universityService.getUniversityModel(universityId);

        if (!this.selectedUniversityModel)
        {
            return;
        }

        const programModelIdListOfUniversity = this.programService.store.items.filter(programModel => programModel.universityId === universityId).map(program => program.id);
        let fullProgramInfoList = this.selectedUniversityModel.allProgramDataList.filter(data => programModelIdListOfUniversity.includes(data.programId))

        if (fieldOfStudyIdList.length !== 0) {
            fullProgramInfoList = fullProgramInfoList.filter(data => fieldOfStudyIdList.includes(data.fieldOfStudyId))
        }

        if (degreeIdList.length !== 0) {
            fullProgramInfoList = fullProgramInfoList.filter(data => degreeIdList.includes(data.degreeId))
        }

        this.cachedPrograms = fullProgramInfoList;
    }

    #createSelectionModels(allProgramDataList, countToSkip) {
        return allProgramDataList.map((data, i) => new ProgramSelectionModel(i + countToSkip,
            this.selectedUniversityModel,
            this.fieldOfStudyService.getFieldOfStudyModel(data.fieldOfStudyId),
            this.programService.getProgramModel(data.programId),
            this.degreeStore.items.find(model => model.id === data.degreeId),
            data.yearCount))
    }
}