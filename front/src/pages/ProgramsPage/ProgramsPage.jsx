import styles from './styles.module.css'
import ProgramSelectionContainer from "../../components/ProgramSelection/ProgramSelectionContainer";
import {ProgramsSelectionController} from "../../controllers/programsSelectionController";
import {SelectedProgramsSummary} from "../../components/ProgramsSummary/SelectedProgramsSummary";
import {useEffect, useState} from "react";

export const programsSelectionController = new ProgramsSelectionController();

export const ProgramsPage = () => {
    const [scrollY, setScrollY] = useState(0);

    useEffect(() => {
        const handleScroll = () => {
            setScrollY(window.scrollY);
        };
        handleScroll();

        window.addEventListener("scroll", handleScroll);
        return () => {
            window.removeEventListener("scroll", handleScroll);
        };
    }, []);

    return (
        <div className={styles.page}>
            <div className={styles.left_content}>
                <ProgramSelectionContainer />
            </div>

            <div className={styles.right_content} id={"right"}>
                <div className={styles.wrapper}>
                    <SelectedProgramsSummary />
                </div>
            </div>
        </div>
    )
}