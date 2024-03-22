import styles from './styles.module.css'
import ProgramSelectionContainer from "../../components/ProgramSelection/ProgramSelectionContainer";

export const ProgramsPage = () => {
    return (
        <div className={styles.page}>
            <div className={styles.left_content}>
                <ProgramSelectionContainer />
            </div>

            <div className={styles.right_content}>

            </div>
        </div>
    )
}