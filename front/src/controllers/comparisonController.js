import {ComparisonData} from "../models/comparison/comparisonData";
import {ProgramComparisonData} from "../models/comparison/programComparisonData";
import {
    courseComparisonDataList,
    lineChartDataList,
    lineChartDataList1,
    lineChartDataList2,
    pieDataList, pieDataList1, pieDataList2
} from "../helpers/mock";
import {action, makeObservable, observable} from "mobx";

export class ComparisonController {
    isLoading = false;
    isComparisonOpened = false;
    comparisonData = undefined;

    constructor() {
        makeObservable(this, {
            isLoading: observable,
            isComparisonOpened: observable,
            comparisonData: observable,
            showComparison: action,
            closeComparison: action,
        })
    }


    showComparison(firstProgramSelectionModel, secondProgramSelectionModel) {
        this.isLoading = true;
        // fetch expected

        this.isComparisonOpened = true;

        this.comparisonData = new ComparisonData(this.#createProgramComparisonData(firstProgramSelectionModel, pieDataList1, lineChartDataList1),
            this.#createProgramComparisonData(secondProgramSelectionModel, pieDataList2, lineChartDataList2),
            courseComparisonDataList)


        this.isLoading = false;
    }

    closeComparison() {
        this.isComparisonOpened = false;
    }

    #createProgramComparisonData(programSelectionModel, pieDataList, lineChartDataList) {
        return new ProgramComparisonData(programSelectionModel.universityModel.displayName,
            programSelectionModel.fieldOfStudyModel.displayName,
            programSelectionModel.programModel.displayName,
            programSelectionModel.degreeModel.displayName,
            pieDataList,
            lineChartDataList)
    }
}