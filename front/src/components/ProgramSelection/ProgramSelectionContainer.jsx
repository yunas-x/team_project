import ComboBox from "../ComboBox/ComboBox";
import ProgramSelectionServicesProvider from "../../store/programSelectionServicesProvider";
import {useCallback, useEffect, useState} from "react";
import {observer} from "mobx-react-lite";
import styles from './styles.module.css'
import ProgramSelectionList from "../ProgramSelectionList/ProgramSelectionList";
import {ProgramSelectionService} from "../../store/services/programSelectionService";

const servicesProvider = new ProgramSelectionServicesProvider();
servicesProvider.loadServices()

const programSelectionService = new ProgramSelectionService(servicesProvider.universityService,
    servicesProvider.fieldOfStudyService, servicesProvider.programService, servicesProvider.degreeStore)

const ProgramSelectionContainer = observer(() => {
    const [selectedUniversityId, setSelectedUniversityId] = useState(undefined);
    const [selectedFieldsOfStudyId, setSelectedFieldsOfStudyId] = useState(undefined);
    const [selectedDegreesId, setSelectedDegreesId] = useState(undefined);

    const [universityService, fieldOfStudyService, programService, degreeStore] =
        [servicesProvider.universityService, servicesProvider.fieldOfStudyService, servicesProvider.programService, servicesProvider.degreeStore];

    const getFieldOfStudies = useCallback (() => {
        if (!selectedUniversityId) {
            return [];
        }

        const universityModel = universityService.getUniversityModel(selectedUniversityId[0]);

        return fieldOfStudyService.store.items.filter(fieldOfStudy => universityModel.allProgramDataList.map(data => data.fieldOfStudyId).includes(fieldOfStudy.id))
    }, [universityService, selectedUniversityId, fieldOfStudyService.store.items]);

    useEffect(() => {
        //programService.loadFilteredData(createFilterProgramObject(fieldOfStudyService.store, selectedFieldsOfStudyId, selectedDegreesId));
        //if (selectedUniversityId) {
            //programService.tempLoadByFilter(universityService.store.items.find(university => selectedUniversityId.includes(university.id)), selectedFieldsOfStudyId, selectedDegreesId)
        //} else {
            //programService.tempLoadByFilter(undefined, selectedFieldsOfStudyId, selectedDegreesId)
        //}

        programSelectionService.updateSelectedInfo(selectedUniversityId ? selectedUniversityId[0] : undefined,
            selectedFieldsOfStudyId ?? [], selectedDegreesId ?? [])

    }, [universityService.store.items, programService, fieldOfStudyService.store, selectedUniversityId, selectedFieldsOfStudyId, selectedDegreesId])

    function onUniversitySelectionChanged(selectedIdList) {
        let selectedUniversityId = selectedIdList && selectedIdList.length === 0 ? undefined : selectedIdList;

        setSelectedUniversityId(selectedUniversityId);

        if (!selectedUniversityId) {
            setSelectedFieldsOfStudyId(undefined);
            setSelectedDegreesId(undefined);
        }
    }

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
            <div className={styles.content_holder}>
                <div className={styles.filters_holder}>
                    <div className={styles.university_holder}>
                        <ComboBox values={universityService.store.items}
                                  placeholderText={"ВУЗ"}
                                  onChange={onUniversitySelectionChanged}
                                  selectedValuesId={selectedUniversityId}
                                  isEditable={true}
                                  isLoading={universityService.isLoading} />
                    </div>

                    <ComboBox values={getFieldOfStudies()}
                              placeholderText={"Направление обучения"}
                              onChange={onFieldsSelectionChanged}
                              isEditable={selectedUniversityId}
                              isLoading={fieldOfStudyService.isLoading}
                              selectedValuesId={selectedFieldsOfStudyId}
                              closeMenuOnSelect={false}
                              isMulti={true} />

                    <ComboBox values={degreeStore.items}
                              placeholderText={"Уровень образования"}
                              onChange={onDegreesSelectionChanged}
                              isEditable={selectedUniversityId}
                              isLoading={false}
                              selectedValuesId={selectedDegreesId}
                              closeMenuOnSelect={false}
                              isMulti={true} />
                </div>

                <div className={styles.filters_placeholder_block} />

                {!selectedUniversityId
                    ? <div className={styles.placeholder_block}>Выберите ВУЗ для просмотра программ обучения</div>
                        :
                <ProgramSelectionList isLoading={programService.isLoading}
                                      programSelectionService={programSelectionService} />
                }
            </div>
        </div>
    )
})

export default ProgramSelectionContainer;