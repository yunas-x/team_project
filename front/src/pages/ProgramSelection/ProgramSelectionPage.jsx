import ComboBox from "../../components/ComboBox/ComboBox";
import ProgramSelectionServicesProvider from "../../store/programSelectionServicesProvider";
import {useCallback, useMemo, useState} from "react";
import {observer} from "mobx-react-lite";
import styles from './styles.module.css'
import ProgramSelectionList from "../../components/ProgramSelectionList/ProgramSelectionList";

const servicesProvider = new ProgramSelectionServicesProvider();
servicesProvider.universityService.loadData();

const ProgramSelectionPage = observer(() => {
    const [isFieldOfStudyEditable, setIsFieldOfStudyEditable] = useState(false);
    const [selectedUniversityId, setSelectedUniversityId] = useState(undefined);
    const [selectedFieldOfStudyId, setSelectedFieldOfStudyId] = useState(undefined);

    const [universityService, fieldOfStudyService, programService] =
        useMemo(() => [servicesProvider.universityService, servicesProvider.fieldOfStudyService, servicesProvider.programService], [])

    const onUniversityChanged = useCallback((selectedId) => {
        setSelectedUniversityId(selectedId);

        setSelectedFieldOfStudyId(undefined);
        setIsFieldOfStudyEditable(false);

        if (selectedId) {
            fieldOfStudyService.loadDataById([selectedId]);
            setIsFieldOfStudyEditable(true);

            programService.loadDataById([selectedId]);
        } else {
            programService.store.setNewItems([])
        }
    }, [fieldOfStudyService, programService])

    const onFieldOfStudyChanged = (selectedId) => {
        setSelectedFieldOfStudyId(selectedId)

        if (selectedId) {
            programService.loadDataById([selectedUniversityId, selectedId]);
        } else if (selectedUniversityId) {
            programService.loadDataById([selectedUniversityId]);
        }
    }

    return (
        <div>
            <div className={styles.combo_box_holder}>
                <ComboBox values={universityService.store.items}
                          placeholderText={"Выберите ВУЗ"}
                          onChange={onUniversityChanged}
                          isEditable={true}
                          isLoading={universityService.isLoading}/>

                <ComboBox values={fieldOfStudyService.store.items}
                          placeholderText={"Выберите Направление"}
                          onChange={onFieldOfStudyChanged}
                          isEditable={isFieldOfStudyEditable}
                          isLoading={fieldOfStudyService.isLoading}
                          selectedValueId={selectedFieldOfStudyId}/>
            </div>

            <ProgramSelectionList isLoading={programService.isLoading}
                                  programItems={programService.store.items} />
        </div>
    )
})

export default ProgramSelectionPage;