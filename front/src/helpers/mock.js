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

export function getMasterId() {
    return degrees[1].id;
}

export const fieldOfStudies = [
    new FieldOfStudyModel("09.03.04", "Программная инженерия"),
    new FieldOfStudyModel("38.04.05", "Бизнес-информатика"),
    new FieldOfStudyModel("38.03.01", "Экономика"),
    new FieldOfStudyModel("40.03.01", "Юриспруденция"),
    new FieldOfStudyModel("42.03.05", "Медиакоммуникации"),
    new FieldOfStudyModel("41.03.04", "Политология"),
    new FieldOfStudyModel("03.03.02", "Физика"),
    new FieldOfStudyModel("10.05.01", "Компьютерная безопасность"),
]

export const programs = [
    new ProgramModel(1, "Программная инженерия"), // se
    new ProgramModel(2, "Экономика и статистика"), // econo
    new ProgramModel(3, "Цифровой юрист"), // yuri
    new ProgramModel(4, "Юриспруденция"), // yuri
    new ProgramModel(5, "Мировая экономика"), // econo
    new ProgramModel(6, "Кинопроизводство"), // media
    new ProgramModel(7, "Право"), // к юриспруденции
    new ProgramModel(8, "Политология и мировая политика"), // poli
    new ProgramModel(9, "Физика"),
    new ProgramModel(10, "Политология"), // poli
    new ProgramModel(11, "Бизнес-информатика: цифровое предприятие и управление информационными системами"),
    new ProgramModel(12, "Компьютерная безопасность")
]

const hseData = [
    new AllProgramData(programs[0].id, fieldOfStudies[0].id, degrees[0].id, 4),
    new AllProgramData(programs[10].id, fieldOfStudies[1].id, degrees[1].id, 2),
    new AllProgramData(programs[1].id, fieldOfStudies[2].id, degrees[0].id, 4),
    new AllProgramData(programs[2].id, fieldOfStudies[3].id, degrees[0].id, 4),
    new AllProgramData(programs[11].id, fieldOfStudies[7].id, degrees[2].id, 6),
    new AllProgramData(programs[3].id, fieldOfStudies[3].id, degrees[0].id, 4),
    new AllProgramData(programs[4].id, fieldOfStudies[2].id, degrees[0].id, 4),
    new AllProgramData(programs[5].id, fieldOfStudies[4].id, degrees[0].id, 4),
    new AllProgramData(programs[6].id, fieldOfStudies[3].id, degrees[0].id, 4),
    new AllProgramData(programs[7].id, fieldOfStudies[5].id, degrees[0].id, 4),
    new AllProgramData(programs[8].id, fieldOfStudies[6].id, degrees[0].id, 4),
    new AllProgramData(programs[9].id, fieldOfStudies[5].id, degrees[0].id, 5),
]

export const universities = [
    new UniversityModel(1, "НИУ ВШЭ", "Москва", hseData),
]

export const pieDataList1 = [
    new PieData(1, "Программирование", 60),
    new PieData(2, "Анализ данных", 10),
    new PieData(3, "Аналитика", 10),
    new PieData(4, "Математика", 20),
]

export const pieDataList2 = [
    new PieData(1, "Программирование", 30),
    new PieData(2, "Физика", 10),
    new PieData(3, "Анализ данных", 9),
    new PieData(4, "Математика", 31),
    new PieData(5, "Защита информации", 20),
]

export const lineChartDataList1 = [
    new LineChartData(1, 22, 1),
    new LineChartData(2, 24, 2),
    new LineChartData(3, 20, 3),
    new LineChartData(4, 19, 4),
]

export const lineChartDataList2 = [
    new LineChartData(1, 22, 1),
    new LineChartData(2, 21, 2),
    new LineChartData(3, 23, 3),
    new LineChartData(4, 19, 4),
    new LineChartData(5, 18, 5),
    new LineChartData(6, 17, 6),
]

export const courseComparisonDataList = [
    new CourseComparisonData(1, "Математические методы анализа данных", "Культура работы с данными", 89),
    new CourseComparisonData(2, "Алгебра", "Алгебра (углублённый курс)", 80),
    new CourseComparisonData(3, "Алгоритмы и алгоритмические языки", "Программирование алгоритмов защиты информации", 79),
    new CourseComparisonData(4, "Компиляторные технологии", "Язык ассемблер", 60),
    new CourseComparisonData(5, "Право", "Правовой режим персональных данных", 55),
]