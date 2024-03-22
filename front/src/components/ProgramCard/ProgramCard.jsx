import styles from './styles.module.css'
import location from '../../imgs/location.svg'
import time from '../../imgs/time.svg'
import {yearPlural} from "../../helpers/consts";

export const ProgramCard = ({cardModel, isSelected, onClick}) => {
    return (
        <div className={styles.card}>
            <div className={styles.card_header}>
                <span className={styles.card_title}>{cardModel.programName}</span>
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
}