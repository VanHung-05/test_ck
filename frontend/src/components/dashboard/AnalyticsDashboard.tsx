'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/services/api'
import { CandidateAnalytics } from '@/types'

export default function AnalyticsDashboard() {
  const [analytics, setAnalytics] = useState<CandidateAnalytics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await apiClient.getMyAnalytics()
        setAnalytics(data)
        setError(null)
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Không thể tải thống kê')
      } finally {
        setLoading(false)
      }
    }

    fetchAnalytics()
  }, [])

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Thống kê</h2>
        <p className="text-gray-600">Đang tải...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Thống kê</h2>
        <p className="text-red-600">{error}</p>
      </div>
    )
  }

  if (!analytics) {
    return null
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Thống kê Portfolio</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Total Views */}
        <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-600 font-medium mb-1">Tổng lượt xem</p>
              <p className="text-4xl font-bold text-blue-900">{analytics.total_views}</p>
            </div>
            <div className="text-blue-500">
              <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
          </div>
          <p className="text-sm text-blue-600 mt-2">
            {analytics.recent_views} lượt trong 30 ngày qua
          </p>
        </div>

        {/* Total Invitations */}
        <div className="bg-green-50 p-6 rounded-lg border border-green-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600 font-medium mb-1">Tổng lời mời</p>
              <p className="text-4xl font-bold text-green-900">{analytics.total_invitations}</p>
            </div>
            <div className="text-green-500">
              <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <p className="text-sm text-green-600 mt-2">
            {analytics.recent_invitations} lời mời trong 30 ngày qua
          </p>
        </div>
      </div>

      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <p className="text-sm text-gray-600">
          <span className="font-semibold">Mẹo:</span> Bật chế độ công khai cho portfolio của bạn để nhà tuyển dụng có thể tìm thấy và xem hồ sơ của bạn.
        </p>
      </div>
    </div>
  )
}
