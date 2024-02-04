import styles from './styles.module.css'
import {observer} from "mobx-react-lite";

const ProgramSelectionList = observer(({isLoading, programItems}) => {
    return (
        <div className={styles.list_holder}>

            {isLoading ? <div className={styles.placeholder_block}>Загрузка...</div> :
                programItems.length === 0
                ? <div className={styles.placeholder_block}>Выберите ВУЗ для выбора программ обучения</div>
                :
                <div className={styles.list_content_block}>
                    {programItems.map((program, i) => <span key={program.id}>{(i + 1)}. {program.name}</span>)}
                </div>
            }
        </div>
    )
})

export default ProgramSelectionList;