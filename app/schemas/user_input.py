from pydantic import BaseModel

M_JOB = {
    "working_pressure": 1.5,
    "volume_limit": 3,
    "power_dis": 1.1,
    "energy_dis": 2.2,
    "power_pump": 0.2,
    "T_in_charge": -32,
    "T_out_charge": -10,
    "T_in_dis": -10,
    "T_out_dis": -30,
    "selected_toxicity_level": "None",
    "phase": "All",
    "accurancy_level": "low"
}

class JobInput(BaseModel):
    working_pressure: float
    volume_limit: float
    power_dis: float
    energy_dis: float
    power_pump: float
    T_in_charge: float
    T_out_charge: float
    T_in_dis: float
    T_out_dis: float
    selected_toxicity_level: str
    phase: str
    accurancy_level: str