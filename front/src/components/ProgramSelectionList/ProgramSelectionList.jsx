import styles from './styles.module.css'
import {observer} from "mobx-react-lite";
import {ProgramCard} from "../ProgramCard/ProgramCard";
import {CardModel} from "../ProgramCard/cardModel";
import {Pagination} from "@mui/material";
import {useRef, useState} from "react";

let card = new CardModel(1, "Разработка интеллектуальных систем для бизнеса", "41.42.43 Направление неудачное очень", "ИТМО", "Бакалавриат", "Москва", 6)
let card2 = new CardModel(2, "Пивас", "01.02.03 Направление полёта", "НИУ ВШЭ", "Магистратура", "Пермь", 4)
let card3 = new CardModel(3, "Кальянчик", "51.22.23 Экономика", "ПНИПУ", "Специалитет", "Санкт-Петербург", 5)

const createCard = (programSelectionModel) =>  {
    return new CardModel(0, programSelectionModel.programModel.displayName,
        programSelectionModel.fieldOfStudyModel.displayName,
        programSelectionModel.universityModel.displayName,
        programSelectionModel.degreeModel.displayName,
        programSelectionModel.universityModel.city,
        programSelectionModel.yearCount)
}

const displayCardCount = 9;

const ProgramSelectionList = observer(({isLoading, programSelectionService}) => {
    const [selectedPageNumber, setSelectedPageNumber] = useState(1)
    const paginationRef = useRef(null);

    return (
        <div className={styles.content_holder}>
            <div className={styles.top_block}>
                <span>Total programs: {programSelectionService.programService.getTotalProgramsCount()}</span>

                <div className={styles.search_block}>
                </div>
            </div>

            <div className={styles.pagination_top_block} ref={paginationRef}>
                <Pagination count={Math.ceil(programSelectionService.programService.getTotalProgramsCount() / displayCardCount) }
                            page={selectedPageNumber}
                            onChange={(e, newPageNumber) => setSelectedPageNumber(newPageNumber)}/>
            </div>

            <div className={styles.cards_holder}>
                {programSelectionService.getPrograms(displayCardCount * (selectedPageNumber - 1), displayCardCount)
                    .map(program => <ProgramCard cardModel={createCard(program)} isSelected={false} onClick={null} />)}
                {/*<ProgramCard cardModel={card} isSelected={false} onClick={null} />*/}
                {/*<ProgramCard cardModel={card2} isSelected={false} onClick={null} />*/}
                {/*<ProgramCard cardModel={card3} isSelected={false} onClick={null} />*/}
            </div>

            <div className={styles.pagination_bottom_block} ref={paginationRef}>
                <Pagination count={Math.ceil(programSelectionService.programService.getTotalProgramsCount() / displayCardCount) }
                            page={selectedPageNumber}
                            onChange={(e, newPageNumber) => setSelectedPageNumber(newPageNumber)}/>
            </div>
        </div>
    )
})

export default ProgramSelectionList;