import {action, computed, makeObservable, observable} from "mobx";

const readyCount = 2

export const getIsSelected = (programsSelectionModel, selectedList) => {
    const found = selectedList.find(selectedModel => areSelectionModelsEqual(programsSelectionModel, selectedModel));

    return found !== undefined;
}

const areSelectionModelsEqual = (firstSelectionModel, secondSelectionModel) => {
    return firstSelectionModel.universityModel.id === secondSelectionModel.universityModel.id &&
        firstSelectionModel.fieldOfStudyModel.id === secondSelectionModel.fieldOfStudyModel.id &&
        firstSelectionModel.programModel.id === secondSelectionModel.programModel.id &&
        firstSelectionModel.degreeModel.id === secondSelectionModel.degreeModel.id;
}

export class ProgramsSelectionController {
    selectedList = [];

    constructor() {
        makeObservable(this, {
            selectedList: observable,
            isReady: computed,
            setSelected: action,
            removeSelected: action,
        })
    }

    setSelected(programsSelectionModel) {
        console.log("setSelected")
        if (this.selectedList.filter(selectedModel => selectedModel.degreeModel.id !== programsSelectionModel.degreeModel.id).length !== 0) {
            console.log("firstReturn")
            return;
        }

        if (this.selectedList.length === readyCount) {
            console.log("secondReturn")
            return;
        }

        this.selectedList = [...this.selectedList, programsSelectionModel];
    }

    removeSelected(programsSelectionModel) {
        this.selectedList = this.selectedList.filter(selectionModel => !areSelectionModelsEqual(selectionModel, programsSelectionModel));
    }

    get isReady() {
        return this.selectedList.length === readyCount;
    }
}