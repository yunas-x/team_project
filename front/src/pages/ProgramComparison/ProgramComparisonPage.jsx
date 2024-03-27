import styles from './styles.module.css'
import {comparisonController} from "../../index";
import {CustomPieChart} from "../../components/CustomPieChart";
import {CustomLineChart} from "../../components/CustomLineChart";

const onBackClicked = () => {
    comparisonController.closeComparison();
}

const comparer = (d1, d2) => {
    let a = d1.similarityPercent;
    let b = d2.similarityPercent;

    if (a > b) {
        return -1;
    }

    if (a < b) {
        return 1;
    }

    return 0;
}

const ProgramComparisonPage = () => {
    const comparisonData = comparisonController.comparisonData;
    const firstComparisonData = comparisonData.firstProgramComparisonData;
    const secondComparisonData = comparisonData.secondProgramComparisonData;

    return (
        <div className={styles.root}>
            <div className={styles.content_holder}>
                <div className={styles.back_btn_holder}>
                    <button className={styles.back_btn} onClick={() => onBackClicked()}><span>Назад</span></button>
                </div>
                <div className={styles.top_label}>Сравнение образовательных программ</div>

                <div className={styles.program_names}>
                    <div className={styles.program_name}>
                        <span>{firstComparisonData.programName}</span>

                        <div className={styles.program_info}>
                            <span>{firstComparisonData.universityName}</span>
                            <span>{firstComparisonData.fieldOfStudyName}</span>
                            <span>{firstComparisonData.degreeName}</span>
                        </div>
                    </div>

                    <div className={styles.vr_divider} />

                    <div className={styles.program_name}>
                        <span>{secondComparisonData.programName}</span>

                        <div className={styles.program_info}>
                            <span>{secondComparisonData.universityName}</span>
                            <span>{secondComparisonData.fieldOfStudyName}</span>
                            <span>{secondComparisonData.degreeName}</span>
                        </div>
                    </div>
                </div>

                <div className={styles.table_holder}>
                    <div className={styles.table_label}>Похожие курсы</div>

                    <div className={styles.table_labels}>
                        <div className={styles.table_left_label}>Название</div>
                        <div className={styles.table_middle_label}>Схожесть</div>
                        <div className={styles.table_right_label}>Название</div>
                    </div>

                    {comparisonData.courseComparisonDataList.sort(comparer).map(comparisonData =>
                        <div className={styles.table_data_labels}
                             key={comparisonData.id}>
                            <div className={styles.table_left_data}>{comparisonData.firstCourseName}</div>
                            <div className={styles.table_middle_data}>{comparisonData.similarityPercent}%</div>
                            <div className={styles.table_right_data}>{comparisonData.secondCourseName}</div>
                        </div>)}

                    <div className={styles.hr_divider} />

                    <div className={styles.pie_charts_holder}>
                        <div className={styles.pie_chart_holder}>
                            <CustomPieChart pieChartDataList={firstComparisonData.pieDataList}/>
                        </div>

                        <div className={styles.pie_chart_holder}>
                            <CustomPieChart pieChartDataList={secondComparisonData.pieDataList}/>
                        </div>
                    </div>

                    <div className={styles.line_charts_holder}>
                        <div className={styles.line_chart_holder}>
                            <CustomLineChart lineChartDataList={firstComparisonData.lineChartDataList} />
                        </div>

                        <div className={styles.line_chart_holder}>
                            <CustomLineChart lineChartDataList={secondComparisonData.lineChartDataList} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export {ProgramComparisonPage}