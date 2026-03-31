"use client";
import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function Home() {
  const router = useRouter();
  const [description, setDescription] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      "image/*": [],
      "application/pdf": [],
      "text/plain": [],
    },
    maxFiles: 1,
  });

  const handleSubmit = async () => {
    if (!description && !file) {
      alert("请描述问题或上传文件");
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      if (description) formData.append("description", description);
      if (file) formData.append("file", file);  // 字段名必须为 'file'
      
      const res = await axios.post("http://127.0.0.1:8000/api/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      sessionStorage.setItem("analysisResult", JSON.stringify(res.data));
      router.push("/result/preview");
    } catch (error) {
      console.error(error);
      alert("分析失败，请稍后重试");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
      <div className="max-w-3xl w-full bg-white rounded-lg shadow-md p-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
          AI 法律助手
        </h1>
        <p className="text-center text-gray-600 mb-8">
          描述您的法律问题或上传合同文件，我们将为您提供专业分析和解决方案。
        </p>
        <div className="mb-6">
          <textarea
            className="w-full border border-gray-300 rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={5}
            placeholder="例如：我签了一份房屋租赁合同，房东突然要求提前解约，我该怎么办？"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <div
          {...getRootProps()}
          className="border-2 border-dashed border-gray-300 rounded-md p-6 text-center cursor-pointer hover:border-blue-500 transition mb-6"
        >
          <input {...getInputProps()} />
          <p className="text-gray-500">
            {file ? file.name : "拖拽或点击上传文件（图片/PDF/TXT）"}
          </p>
        </div>
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded-md font-medium hover:bg-blue-700 disabled:bg-blue-300 transition"
        >
          {loading ? "分析中..." : "开始分析"}
        </button>
      </div>
    </div>
  );
}