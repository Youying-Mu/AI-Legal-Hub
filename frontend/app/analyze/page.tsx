"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function AnalyzePage() {
  const router = useRouter();
  useEffect(() => {
    // 模拟分析等待，实际结果已在 sessionStorage 中，直接跳转
    const timer = setTimeout(() => {
      router.push("/result/preview");
    }, 1000);
    return () => clearTimeout(timer);
  }, [router]);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mb-4"></div>
      <p className="text-gray-600">AI 正在分析您的合同，请稍候...</p>
    </div>
  );
}