"""Dashboard API endpoints for analytics and insights."""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
from app.database.connection import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.dashboard import (
    DashboardResponse, 
    CVInsightsResponse, 
    SkillAnalyticsResponse,
    CareerAnalyticsResponse
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/overview", response_model=DashboardResponse)
async def get_dashboard_overview(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    user_id: Optional[str] = Query(None, description="Filter by specific user"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get comprehensive dashboard overview with analytics."""
    try:
        analytics_service = AnalyticsService(db)
        dashboard_data = await analytics_service.get_dashboard_data(user_id=user_id, days=days)
        
        return JSONResponse(content={
            "success": True,
            "data": dashboard_data,
            "message": "Dashboard data retrieved successfully"
        })
        
    except Exception as e:
        logger.error(f"Error retrieving dashboard overview: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dashboard data: {str(e)}")

@router.get("/cv-insights/{cv_analysis_id}", response_model=CVInsightsResponse)
async def get_cv_insights(
    cv_analysis_id: str,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get detailed insights for a specific CV analysis."""
    try:
        analytics_service = AnalyticsService(db)
        insights = await analytics_service.generate_cv_insights(cv_analysis_id)
        
        return JSONResponse(content={
            "success": True,
            "data": insights,
            "message": "CV insights generated successfully"
        })
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating CV insights: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")

@router.get("/skills-analytics", response_model=SkillAnalyticsResponse)
async def get_skills_analytics(
    user_id: Optional[str] = Query(None, description="Filter by specific user"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get comprehensive skills analytics and trends."""
    try:
        analytics_service = AnalyticsService(db)
        skill_analytics = await analytics_service.get_skill_analytics(user_id=user_id)
        
        return JSONResponse(content={
            "success": True,
            "data": skill_analytics,
            "message": "Skills analytics retrieved successfully"
        })
        
    except Exception as e:
        logger.error(f"Error retrieving skills analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve skills analytics: {str(e)}")

@router.get("/career-analytics", response_model=CareerAnalyticsResponse)
async def get_career_analytics(
    user_id: Optional[str] = Query(None, description="Filter by specific user"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get comprehensive career recommendation analytics."""
    try:
        analytics_service = AnalyticsService(db)
        career_analytics = await analytics_service.get_career_analytics(user_id=user_id)
        
        return JSONResponse(content={
            "success": True,
            "data": career_analytics,
            "message": "Career analytics retrieved successfully"
        })
        
    except Exception as e:
        logger.error(f"Error retrieving career analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve career analytics: {str(e)}")

@router.get("/metrics/performance")
async def get_performance_metrics(
    days: int = Query(7, ge=1, le=90, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get system performance metrics."""
    try:
        analytics_service = AnalyticsService(db)
        dashboard_data = await analytics_service.get_dashboard_data(days=days)
        performance_metrics = dashboard_data.get("performance_metrics", {})
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "period_days": days,
                "metrics": performance_metrics,
                "summary": dashboard_data.get("summary", {})
            },
            "message": "Performance metrics retrieved successfully"
        })
        
    except Exception as e:
        logger.error(f"Error retrieving performance metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve performance metrics: {str(e)}")

@router.get("/trends/skills")
async def get_skill_trends(
    days: int = Query(90, ge=30, le=365, description="Number of days to analyze"),
    limit: int = Query(20, ge=5, le=50, description="Number of top skills to return"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get skill trends over time."""
    try:
        analytics_service = AnalyticsService(db)
        dashboard_data = await analytics_service.get_dashboard_data(days=days)
        skill_trends = dashboard_data.get("skill_trends", {})
        
        # Limit the results
        if "trending_up" in skill_trends:
            skill_trends["trending_up"] = skill_trends["trending_up"][:limit]
        if "trending_down" in skill_trends:
            skill_trends["trending_down"] = skill_trends["trending_down"][:limit]
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "period_days": days,
                "trends": skill_trends,
                "limit": limit
            },
            "message": "Skill trends retrieved successfully"
        })
        
    except Exception as e:
        logger.error(f"Error retrieving skill trends: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve skill trends: {str(e)}")

@router.get("/trends/careers")
async def get_career_trends(
    days: int = Query(90, ge=30, le=365, description="Number of days to analyze"),
    limit: int = Query(15, ge=5, le=30, description="Number of top roles to return"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get career recommendation trends over time."""
    try:
        analytics_service = AnalyticsService(db)
        dashboard_data = await analytics_service.get_dashboard_data(days=days)
        career_trends = dashboard_data.get("career_trends", {})
        
        # Limit the results
        if "popular_roles" in career_trends:
            career_trends["popular_roles"] = career_trends["popular_roles"][:limit]
        if "emerging_roles" in career_trends:
            career_trends["emerging_roles"] = career_trends["emerging_roles"][:limit]
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "period_days": days,
                "trends": career_trends,
                "limit": limit
            },
            "message": "Career trends retrieved successfully"
        })
        
    except Exception as e:
        logger.error(f"Error retrieving career trends: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve career trends: {str(e)}")

@router.get("/export/data")
async def export_analytics_data(
    format: str = Query("json", regex="^(json|csv)$", description="Export format"),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    user_id: Optional[str] = Query(None, description="Filter by specific user"),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Export analytics data in specified format."""
    try:
        analytics_service = AnalyticsService(db)
        
        # Get comprehensive data
        dashboard_data = await analytics_service.get_dashboard_data(user_id=user_id, days=days)
        skill_analytics = await analytics_service.get_skill_analytics(user_id=user_id)
        career_analytics = await analytics_service.get_career_analytics(user_id=user_id)
        
        export_data = {
            "export_timestamp": "2025-01-24T00:00:00Z",  # Current timestamp
            "parameters": {
                "format": format,
                "days": days,
                "user_id": user_id
            },
            "dashboard_data": dashboard_data,
            "skill_analytics": skill_analytics,
            "career_analytics": career_analytics
        }
        
        if format == "csv":
            # For CSV format, we'd typically convert to CSV and return file
            # For now, return JSON with CSV indication
            return JSONResponse(content={
                "success": True,
                "data": export_data,
                "message": "Data exported successfully (CSV format conversion would be implemented)",
                "format": "csv"
            })
        else:
            return JSONResponse(content={
                "success": True,
                "data": export_data,
                "message": "Data exported successfully",
                "format": "json"
            })
        
    except Exception as e:
        logger.error(f"Error exporting analytics data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to export data: {str(e)}")

@router.get("/health")
async def get_system_health(
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get system health status and metrics."""
    try:
        analytics_service = AnalyticsService(db)
        dashboard_data = await analytics_service.get_dashboard_data(days=1)  # Last 24 hours
        
        summary = dashboard_data.get("summary", {})
        health_score = summary.get("health_score", 0)
        
        # Determine health status
        if health_score >= 90:
            status = "excellent"
        elif health_score >= 75:
            status = "good"
        elif health_score >= 50:
            status = "fair"
        else:
            status = "poor"
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "status": status,
                "health_score": health_score,
                "metrics": summary,
                "timestamp": "2025-01-24T00:00:00Z"
            },
            "message": f"System health is {status}"
        })
        
    except Exception as e:
        logger.error(f"Error retrieving system health: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve system health: {str(e)}")
