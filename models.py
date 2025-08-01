
from typing import Optional, Any
from pydantic import BaseModel, Field, root_validator

class Permit(BaseModel):
    number: str = Field(..., description="Permit number is required")
    type_: Optional[Any] = Field(None, alias="type")
    type_desc: Optional[Any] = None
    class_mapped: Optional[Any] = None
    class_: Optional[Any] = Field(None, alias="class")
    work_class: Optional[Any] = None
    condominium: Optional[Any] = None
    master_number: Optional[Any] = None
    link: Optional[Any] = None
    certificate_of_occupancy: Optional[Any] = None
    issue_method: Optional[Any] = None

class Project(BaseModel):
    name: Optional[Any] = None
    description: Optional[Any] = None
    tcad_id: Optional[Any] = None
    legal_description: Optional[Any] = None

class Dates(BaseModel):
    applied: Optional[Any] = None
    issued: Optional[Any] = None
    day_issued: Optional[Any] = None
    calendar_year: Optional[Any] = None
    fiscal_year: Optional[Any] = None
    status: Optional[Any] = None
    completed: Optional[Any] = None
    expires: Optional[Any] = None

class Status(BaseModel):
    current: Optional[Any] = None

class Flags(BaseModel):
    issued_last_30: Optional[Any] = None

class Area(BaseModel):
    existing: Optional[Any] = None
    remodel: Optional[Any] = None
    addition: Optional[Any] = None
    lot: Optional[Any] = None

class Building(BaseModel):
    num_floors: Optional[Any] = None
    housing_units: Optional[Any] = None

class Valuation(BaseModel):
    total_job: Optional[Any] = None
    remodel_total: Optional[Any] = None
    building: Optional[Any] = None
    building_remodel: Optional[Any] = None
    electrical: Optional[Any] = None
    electrical_remodel: Optional[Any] = None
    mechanical: Optional[Any] = None
    mechanical_remodel: Optional[Any] = None
    plumbing: Optional[Any] = None
    plumbing_remodel: Optional[Any] = None
    medgas: Optional[Any] = None
    medgas_remodel: Optional[Any] = None

class Coordinates(BaseModel):
    latitude: Optional[Any] = None
    longitude: Optional[Any] = None

class OriginalAddress(BaseModel):
    street_address: Optional[Any] = None
    city: Optional[Any] = None
    state: Optional[Any] = None
    zip: Optional[Any] = None

class Location(BaseModel):
    council_district: Optional[Any] = None
    jurisdiction: Optional[Any] = None
    description: Optional[Any] = None
    geo: Optional[Any] = None
    original: Optional[Any] = None

class Address(BaseModel):
    street: Optional[Any] = None
    unit: Optional[Any] = None
    city: Optional[Any] = None
    zip: Optional[Any] = None

class Contractor(BaseModel):
    trade: Optional[Any] = None
    company_name: Optional[Any] = None
    name: Optional[Any] = None
    phone: Optional[Any] = None
    address: Optional[Any] = None

class Applicant(BaseModel):
    full_name: Optional[Any] = None
    organization: Optional[Any] = None
    phone: Optional[Any] = None
    address: Optional[Any] = None

class PermitRecord(BaseModel):
    permit: Permit
    project: Project
    dates: Dates
    status: Status
    flags: Flags
    area: Area
    building: Building
    valuation: Valuation
    location: Location
    contractor: Contractor
    applicant: Applicant

    @root_validator(pre=True)
    def check_must_have_number(cls, values):
        permit = values.get('permit', {})
        if not permit or not permit.get('number'):
            raise ValueError('Missing required permit.number')
        return values

    class Config:
        extra = 'ignore'
        populate_by_name = True
