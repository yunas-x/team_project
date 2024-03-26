import {action, computed, makeObservable, observable} from "mobx";
import {ProgramSelectionModel} from "../../models/programSelectionModel";
import {checkAreArraysEqual} from "../../helpers/listHelpers";

export class ProgramSelectionService {
    selectedUniversityModel;
    selectedFieldOfStudyIdList = [];
    selectedDegreeIdList = [];
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
        this.selectedFieldOfStudyIdList = [...fieldOfStudyIdList];
        this.selectedDegreeIdList = [...degreeIdList];

        if (!this.selectedUniversityModel)
        {
            return;
        }

        const programModelIdListOfUniversity = this.programService.store.items.map(program => program.id);
        let fullProgramInfoList = this.selectedUniversityModel.allProgramDataList.filter(data => programModelIdListOfUniversity.includes(data.programId))

        if (this.selectedFieldOfStudyIdList.length !== 0) {
            fullProgramInfoList = fullProgramInfoList.filter(data => this.selectedFieldOfStudyIdList.includes(data.fieldOfStudyId))
        }

        if (this.selectedDegreeIdList.length !== 0) {
            fullProgramInfoList = fullProgramInfoList.filter(data => this.selectedDegreeIdList.includes(data.degreeId))
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