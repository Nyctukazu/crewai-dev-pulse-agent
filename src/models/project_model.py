import os
from dotenv import load_dotenv
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String, Boolean, DateTime, Integer, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class GroupRoles(str, PyEnum):
    QA = "QA"
    UI = "UI"
    UX = "UX"
    BACKEND = "BACKEND"
    FRONTEND = "FRONTEND"
    PROJECT_LEAD = "PROJECT_LEAD"
    RESEARCHER = "RESEARCHER"

class Status(str, PyEnum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"

class Base(DeclarativeBase):
    pass

class MemberInfo(Base):
    __tablename__ = "member_info"

    name: Mapped[str] = mapped_column(String, primar_key=True)
    role_string: Mapped[str] = mapped_column(String, nullable=False, default="DEVELOPER")
    status: Mapped[Status] = mapped_column(String, default=Status.ACTIVE)
    has_contributed_today: Mapped[bool] = mapped_column(Boolean, default=False)
    last_active_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    project_id: Mapped[int] = mapped_column(ForeignKey("Project_info.id"))
    project: Mapped["ProjectInfo"] = relationship(back_populates="members")

    @property
    def roles(self) -> List[GroupRoles]:
        return [GroupRoles(r.strp()) for r in self.role_string.split(",") if r.strip()]
    
class ProjectInfo(Base):
    __tablename__ = "project_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_name: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[str] = mapped_column(String, nullable=False)
    project_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    members: Mapped[List[MemberInfo]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )