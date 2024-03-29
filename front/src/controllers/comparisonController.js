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
import {InfographicsService} from "../store/services/infographicsService";

export class ComparisonController {
    isLoading = false;
    isComparisonOpened = false;
    comparisonData = undefined;
    infographicsService = new InfographicsService();

    constructor() {
        makeObservable(this, {
            isLoading: observable,
            isComparisonOpened: observable,
            comparisonData: observable,
            showComparison: action,
            closeComparison: action,
            setIsLoading: action,
        })
    }

    async showComparison(firstProgramSelectionModel, secondProgramSelectionModel) {
        this.setIsLoading(true);
        this.isComparisonOpened = true;

        await this.infographicsService.loadAllData({
            firstProgramId: firstProgramSelectionModel.programModel.id,
            secondProgramId: secondProgramSelectionModel.programModel.id,
        });

        this.comparisonData = this.infographicsService.store.items[0];

        // this.comparisonData = new ComparisonData(this.#createProgramComparisonData(firstProgramSelectionModel, pieDataList1, lineChartDataList1),
        //     this.#createProgramComparisonData(secondProgramSelectionModel, pieDataList2, lineChartDataList2),
        //     courseComparisonDataList) // mock data


        this.setIsLoading(false);
    }

    closeComparison() {
        this.isComparisonOpened = false;
    }

    setIsLoading(value) {
        this.isLoading = value;
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