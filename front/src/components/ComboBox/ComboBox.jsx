import Select from "react-select";
import {memo, useEffect, useRef} from "react";

function convertValuesToOptions(values) {
    return values.map(value => {return {value: value.id, label: value.name}})
}

const getNoResultMessage = () => "Нет результатов";
const getLoadingMessage = () => "Загрузка...";

export default memo(function ComboBox({values, placeholderText, isEditable, onChange, isLoading, selectedValueId = undefined}) {
    const selectInputRef = useRef();

    useEffect(() => {
        if (!selectedValueId) {
            selectInputRef.current?.clearValue();
        }

    }, [selectedValueId])

    const findSelectedValue = (selectedId) => {
        if (selectedId) {
            let selectedValue = values.find(value => value.id === selectedId);

            return {value: selectedValue.id, label: selectedValue.name};
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
                onChange={(newValue) => onChange(newValue?.value)}
                isClearable={true}
                value={findSelectedValue(selectedValueId)}
                ref={selectInputRef} />
    )
})