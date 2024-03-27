import {LineChart} from "@mui/x-charts";

const getXValues = (lineChartDataList) => {
    return lineChartDataList.map(data => data.yearNumber);
}

const getYValues = (lineChartDataList) => {
    return lineChartDataList.map(data => data.hours);
}

const CustomLineChart = ({lineChartDataList}) => {
    return (
        <LineChart xAxis={[{ label: 'Курс', data: getXValues(lineChartDataList), scaleType: 'point' }]}
                   yAxis={[{ label: 'Часы в неделю' }]}
                   series={[{ data: getYValues(lineChartDataList) }]}
                   margin={{ top: 40, bottom: 50, left: 60, right: 60 }}
                   grid={{ vertical: true, horizontal: true }}/>
    )
}

export {CustomLineChart}