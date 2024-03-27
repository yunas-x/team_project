import {observer} from "mobx-react-lite";
import {comparisonController} from "./index";
import {ProgramComparisonPage} from "./pages/ProgramComparison/ProgramComparisonPage";
import {ProgramsPage} from "./pages/ProgramsPage/ProgramsPage";
import NotificationContainer from "react-notifications/lib/NotificationContainer";
import 'react-notifications/lib/notifications.css';

export const App = observer(() => {
    return (
        <>
            <NotificationContainer />
            {comparisonController.isComparisonOpened ? <ProgramComparisonPage/> : <ProgramsPage/>}
        </>
    )
})