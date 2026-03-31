"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function PreviewResultPage() {
  const router = useRouter();
  const [result, setResult] = useState<any>(null);
  const [isPaying, setIsPaying] = useState(false);

  useEffect(() => {
    const stored = sessionStorage.getItem("analysisResult");
    if (stored) {
      setResult(JSON.parse(stored));
    } else {
      router.push("/");
    }
  }, [router]);

  const handleUnlock = () => {
    setIsPaying(true);
    setTimeout(() => {
      setIsPaying(false);
      router.push("/result/full");
    }, 1500);
  };

  if (!result) return <div>加载中...</div>;

  return (
    <div className="max-w-4xl mx-auto py-10 px-4">
      {/* 支付弹窗 */}
      {isPaying && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg text-center">
            <p className="text-lg font-semibold mb-4">正在处理支付...</p>
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="text-sm text-gray-500 mt-4">（演示模式，不实际扣费）</p>
          </div>
        </div>
      )}

      <h1 className="text-2xl font-bold mb-6">风险分析报告（免费预览）</h1>

      {/* 雷达图占位 */}
      <div className="bg-gray-100 rounded-lg p-6 mb-6">
        <h2 className="text-lg font-semibold mb-2">风险雷达图（预览）</h2>
        <div className="h-48 bg-gray-200 rounded flex items-center justify-center">
          （付费解锁后查看完整评分）
        </div>
      </div>

      {/* 根据阶段展示不同内容 */}
      {result.stage === "prevention" && (
        <>
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">风险点摘要</h2>
            {result.risk_points?.slice(0, 2).map((rp: any, idx: number) => (
              <div key={idx} className="border-l-4 border-yellow-400 p-3 mb-2 bg-gray-50">
                <p className="font-medium">{rp.clause}</p>
                <p className="text-gray-600 line-through decoration-2 decoration-gray-400">
                  {rp.reason?.substring(0, 50)}...（付费解锁后查看详情）
                </p>
              </div>
            ))}
            {(!result.risk_points || result.risk_points.length === 0) && (
              <p className="text-gray-500">暂无风险点，付费解锁后可查看完整分析</p>
            )}
          </div>
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">AI 总结（预览）</h2>
            <p className="text-gray-700">{result.summary?.substring(0, 150)}...</p>
            <p className="text-blue-500 text-sm mt-1">（付费解锁后查看完整合同修改建议）</p>
          </div>
        </>
      )}

      {result.stage === "remedy" && (
        <>
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">风险类型</h2>
            <p className="text-red-600 font-medium">{result.risk_points?.[0]?.clause || "违约/侵权风险"}</p>
          </div>
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">维权路径概要</h2>
            <p className="text-gray-700">建议通过行政投诉或司法途径解决。解锁后可查看具体维权部门、联系电话及在线入口。</p>
          </div>
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">赔偿金额提示</h2>
            <p className="text-gray-700">详细计算模型（含公式及精确区间）需解锁后查看。</p>
          </div>
        </>
      )}

      {/* 如果 stage 缺失，显示通用预览 */}
      {!["prevention", "remedy"].includes(result.stage) && (
        <div className="mb-6">
          <h2 className="text-lg font-semibold mb-2">预览</h2>
          <p className="text-gray-700">请解锁查看完整报告</p>
        </div>
      )}

      <button
        onClick={handleUnlock}
        className="w-full bg-blue-600 text-white py-3 rounded-md font-medium hover:bg-blue-700 transition"
      >
        解锁完整报告（¥9.9）
      </button>
    </div>
  );
}