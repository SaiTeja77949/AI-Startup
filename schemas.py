"""
Pydantic models for request/response schemas and structured agent outputs.
"""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, HttpUrl

class ResearchSpec(BaseModel):
    """Structured output from Research Agent"""
    pain_points: List[str] = Field(
        ...,
        min_items=3,
        max_items=5,
        description="3-5 key pain points addressed by the product"
    )
    competitors: List[str] = Field(
        ...,
        min_items=3,
        max_items=3,
        description="Exactly 3 competitors with name and URL"
    )
    requirements: List[str] = Field(
        ...,
        min_items=3,
        max_items=5,
        description="3-5 actionable implementation requirements"
    )

class ReviewResult(BaseModel):
    """Structured output from Critic Agent"""
    status: Literal["PASS", "ISSUES"] = Field(
        ...,
        description="Review status - PASS for clean code, ISSUES for changes needed"
    )
    diffs: List[str] = Field(
        default=[],
        description="List of suggested code changes when status is ISSUES"
    )

class JobRequest(BaseModel):
    """API request for starting a new job"""
    idea: str = Field(..., min_length=10, description="Product idea description")
    publish_repo: bool = Field(
        default=False,
        description="Whether to publish the result to GitHub"
    )
    visibility: Literal["public", "private"] = Field(
        default="public",
        description="GitHub repository visibility if publishing"
    )

class JobPhase(BaseModel):
    """Current phase information for a job"""
    name: Literal["research", "engineer", "critic", "marketing", "compile", "publish"] = Field(
        ...,
        description="Current execution phase"
    )
    progress: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Progress percentage for current phase"
    )

class JobStatus(BaseModel):
    """API response for job status"""
    job_id: str = Field(..., description="Unique job identifier")
    status: Literal["queued", "running", "failed", "succeeded"] = Field(
        ...,
        description="Overall job status"
    )
    phase: Optional[JobPhase] = Field(
        None,
        description="Current execution phase and progress"
    )
    compile_status: Optional[bool] = Field(
        None,
        description="True if compilation passed, False if failed, None if not yet compiled"
    )
    errors: List[str] = Field(
        default=[],
        description="List of error messages if any occurred"
    )
    artifact_links: List[str] = Field(
        default=[],
        description="Links to generated artifacts"
    )
    repo_url: Optional[HttpUrl] = Field(
        None,
        description="GitHub repository URL if published"
    )
