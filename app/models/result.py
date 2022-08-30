from sqlalchemy import Column, Integer, PickleType, String, ForeignKey, Float, BOOLEAN
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Result(Base):
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('case.id'))
    case = relationship("Case", back_populates='result')
    type = Column(String(256), nullable=False)
    htf = Column(String(256), nullable=False)
    material = Column(String(256), nullable=False)
    cost = Column(Float, nullable=False)
    run_time = Column(Float, nullable=False)

class Result_2(Base):
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('case.id'))
    case = relationship("Case", back_populates='result_2')
    tes_type = Column(String(256), nullable=False)
    tes_attr = Column(PickleType)
    tes_op_attr = Column(PickleType)
    
    chiller = Column(String(256), nullable=False)
    chiller_no_tes = Column(String(256), nullable=False)
    capex = Column(Float, nullable=False)
    capex_no_tes = Column(Float, nullable=False)
    lcos = Column(Float, nullable=False)
    lcos_no_tes = Column(Float, nullable=False) 
    load_split_profile = relationship("LoadSplitProfile", back_populates="result_2")
    electric_split_profile = relationship("ElectricSplitProfile", back_populates="result_2")
    cost_profile = relationship("CostProfile", back_populates="result_2")
    
    htf = Column(String(256), nullable=False)
    htf_attr = Column(PickleType)
    material = Column(String(256), nullable=False)
    material_attr = Column(PickleType)
    # cost = Column(Float, nullable=False)
    run_time = Column(Float, nullable=False)

class LoadSplitProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    parent_id =Column(Integer, ForeignKey('result_2.id'))
    result_2 = relationship("Result_2", back_populates='load_split_profile')
    time = Column(Float, nullable=False)
    value = Column(PickleType, nullable=False)
    with_tes = Column(BOOLEAN, nullable=False, default=False)

class ElectricSplitProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    parent_id =Column(Integer, ForeignKey('result_2.id'))
    result_2 = relationship("Result_2", back_populates='electric_split_profile')
    time = Column(Float, nullable=False)
    value = Column(PickleType, nullable=False)
    with_tes = Column(BOOLEAN, nullable=False, default=False)

class CostProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    parent_id =Column(Integer, ForeignKey('result_2.id'))
    result_2 = relationship("Result_2", back_populates='cost_profile')
    time = Column(Float, nullable=False)
    value = Column(PickleType, nullable=False)
    with_tes = Column(BOOLEAN, nullable=False, default=False)



