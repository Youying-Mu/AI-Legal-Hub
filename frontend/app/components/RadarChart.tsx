"use client";
import ReactECharts from "echarts-for-react";
import { useMemo } from "react";

interface RadarChartProps {
  data: Record<string, number>; // { "权利义务": 70, "违约责任": 45, ... }
}

export default function RadarChart({ data }: RadarChartProps) {
  const indicators = useMemo(() => Object.keys(data).map((name) => ({ name, max: 100 })), [data]);
  const seriesData = [Object.values(data)];

  const option = {
    radar: {
      indicator: indicators,
      shape: "circle",
      name: { textStyle: { fontSize: 12, color: "#333" } },
      center: ["50%", "50%"],
      radius: "65%",
    },
    series: [
      {
        name: "风险评分",
        type: "radar",
        data: seriesData,
        areaStyle: { color: "rgba(255, 99, 71, 0.3)" },
        lineStyle: { color: "#ff6347", width: 2 },
        symbol: "none",
      },
    ],
  };

  return <ReactECharts option={option} style={{ height: "300px", width: "100%" }} />;
}
