import {observer} from "mobx-react-lite";
import {comparisonController} from "./index";
import {ProgramComparisonPage} from "./pages/ProgramComparison/ProgramComparisonPage";
import {ProgramsPage} from "./pages/ProgramsPage/ProgramsPage";

export const App = observer(() => {
    return (
        <>
            {comparisonController.isComparisonOpened ? <ProgramComparisonPage/> : <ProgramsPage/>}
        </>
    )
})