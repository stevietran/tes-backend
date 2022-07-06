import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Case(Base):
    id = Column(Integer, primary_key=True, index=True)
    submitter_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    app_type = Column(String(256), nullable=True)
    status = Column(String(256), default="SUBMITTED", nullable=False)
    submit_time = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, onupdate=datetime.datetime.utcnow)
    submitter = relationship("User", back_populates="cases")
    caseparams = relationship("CaseParams", back_populates="case", uselist=False)
    caseparams_2 = relationship("CaseParams_2", back_populates="case", uselist=False)
    result = relationship("Result", back_populates="case", uselist=False)
    result_2 = relationship("Result_2", back_populates="case", uselist=False)

class CaseParams_2(Base):
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('case.id'))
    app = Column(String(256), nullable=False)
    accuracy_level = Column(String(256), nullable=False)
    country_selection = Column(String(256), nullable=False)
    load_selection = Column(String(256), nullable=True)
    load_value = Column(Float, nullable=True)
    safety_factor = Column(Float, nullable=False)
    has_profiles = Column(Boolean, nullable=False)
    case = relationship("Case", back_populates='caseparams_2')
    loadprofile = relationship("LoadProfile", back_populates="caseparams_2", uselist=False)

class LoadProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    parent_id =Column(Integer, ForeignKey('caseparams_2.id'))
    caseparams_2 = relationship("CaseParams_2", back_populates='loadprofile')
    time = Column(Float, nullable=False)
    value = Column(Float, nullable=False)

class CaseParams(Base):
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('case.id'))
    case = relationship("Case", back_populates='caseparams')
    app = Column(String(256), nullable=False)
    accuracy_level = Column(String(256), nullable=False)
    pressure = Column(Float, nullable=False)
    upper_temperature = Column(Float, nullable=False)
    lower_temperature = Column(Float, nullable=False)
    flowprofile = relationship("FlowProfile", back_populates="caseparams", uselist=False)

class FlowProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    parent_id =Column(Integer, ForeignKey('caseparams.id'))
    caseparams = relationship("CaseParams", back_populates='flowprofile')
    time = Column(Float, nullable=False)
    value = Column(Float, nullable=False)

  





