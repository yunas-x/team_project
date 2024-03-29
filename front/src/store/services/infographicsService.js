import ServiceBase from "../base/serviceBase";
import {fetchInfographics} from "../../api/fetchInfographics";
import {InfographicsDTO} from "../dto/infographicsDTO";
import {PieData} from "../../models/comparison/pieData";
import {LineChartData} from "../../models/comparison/lineChartData";
import {ProgramComparisonData} from "../../models/comparison/programComparisonData";
import {CourseComparisonData} from "../../models/comparison/courseComparisonData";
import {ComparisonData} from "../../models/comparison/comparisonData";

export class InfographicsService extends ServiceBase {
    async _doLoadToStore(getParams) {
        const infographicsRawData = await fetchInfographics(getParams.firstProgramId, getParams.secondProgramId);
        const infographicsDTO = Object.assign(new InfographicsDTO(), infographicsRawData)

        this.store.setNewItems([this.#createComparisonData(infographicsDTO)])
    }

    #createComparisonData(dto) {
        const [firstProgramComparisonData, secondProgramComparisonData] = this.#createTwoProgramComparisonData(dto);

        const courseComparisonDataList = this.#createCourseComparisonData(dto);

        return new ComparisonData(firstProgramComparisonData, secondProgramComparisonData, courseComparisonDataList)
    }

    #createTwoProgramComparisonData(dto) {
        const [firstPieData, secondPieData] = this.#createTwoPieData(dto);
        const [firstLineData, secondLineData] = this.#createTwoLineData(dto);

        const firstProgram = dto.first_program;
        const firstProgramComparisonData = new ProgramComparisonData(firstProgram.university.university_name,
            firstProgram.field.field_code + " " + firstProgram.field.field_name,
            firstProgram.program_name,
            firstProgram.degree,
            firstPieData,
            firstLineData);

        const secondProgram = dto.second_program;
        const secondProgramComparisonData = new ProgramComparisonData(secondProgram.university.university_name,
            secondProgram.field.field_code + " " + secondProgram.field.field_name,
            secondProgram.program_name,
            secondProgram.degree,
            secondPieData,
            secondLineData);

        return [firstProgramComparisonData, secondProgramComparisonData];
    }

    #createTwoPieData(dto) {
        const pieRawDataList1 = dto.first_program_popular_competences;
        const pieRawDataList2 = dto.second_program_popular_competences;

        return [this.#createPieData(pieRawDataList1), this.#createPieData(pieRawDataList2)];
    }

    #createPieData(pieDataList) {
        return pieDataList.map(pieRawData => new PieData(0, pieRawData.competence, pieRawData.share));
    }

    #createTwoLineData(dto) {
        const lineRawData1 = dto.first_program_lesson_hours_a_week;
        const lineRawData2 = dto.second_program_lesson_hours_a_week;

        return [this.#createLineData(lineRawData1), this.#createLineData(lineRawData2)];
    }

    #createLineData(lineDataList) {
        return lineDataList.map((lineRawData, i) => new LineChartData(0, lineRawData, i + 1))
    }

    #createCourseComparisonData(dto) {
        const courseRawData = dto.similar_courses;

        return courseRawData.map(data => new CourseComparisonData(0,
            data.first_course_name,
            data.second_course_name,
            data.similarity))
    }
}