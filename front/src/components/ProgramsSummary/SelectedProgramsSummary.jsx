import {observer} from "mobx-react-lite";
import styles from './styles.module.css'
import {programsSelectionController} from "../../pages/ProgramsPage/ProgramsPage";
import remove from '../../imgs/remove.svg'
import {comparisonController} from "../../index";

const onCompareClicked = () => {
    const [firstSelectedModel, secondSelectedModel] = programsSelectionController.selectedList;

    comparisonController.showComparison(firstSelectedModel, secondSelectedModel)
}

const SelectedProgramsSummary = observer(() => {
    return (
        <div className={styles.content_holder}>
            <div className={styles.list_holder}>
                <div className={styles.chosen_label}>
                    Выбрано:
                </div>
                {programsSelectionController.selectedList.map(programSelectionModel =>
                    <div key={programSelectionModel.id}
                         className={styles.info_holder}>
                        <div className={styles.university_holder}>
                            <span>{programSelectionModel.universityModel.displayName}</span>
                            <span className={styles.program_name}>{programSelectionModel.programModel.displayName}</span>
                        </div>

                        <div className={styles.remove_block}>
                            <div className={styles.remove_btn_holder} onClick={() => programsSelectionController.removeSelected(programSelectionModel)}>
                                <img alt={"del"}
                                     draggable={false}
                                     src={remove}
                                     className={styles.remove_img} />
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <div className={styles.bottom_content}>
                {programsSelectionController.selectedList.length === 0
                    ? <div className={styles.help_msg}>Выберите 2 программы</div>
                    : programsSelectionController.selectedList.length === 1 ?
                    <div className={styles.help_msg}>
                        Выберите ещё одну программу
                    </div>
                        : <div className={`${styles.help_msg} ${styles.help_msg_placeholder}`}>В</div>}

                <div className={styles.compare_btn_holder}>
                    <button className={programsSelectionController.isReady ? `${styles.compare_btn}` : `${styles.compare_btn} ${styles.btn_disabled}`}
                            disabled={!programsSelectionController.isReady}
                    onClick={() => onCompareClicked()}>
                        <span>Сравнить</span>
                    </button>
                </div>
            </div>
        </div>
    )
})

export {SelectedProgramsSummary};