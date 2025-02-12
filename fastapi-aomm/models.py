from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from enum import Enum
from pydantic import BaseModel, Field, EmailStr

Base = declarative_base()

class Service(Enum):
    SERVICE_HOME_BB = "Home Broadband"
    SERVICE_MOBILE = "Mobile Service"
    SERVICE_ENT_SOLS = "Enterprise Solutions"
    SERVICE_HBB_ENT_SOLS = "Home BB & Ent. Soln."
    SERVICE_ALL = "All Services"

class Operation(Enum):
    OP_TM = "Network Planning and Topology Management"
    OP_NOC = "Network Operations Center"
    OP_NA = "Service Operations Center"
    OP_FO = "Field Operations"
    OP_IM = "Inventory Management"
    OP_SO = "Products and Services"
    OP_CX = "Customer Experience"
    OP_NO = "Network Optimization"
    OP_AO = "Autonomous Operations"
    OP_OT = "Other Topics"

class Operation_Sub_Group(Enum):
    OP_CX_01 = "Customer Experience Management",
    OP_CX_02 = "Customer Information Management",
    OP_CX_03 = "Customer Order Management",
    OP_CX_04 = "Customer Behavior Analysis",
    OP_FO_01 = "Asset Management",
    OP_FO_02 = "Work Order Management",
    OP_IM_01 = "Inventory Management",
    OP_IM_02 = "Supply Chain Fulfillment",
    OP_TM_01 = "Network Planning",
    OP_TM_02 = "Network Deployment",
    OP_TM_03 = "Network Topology Management",
    OP_NA_01 = "Service Analysis",
    OP_NA_02 = "Service Management",
    OP_NA_03 = "Service Problem Management",
    OP_NA_04 = "Service Quality and Performance Management",
    OP_NOC_1 = "RAN Network Performance Management",
    OP_NOC_2 = "RAN Network Trouble Management",
    OP_NOC_3 = "Core Network Performance Management",
    OP_NOC_4 = "Core Network Trouble Management",
    OP_NOC_5 = "IP Network Performance Management",
    OP_NOC_6 = "IP and Backhaul Network Trouble Management",
    OP_NOC_7 = "Network Usage Management",
    OP_NOC_8 = "E2E Network Performance Management",
    OP_NO_01 = "Network Capacity Management",
    OP_NO_02 = "Network Optimization for RAN",
    OP_NO_03 = "Network Optimization for Core",
    OP_NO_04 = "Network Optimization for IP and Backhaul",
    OP_NO_05 = "Network Optimization for QoE",
    OP_NO_06 = "Network Traffic Management",
    OP_NO_07 = "Anomaly Management",
    OP_SO_01 = "Product and Service Configuration & Activation",
    OP_SO_02 = "Product and Service Operational Analysis",
    OP_SO_03 = "Product and Service Performance Management",
    OP_SO_04 = "Product and Service Problem Management",
    OP_SO_05 = "Security Management",
    OP_SO_06 = "Service Offer Management",
    OP_AO_01 = "Autonomous Operations Platform and People",
    OP_AO_02 = "Autonomous Operations Culture",
    OP_AO_03 = "Autonomous Operations Business Strategy",
    OP_OT_01 = "B2B2X Partner Engagement",
    OP_OT_02 = "Employee Engagement",
    OP_OT_03 = "Engagement of Smart Things" 

class Dimension(Enum):
    PARTY = "Party"
    TECHNOLOGY = "Technology"
    CULTURE = "Culture"
    STRATEGY = "Strategy"
    OPERATIONS = "Operations"
    DATA = "Data"

class AOMM_Levels(Enum):
    LEVEL1 = "Initiating"
    LEVEL2 = "Emerging"
    LEVEL3 = "Performing"
    LEVEL4 = "Advancing"
    LEVEL5 = "Leading"

class Sub_Dimension(Base):
    __tablename__ = "sub_dimension"

    id = Column(Integer)
    sub_dimension_id = Column(String, primary_key=True, index=True)
    sub_dimension_name = Column(String, nullable=False)
    sub_dimension_definition = Column(String)
    sub_dimension_context = Column(String)
    dimension = Column(String, nullable=False)

class Criteria(Base):
    __tablename__ = "criteria"

    id = Column(Integer)
    criteria_id = Column(String, primary_key=True, index=True)
    criteria_scope = Column(String)
    criteria_description = Column(String)
    sub_dimension = Column(String, ForeignKey("Sub_Dimension.sub_dimension_id"), nullable=False)

class Attribute(Base):
    __tablename__ = "attribute"

    id = Column(Integer)
    attribute_id = Column(String, primary_key=True, index=True)
    attribute_id_level1 = Column(String)
    attribute_level1 = Column(String)
    attribute_id_level2 = Column(String)
    attribute_level2 = Column(String)
    attribute_id_level3 = Column(String)
    attribute_level3 = Column(String)
    attribute_id_level4 = Column(String)
    attribute_level4 = Column(String)    
    attribute_id_level5 = Column(String)
    attribute_level5 = Column(String)
    criteria_id = Column(String, ForeignKey("Criteria.criteria_id"), nullable=False)

