import Select from "react-select";
import {memo, useEffect, useRef} from "react";

function convertValuesToOptions(values) {
    return values.map(value => {return {value: value.id, label: value.displayName}})
}

const getNoResultMessage = () => "Нет результатов";
const getLoadingMessage = () => "Загрузка...";

const customStyles = {
    control: base => ({
        ...base,
        minHeight: 40,
        minWidth: 300,
        maxWidth: 300,
    })
};

export default memo(function ComboBox({values, placeholderText, isEditable, isLoading, onChange = () => {},
                                          selectedValuesId = undefined,
                                          closeMenuOnSelect = true, isMulti = false}) {
    const selectInputRef = useRef();

    useEffect(() => {
        if (!selectedValuesId || selectedValuesId.length === 0) {
            selectInputRef.current?.clearValue();
        }
    }, [selectedValuesId])

    const findSelectedValues = (selectedIdList) => {
        if (selectedIdList && selectedIdList.length !== 0) {
            let selectedValues = values.filter(value => selectedIdList.includes(value.id));

            return selectedValues.map(selectedValue => {return {value: selectedValue.id, label: selectedValue.displayName}});
        } else {
            return undefined;
        }
    }

    return (
        <Select options={convertValuesToOptions(values)}
                noOptionsMessage={getNoResultMessage}
                placeholder={placeholderText}
                isDisabled={!isEditable}
                isLoading={isLoading}
                loadingMessage={getLoadingMessage}
                onChange={(newValue) => onChange(newValue?.map(v => v.value))}
                isClearable={true}
                value={findSelectedValues(selectedValuesId)}
                ref={selectInputRef}
                closeMenuOnSelect={closeMenuOnSelect}
                isMulti={isMulti}
                styles={customStyles}/>
    )
})