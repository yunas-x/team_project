import styles from './styles.module.css'
import {observer} from "mobx-react-lite";
import {ProgramCard} from "../ProgramCard/ProgramCard";
import {CardModel} from "../ProgramCard/cardModel";

let card = new CardModel(1, "Разработка интеллектуальных систем для бизнеса", "41.42.43 Направление неудачное очень", "ИТМО", "Бакалавриат", "Москва", 6)
let card2 = new CardModel(2, "Пивас", "01.02.03 Направление полёта", "НИУ ВШЭ", "Магистратура", "Пермь", 4)
let card3 = new CardModel(3, "Кальянчик", "51.22.23 Экономика", "ПНИПУ", "Специалитет", "Санкт-Петербург", 5)

const ProgramSelectionList = observer(({isLoading, programs}) => {
    return (
        <div className={styles.list_holder}>

            {/*{isLoading ? <div className={styles.placeholder_block}>Загрузка...</div> :*/}
            {/*    programs.length === 0*/}
            {/*    ? <div className={styles.placeholder_block}>Выберите ВУЗ для выбора программ обучения</div>*/}
            {/*    :*/}
            {/*    <div className={styles.list_content_block}>*/}
            {/*        {programs.map((program, i) => <span key={program.id}>{(i + 1)}. {program.name}</span>)}*/}
            {/*    </div>*/}
            {/*}*/}
            <ProgramCard cardModel={card} isSelected={false} onClick={null} />
            <ProgramCard cardModel={card2} isSelected={false} onClick={null} />
            <ProgramCard cardModel={card3} isSelected={false} onClick={null} />
        </div>
    )
})

export default ProgramSelectionList;