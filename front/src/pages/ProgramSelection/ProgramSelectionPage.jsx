import ComboBox from "../../components/ComboBox/ComboBox";
import ProgramSelectionServicesProvider from "../../store/programSelectionServicesProvider";
import {useEffect, useState} from "react";
import {observer} from "mobx-react-lite";
import styles from './styles.module.css'
import ProgramSelectionList from "../../components/ProgramSelectionList/ProgramSelectionList";
import {FilterProgram} from "../../store/dto/filterProgram";

const servicesProvider = new ProgramSelectionServicesProvider();
servicesProvider.loadServices()

const ProgramSelectionPage = observer(() => {
    const [selectedFieldsOfStudyId, setSelectedFieldsOfStudyId] = useState(undefined);
    const [selectedDegreesId, setSelectedDegreesId] = useState(undefined);

    const [universityService, fieldOfStudyService, programService, degreeStore] =
        [servicesProvider.universityService, servicesProvider.fieldOfStudyService, servicesProvider.programService, servicesProvider.degreeLevelStore];

    useEffect(() => {
        programService.loadFilteredData(createFilterProgramObject(fieldOfStudyService.store, selectedFieldsOfStudyId, selectedDegreesId));
    }, [programService, fieldOfStudyService.store, selectedFieldsOfStudyId, selectedDegreesId])

    function onFieldsSelectionChanged(selectedIdList) {
        let selectedFieldsOfStudyId = selectedIdList && selectedIdList.length === 0 ? undefined : selectedIdList;

        setSelectedFieldsOfStudyId(selectedFieldsOfStudyId);
    }

    function onDegreesSelectionChanged(selectedIdList) {
        let selectedDegreesId = selectedIdList && selectedIdList.length === 0 ? undefined : selectedIdList;

        setSelectedDegreesId(selectedDegreesId);
    }

    return (
        <div>
            <div className={styles.combo_box_holder}>
                <ComboBox values={universityService.store.items}
                          placeholderText={"Выберите ВУЗ"}
                          isEditable={true}
                          isLoading={universityService.isLoading} />

                <ComboBox values={fieldOfStudyService.store.items}
                          placeholderText={"Выберите Направление"}
                          onChange={onFieldsSelectionChanged}
                          isEditable={true}
                          isLoading={fieldOfStudyService.isLoading}
                          selectedValuesId={selectedFieldsOfStudyId}
                          closeMenuOnSelect={false}
                          isMulti={true} />

                <ComboBox values={degreeStore.items}
                          placeholderText={"Выберите Уровень образования"}
                          onChange={onDegreesSelectionChanged}
                          isEditable={true}
                          isLoading={false}
                          selectedValuesId={selectedDegreesId}
                          closeMenuOnSelect={false}
                          isMulti={true} />

                <ComboBox values={programService.store.items}
                          placeholderText={"Выберите Образовательную программу"}
                          isEditable={true}
                          isLoading={programService.isLoading}/>
            </div>

            {/*<ProgramSelectionList isLoading={programService.isLoading}*/}
            {/*                      programItems={programService.store.items} />*/}
        </div>
    )
})

function createFilterProgramObject(fieldsStore, selectedFieldsId, selectedDegreesId) {
    const fieldGroupsId = selectedFieldsId?.map(fieldId => fieldsStore.items.find(item => item.id === fieldId).fieldGroupCode);

    return new FilterProgram(selectedFieldsId, fieldGroupsId, selectedDegreesId);
}

export default ProgramSelectionPage;