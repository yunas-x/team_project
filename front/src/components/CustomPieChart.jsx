import {PieChart} from "@mui/x-charts";
import {mangoFusionPalette} from '@mui/x-charts/colorPalettes';

const convert = (pieChartDataList) => {
    return pieChartDataList.map(data => {return {value: data.ratioPercent, label: data.courseName}});
}

const CustomPieChart = ({pieChartDataList}) => {
    return (
        <PieChart margin={{ top: 0, bottom: 60, left: 0, right: 0 }}
                  series={[
                      {
                          data: convert(pieChartDataList),
                          paddingAngle: 0.5,
                          cornerRadius: 3
                      },
                  ]}
                  slotProps={{
                      legend: {
                          direction: 'row',
                          position: { vertical: 'bottom', horizontal: 'middle' },
                          padding: {top: 0, bottom: 0, left: 0, right: 0},
                          labelStyle: {
                              fontSize: 14,
                          },
                      },
                  }}
                  colors={mangoFusionPalette}
    />
    )
}

export {CustomPieChart}