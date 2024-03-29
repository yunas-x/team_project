from models.Infographics import CourseSimilarity, PopularCompetence


similar_courses: list[CourseSimilarity] = [
    CourseSimilarity(first_course_name="История России",
                     second_course_name="История России",
                     similarity=98),
    CourseSimilarity(first_course_name="Правовая граммотность",
                     second_course_name="Правовая граммотность",
                     similarity=94),
    CourseSimilarity(first_course_name="Экономика",
                     second_course_name="Введение в экономику",
                     similarity=71),
    CourseSimilarity(first_course_name="Программирование на Python",
                     second_course_name="Анализ данных на Python",
                     similarity=65),
    CourseSimilarity(first_course_name="Проектный семинар",
                     second_course_name="Проектный семинар 2",
                     similarity=73)
]

first_program_popular_competences: list[PopularCompetence] = [
    PopularCompetence(competence="Аналитическое мышление", share=24),
    PopularCompetence(competence="Управление", share=13),
    PopularCompetence(competence="Проектная деятельность", share=32),
    PopularCompetence(competence="Цифровые навыки", share=31)
]

second_program_popular_competences: list[PopularCompetence] = [
    PopularCompetence(competence="Аналитическое мышление", share=21),
    PopularCompetence(competence="Цифровые навыки", share=33),
    PopularCompetence(competence="Экономика", share=13),
    PopularCompetence(competence="Проектный менеджмент",share=18),
    PopularCompetence(competence="Логическое мышление",share=15)
]

first_program_lesson_hours_a_week: list[int] = [30, 28, 25, 22, 16, 12]
second_program_lesson_hours_a_week: list[int] = [32, 29, 27, 23, 15, 11]