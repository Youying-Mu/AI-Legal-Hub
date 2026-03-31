"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import RadarChart from "../../components/RadarChart";

export default function FullResultPage() {
  const router = useRouter();
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("analysisResult");
    if (stored) {
      setResult(JSON.parse(stored));
    } else {
      router.push("/");
    }
  }, [router]);

  const handleDownload = () => {
    if (!result) return;
    let content = `合同分析报告\n\n`;
    content += `总分：${result.total_score}\n`;
    content += `维度评分：${JSON.stringify(result.dimensions)}\n\n`;
    content += `风险点详情：\n${result.risk_points?.map((rp: any) => `- ${rp.clause}: ${rp.reason}`).join("\n")}\n\n`;
    content += `AI 总结：${result.summary}\n\n`;

    if (result.stage === "prevention") {
      content += `风险预防建议：\n${result.prevention_advice}\n\n`;
      content += `合同修改建议：\n${result.contract_modification?.join("\n")}\n`;
    } else if (result.stage === "remedy") {
      content += `维权路径：\n${result.remedy_path}\n\n`;
      if (result.compensation_model) {
        content += `赔偿计算模型：\n最低：${result.compensation_model.min} 元\n最高：${result.compensation_model.max} 元\n公式：${result.compensation_model.calculation}\n说明：${result.compensation_model.explanation}\n`;
      }
    }

    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "分析报告.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!result) return <div>加载中...</div>;

  return (
    <div className="max-w-4xl mx-auto py-10 px-4">
      <h1 className="text-2xl font-bold mb-6">完整风险分析报告</h1>

      {/* 雷达图 */}
      <div className="bg-white rounded-lg p-6 mb-6 shadow">
        <h2 className="text-lg font-semibold mb-2">风险雷达图</h2>
        <RadarChart data={result.dimensions || {}} />
      </div>

      {/* 风险点详情 */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">风险点详情</h2>
        {result.risk_points?.map((rp: any, idx: number) => (
          <div key={idx} className="border-l-4 border-red-400 p-3 mb-2 bg-gray-50">
            <p className="font-medium">{rp.clause}</p>
            <p className="text-gray-700">{rp.reason}</p>
            {rp.suggestion && <p className="text-blue-600 text-sm mt-1">建议：{rp.suggestion}</p>}
          </div>
        ))}
      </div>

      {/* 根据阶段展示不同内容 */}
      {result.stage === "prevention" && (
        <>
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">风险预防建议</h2>
            <div className="bg-gray-50 p-4 rounded whitespace-pre-line">
              {result.prevention_advice || "暂无"}
            </div>
          </div>
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">合同修改建议</h2>
            <div className="bg-gray-50 p-4 rounded">
              {result.contract_modification?.map((item: string, idx: number) => (
                <p key={idx} className="mb-2 whitespace-pre-line">{item}</p>
              ))}
            </div>
          </div>
        </>
      )}

      {result.stage === "remedy" && (
        <>
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">维权路径</h2>
            <div className="bg-gray-50 p-4 rounded whitespace-pre-line">
              {result.remedy_path || "暂无"}
            </div>
          </div>
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">赔偿计算模型</h2>
            {result.compensation_model ? (
              <div className="bg-gray-50 p-4 rounded">
                <p>最低赔偿：{result.compensation_model.min} 元</p>
                <p>最高赔偿：{result.compensation_model.max} 元</p>
                <p>计算公式：{result.compensation_model.calculation}</p>
                <p className="text-sm text-gray-600">{result.compensation_model.explanation}</p>
              </div>
            ) : (
              <p className="text-gray-700">暂无详细模型</p>
            )}
          </div>
        </>
      )}

      <button
        onClick={handleDownload}
        className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition"
      >
        下载报告
      </button>
    </div>
  );
}