class Technology(Enum):
    TECH_RAN = "Radio Access Network"
    TECH_CORE = "Core Network"
    TECH_IP = "IP Core Network"
    TECH_OPT = "Optical Network"
    TECH_MW = "Transmission and Microwave"
    TECH_FN = "Fixed Network"
    TECH_DC = "Data Center"
    TECH_FO = "Field Operations"
    TECH_INFRA = "Infrastructure Maintenance"

class Value_Stream(Base):
    __tablename__ = "value_stream"

    id = Column(Integer)
    value_stream_id = Column(String, primary_key=True, index=True)
    value_stream_name = Column(String)
    operation = Column(String, nullable=False)
    operation_sub_group = str

class Value_Stream_Technology_Relation(Base):
    __tablename__ = "value_stream_technology_relation"

    relation_id = Column(Integer, primary_key=True, index=True)
    value_stream_id = Column(String)
    technology = Column(String)

class Value_Stream_Service_Relation(Base):
    __tablename__ = "value_stream_service_relation"

    relation_id = Column(Integer, primary_key=True, index=True)
    value_stream_id = Column(String)
    service = Column(String)

class Capability(Base):
    __tablename__ = "capability"

    id = Column(Integer)
    capability_id = Column(String, primary_key=True, index=True)
    capability_name = Column(String)
    capability_definition = Column(String)
    value_stream_id = Column(String, ForeignKey("Value_Stream.value_stream_id"), nullable=False)
    sub_dimension_id = Column(String, ForeignKey("Sub_Dimension.sub_dimension_id"), nullable=False)

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer)
    question_id = Column(String, primary_key=True, index=True)
    question_description = Column(String)
    criteria_id = Column(String, ForeignKey("Criteria.criteria_id"), nullable=False)

class Capability_Question_Relation(Base):
    __tablename__ = "capability_question_relation"

    capability_id = Column(String, ForeignKey("Capability.capability_id"), primary_key=True, nullable=False)
    question_id = Column(String, ForeignKey("Question.question_id"), primary_key=True, nullable=False)

class CLA(Base):
    __tablename__ = "cla"

    id = Column(Integer)
    cla_id = Column(String, primary_key=True, index=True)
    cla_level1_id = Column(String)
    cla_level1_description = Column(String)
    cla_level2_id = Column(String)
    cla_level2_description = Column(String)
    cla_level3_id = Column(String)
    cla_level3_description = Column(String)
    cla_level4_id = Column(String)
    cla_level4_description = Column(String)
    cla_level5_id = Column(String)
    cla_level5_description = Column(String)                
    question_id = Column(String, ForeignKey("Question.question_id"), nullable=False)
    attribute_id = Column(String, ForeignKey("Attribute.attribute_id"), nullable=False)

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    AUDIT = "audit"
    REPORT = "report"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer)
    user_id = Column(String, primary_key=True, index=True)
    fname = Column(String)
    lname = Column(String)
    email : EmailStr = Column(String)
    role = Column(String)
    hashed_password = Column(String)
    creation_time = Column(DateTime)
    last_login_time = Column(DateTime)
    is_active = Column(Boolean, default=True)

class User_Operation_Map(Base):
    __tablename__ = "user_operation_map"

    relation_id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("User.user_id"), nullable=False)
    operation_id = Column(String, nullable=False)

class UserSchema(BaseModel):
    fullname: str = Field(default = None)
    email: EmailStr = Field(default = None)
    password: str = Field(default = None)

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Joe Doe",
                "email": "joe@xyz.com",
                "password": "any"
            }
        }

class Self_Assessment(Base):
    __tablename__ = "self_assessment"

    id = Column(Integer)
    self_assessment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creation_time = Column(DateTime)
    update_time = Column(DateTime)
    user_id = Column(String, ForeignKey("User.user_id"), nullable=False)
    service = Column(String)
    operation = Column(String)
    operation_sub_group = Column(String)
    is_archived = Column(String, nullable=False, default="f")


class SA_Technology_Relation(Base):
    __tablename__ = "sa_technology_relation"

    relation_id = Column(Integer, primary_key=True, index=True)
    self_assessment_id = Column(UUID(as_uuid=True), ForeignKey("Self_Assessment.self_assessment_id"), nullable=False)
    technology = Column(String)

class SA_Question_Relation(Base):
    __tablename__ = "sa_question_relation"

    relation_id = Column(Integer, primary_key=True, index=True)
    self_assessment_id = Column(UUID(as_uuid=True), ForeignKey("Self_Assessment.self_assessment_id"), nullable=False)
    question_id = Column(String, ForeignKey("Question.question_id"), nullable=False)
    weighting = Column(Integer)
    selected_cla_level_id = Column(String, nullable=False)
    cla_level = Column(String)
    capability_id = Column(String, ForeignKey("Capability.capability_id"), nullable=False)
    value_stream_id = Column(String, ForeignKey("Value_Stream.value_stream_id"), nullable=False)
    criteria_id = Column(String, ForeignKey("Criteria.criteria_id"), nullable=False)
    sub_dimension_id = Column(String, ForeignKey("Sub_Dimension.sub_dimension_id"), nullable=False)
    capability_score = Column(Float)
    is_archived = Column(String, nullable=False, default="f")


class UserLogin(BaseModel):
    email: EmailStr = Field(default = None)
    password: str = Field(default = None)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any"
            }
        }