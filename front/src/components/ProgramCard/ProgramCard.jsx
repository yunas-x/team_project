import styles from './styles.module.css'
import location from '../../imgs/location.svg'
import time from '../../imgs/time.svg'
import {yearPlural} from "../../helpers/consts";
import {getIsSelected} from "../../controllers/programsSelectionController";
import {observer} from "mobx-react-lite";

export const ProgramCard = observer(({cardModel, programsSelectionModel, programsSelectionController}) => {
    const isSelected = getIsSelected(programsSelectionModel, programsSelectionController.selectedList);
    const isBlocked = !isSelected && programsSelectionController.isReady;

    return (
        <div className={isBlocked ? `${styles.card} ${styles.blocked_card}` : isSelected ? `${styles.card} ${styles.selected_card}` : `${styles.card}`}
             onClick={() => isSelected
                 ? programsSelectionController.removeSelected(programsSelectionModel)
                 : programsSelectionController.setSelected(programsSelectionModel)}>
            <div className={styles.card_header}>
                <span className={cardModel.programName.length < 50 ? `${styles.card_title}` : `${styles.card_title} ${styles.small_card_title}`}>{cardModel.programName}</span>
            </div>

            <div className={styles.card_body}>
                <ul>
                    <li>{cardModel.universityName}</li>
                    <li>{cardModel.fieldOfStudyName}</li>
                    <li>{cardModel.degreeName}</li>
                </ul>
            </div>

            <div className={styles.card_footer}>
                <div className={styles.card_footer_item_holder}>
                    <img alt={"geo"} src={location} className={styles.location_img} />
                    <span>{cardModel.city}</span>
                </div>

                <div className={styles.card_footer_item_holder}>
                    <img alt={"year"} src={time} className={styles.time_img} />
                    <span>{cardModel.yearCount + " " + yearPlural[cardModel.yearCount] ?? "лет"}</span>
                </div>
            </div>
        </div>
    )
})