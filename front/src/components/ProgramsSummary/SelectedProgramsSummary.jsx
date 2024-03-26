import {observer} from "mobx-react-lite";
import styles from './styles.module.css'
import {programsSelectionController} from "../../pages/ProgramsPage/ProgramsPage";
import remove from '../../imgs/remove.svg'
import {useState} from "react";

const SelectedProgramsSummary = observer(() => {
    return (
        <div className={styles.content_holder}>
            <div className={styles.list_holder}>
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
                                     src={remove}
                                     className={styles.remove_img} />
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <div className={styles.compare_btn_holder}>
                <button className={styles.compare_btn}>
                    <span>Сравнить</span>
                </button>
            </div>
        </div>
    )
})

export {SelectedProgramsSummary};