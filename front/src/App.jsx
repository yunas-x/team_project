import {observer} from "mobx-react-lite";
import {comparisonController} from "./index";
import {ProgramComparisonPage} from "./pages/ProgramComparison/ProgramComparisonPage";
import {ProgramsPage} from "./pages/ProgramsPage/ProgramsPage";
import NotificationContainer from "react-notifications/lib/NotificationContainer";
import 'react-notifications/lib/notifications.css';
import {CircularProgress} from "@mui/material";

export const App = observer(() => {
    return (
        <>
            <NotificationContainer />
            {comparisonController.isComparisonOpened
                ? comparisonController.isLoading
                    ? <div style={{display: "flex", width: "100%", height: "95vh", justifyContent: "center", alignItems: "center"}}>
                        <CircularProgress /> </div>
                    : <ProgramComparisonPage/>
                : <ProgramsPage/>}
        </>
    )
})