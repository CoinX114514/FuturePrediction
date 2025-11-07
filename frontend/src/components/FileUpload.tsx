import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { uploadFile } from '../services/api'

/** OHLCV 数据项接口。 */
export interface OHLCVData {
  /** 日期。 */
  日期: string
  /** 开盘价。 */
  开盘: number
  /** 最高价。 */
  最高: number
  /** 最低价。 */
  最低: number
  /** 收盘价。 */
  收盘: number
  /** 成交量。 */
  成交量: number
}

/** 文件上传组件的属性接口。 */
interface FileUploadProps {
  /** 上传成功回调函数。 */
  onUploadSuccess: (fileId: string, data: OHLCVData[]) => void
  /** 上传错误回调函数。 */
  onUploadError: (error: string) => void
  /** 是否禁用上传功能。 */
  disabled?: boolean
}

/** 文件上传组件。
 * 
 * 提供拖拽上传和点击上传功能，支持 CSV 文件。
 * 
 * @param props - 组件属性。
 */
function FileUpload({
  onUploadSuccess,
  onUploadError,
  disabled = false,
}: FileUploadProps) {
  /** 上传状态。 */
  const [uploading, setUploading] = useState<boolean>(false)
  
  /** 上传的文件名。 */
  const [fileName, setFileName] = useState<string | null>(null)

  /**
   * 处理文件上传。
   * 
   * @param acceptedFiles - 接受的文件列表。
   */
  const handleFileUpload = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) {
        return
      }

      const file = acceptedFiles[0]

      // 验证文件类型
      if (!file.name.endsWith('.csv')) {
        onUploadError('请上传 CSV 格式的文件')
        return
      }

      setUploading(true)
      setFileName(file.name)

      try {
        const response = await uploadFile(file)
        
        if (response.file_id) {
          // 传递文件ID和解析后的数据
          const data = response.data || []
          onUploadSuccess(response.file_id, data)
        } else {
          onUploadError('上传失败：未收到文件 ID')
        }
      } catch (error: any) {
        // 处理错误信息，可能是字符串或对象
        let errorMessage = '文件上传失败'
        
        if (error.response?.data) {
          const errorData = error.response.data
          if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail
          } else if (typeof errorData.detail === 'object' && errorData.detail.error) {
            // 如果是对象格式的错误，提取错误信息
            errorMessage = errorData.detail.error
            if (errorData.detail.details && Array.isArray(errorData.detail.details)) {
              errorMessage += ': ' + errorData.detail.details.join(', ')
            }
          } else if (errorData.message) {
            errorMessage = errorData.message
          }
        } else if (error.message) {
          errorMessage = error.message
        }
        
        onUploadError(errorMessage)
      } finally {
        setUploading(false)
      }
    },
    [onUploadSuccess, onUploadError]
  )

  /** Dropzone 配置。 */
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: handleFileUpload,
    accept: {
      'text/csv': ['.csv'],
    },
    disabled: disabled || uploading,
    multiple: false,
  })

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-800">上传 OHLCV 数据</h2>
        <div
          {...getRootProps()}
          className={`
            inline-flex items-center gap-2 px-4 py-2 rounded-lg
            transition-colors duration-200
            ${
              isDragActive
                ? 'bg-blue-100 text-blue-700 border-2 border-blue-300'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }
            ${disabled || uploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
          `}
        >
          <input {...getInputProps()} />
          {uploading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span className="text-sm">上传中...</span>
            </>
          ) : (
            <>
              <svg
                className="h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
              <span className="text-sm font-medium">上传CSV文件</span>
            </>
          )}
        </div>
      </div>

      {/* 拖拽区域（仅在未上传时显示） */}
      {!fileName && !uploading && (
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-6 text-center cursor-pointer
            transition-colors duration-200
            ${
              isDragActive
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 bg-gray-50 hover:border-gray-400 hover:bg-gray-100'
            }
            ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <p className="text-blue-600">松开鼠标以上传文件</p>
          ) : (
            <div className="space-y-2">
              <svg
                className="mx-auto h-10 w-10 text-gray-400"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
              >
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <p className="text-sm text-gray-600">
                拖拽 CSV 文件到此处，或点击上方按钮选择文件
              </p>
              <p className="text-xs text-gray-500">
                必须包含：日期、开盘、最高、最低、收盘、成交量
              </p>
            </div>
          )}
        </div>
      )}

      {/* 上传成功提示 */}
      {fileName && !uploading && (
        <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm text-green-700 flex items-center gap-2">
            <span>✓</span>
            <span>文件已上传：{fileName}</span>
          </p>
        </div>
      )}
    </div>
  )
}

export default FileUpload

