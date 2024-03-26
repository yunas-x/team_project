import UniversityModel from "../models/universityModel";
import FieldOfStudyModel from "../models/fieldOfStudyModel";
import ProgramModel from "../models/programModel";
import {AllProgramData} from "../models/allProgramData";
import {DegreeModel} from "../models/degreeModel";
import {PieData} from "../models/comparison/pieData";
import {LineChartData} from "../models/comparison/lineChartData";
import {CourseComparisonData} from "../models/comparison/courseComparisonData";

export const degrees = [
    new DegreeModel(3, "Бакалавриат"),
    new DegreeModel(4, "Магистратура"),
    new DegreeModel(5, "Специалитет"),
]

export const fieldOfStudies = [
    new FieldOfStudyModel("01.02.03", "Программная инженерия"),
    new FieldOfStudyModel("01.02.04", "Бизнес-информатика"),
    new FieldOfStudyModel("03.01.02", "Экономика"),
    new FieldOfStudyModel("04.01.03", "Юриспруденция"),
    new FieldOfStudyModel("05.02.03", "Право"),
    new FieldOfStudyModel("42.03.05", "Медиакоммуникации"),
    new FieldOfStudyModel("41.03.04", "Политология"),
    new FieldOfStudyModel("03.03.02", "Физика"),
]

export const programs = [
    new ProgramModel(1, "Разработка интеллектуальных систем для бизнеса"), // se
    new ProgramModel(2, "Экономика и статистика"), // econo
    new ProgramModel(3, "Цифровой юрист"), // yuri
    new ProgramModel(4, "Юриспруденция"), // yuri
    new ProgramModel(5, "Мировая экономика"), // econo
    new ProgramModel(6, "Кинопроизводство"), // media
    new ProgramModel(7, "Право"), // к юриспруденции
    new ProgramModel(8, "Политология и мировая политика"), // poli
    new ProgramModel(9, "Физика"),
    new ProgramModel(10, "Политология"), // poli
]

const hseData = [
    new AllProgramData(programs[0].id, fieldOfStudies[0].id, degrees[0].id, 4),
    new AllProgramData(programs[0].id, fieldOfStudies[1].id, degrees[0].id, 5),
    new AllProgramData(programs[1].id, fieldOfStudies[2].id, degrees[0].id, 4),
    new AllProgramData(programs[1].id, fieldOfStudies[2].id, degrees[1].id, 2),
    new AllProgramData(programs[2].id, fieldOfStudies[3].id, degrees[0].id, 4),
    new AllProgramData(programs[3].id, fieldOfStudies[3].id, degrees[0].id, 5),
    new AllProgramData(programs[3].id, fieldOfStudies[3].id, degrees[1].id, 2),
    new AllProgramData(programs[4].id, fieldOfStudies[2].id, degrees[0].id, 4),
    new AllProgramData(programs[5].id, fieldOfStudies[5].id, degrees[0].id, 5),
    new AllProgramData(programs[6].id, fieldOfStudies[3].id, degrees[0].id, 6),
    new AllProgramData(programs[7].id, fieldOfStudies[6].id, degrees[0].id, 4),
    new AllProgramData(programs[8].id, fieldOfStudies[7].id, degrees[0].id, 4),
    new AllProgramData(programs[9].id, fieldOfStudies[6].id, degrees[0].id, 5),
]

export const universities = [
    new UniversityModel(1, "НИУ ВШЭ", "Москва", hseData),
]

export const pieDataList = [
    new PieData(1, "Лядова", 45),
    new PieData(2, "Дацун", 40),
    new PieData(3, "Управление проектами", 4),
    new PieData(4, "Ржомбанье", 6),
]

export const lineChartDataList = [
    new LineChartData(1, 30, 1),
    new LineChartData(2, 50, 2),
    new LineChartData(3, 43, 3),
    new LineChartData(4, 101, 4),
]

export const courseComparisonDataList = [
    new CourseComparisonData(1, "Лядова", "Дацун", 99),
    new CourseComparisonData(2, "Прога", "Олимпиадная прога", 30),
    new CourseComparisonData(3, "Рыбалка", "Охота", 40),
    new CourseComparisonData(4, "Прохождение СОПа", "Написание диплома", 2),
    new CourseComparisonData(5, "Разработка ПО", "Проектирование архитектуры", 5),
]