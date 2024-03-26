import styles from './styles.module.css'
import {observer} from "mobx-react-lite";
import {ProgramCard} from "../ProgramCard/ProgramCard";
import {CardModel} from "../ProgramCard/cardModel";
import {Pagination} from "@mui/material";
import {useMemo, useRef, useState} from "react";
import {programsSelectionController} from "../../pages/ProgramsPage/ProgramsPage";

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
    const [selectedPageNumber, setSelectedPageNumber] = useState(1);

    const programCount = programSelectionService.programCount;
    const pageCount = Math.ceil(programCount / displayCardCount);

    if (selectedPageNumber > pageCount && programCount !== 0) {
        setSelectedPageNumber(pageCount)
    }

    return (
        <div className={styles.content_holder}>
            <div className={styles.top_block}>
                <span>Найдено программ: {programCount}</span>

                <div className={styles.search_block}>
                </div>
            </div>

            <div className={styles.pagination_top_block}>
                <Pagination count={pageCount}
                            page={selectedPageNumber}
                            onChange={(e, newPageNumber) => setSelectedPageNumber(newPageNumber)}/>
            </div>

            <div className={styles.cards_holder}>
                {programSelectionService.getPrograms(displayCardCount * (selectedPageNumber - 1), displayCardCount)
                    .map(program => <ProgramCard key={program.id}
                                                 cardModel={createCard(program)}
                                                 programsSelectionModel={program}
                                                 programsSelectionController={programsSelectionController} />)}
            </div>

            <div className={styles.pagination_bottom_block}>
                <Pagination count={pageCount}
                            page={selectedPageNumber}
                            onChange={(e, newPageNumber) => setSelectedPageNumber(newPageNumber)}/>
            </div>
        </div>
    )
})

export default ProgramSelectionList;