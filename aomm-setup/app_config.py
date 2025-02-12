from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    #postgres_password: str = os.getenv("POSTGRES_PWD", "TPQdZ7keCJ")
    #postgres_password: str = "TPQdZ7keCJ"
    postgres_password: str = "Je8e39bOeg"
    
    #db_host: str = "localhost"
    #db_host: str = "dev.tpk.he-pi-os-ohn-004.k8s.dyn.nesc.nokia.net"
    #db_host: str = os.getenv("DB_HOST", "localhost")
    ## Deployment in MLOps NESC
    db_host: str = "prod.ccsmlops.he-pi-os-ohn-005.k8s.dyn.nesc.nokia.net"
    #db_host: str = "34.122.253.56" 
    
    ## For python insert_csv.py along with port 30706 
    #db_host: str = "10.181.4.212"
    
    #db_port: str = os.getenv("DB_PORT", "5432")
    #db_port: str = '5432'
    #db_port: str = '32695'

    ## For python insert_csv.py along with port 30706
    db_port: str = '30706'
    #db_port: str = '30364'

    #root_path: str = os.getenv("ROOT_PATH", "/usr/src/app/")
    root_path: str = "E:\\Deployment\\aomm\\aomm-setup\\"

#settings = Settings()

def setenv(): 
    keys = ["DB_HOST", "DB_PORT", "ROOT_PATH"] 
    for key in keys:
        print(key, os.getenv(key, "---NOT SET---"))


service_dict = {
    'SERVICE_HOME_BB':'Home Broadband',
    'SERVICE_MOBILE':'Mobile Service',
    'SERVICE_ENT_SOLS':'Enterprise Solutions',
    'SERVICE_HBB_ENT_SOLS':'Home BB & Ent. Soln.',
    'SERVICE_ALL':'All Services'
}

dimension_dict = {
    'PARTY':'Party',
    'STRATEGY':'Strategy',
    'TECHNOLOGY':'Technology',
    'OPERATIONS':'Operations',
    'CULTURE':'Culture',
    'DATA':'Data'
}

sub_dimension_dict = {
    '1.1':'Customer Engagement','1.2':'Customer Experience','1.3':'Customer Insight','1.4':'Customer Trust','1.5':'B2B2X Partner Engagement','1.6':'Employee Engagement','1.7':'Engagement of Smart Things',
    '2.1':'Value Model','2.2':'Business Architecture','2.3':'Financial Management','2.4':'Governance Framework','2.5':'Sustainability Management',
    '3.1':'Autonomous Architecture','3.2':'Technology Architecture','3.3':'Technology Resources Management','3.4':'Technology Lifecycle Management',
    '4.1':'Anomaly Resolution','4.2':'Customer Network Experience Assurance','4.3':'Customer Network Complaints Resolution','4.4':'Customer Value Preservation and Uplift','4.5':'Energy Optimization and Operations Carbon Footprint','4.6':'Order Fulfillment',
    '5.1':'Innovation Culture','5.2':'Quality Culture','5.3':'Culture Management','5.4':'Organization Alignment','5.5':'Workplace Enablement',
    '6.1':'Data Life-Cycle Management','6.2':'Data  Quality','6.3':'Data Security','6.4':'Data Monetization'
}

operation_dict = {
    'OP_TM':'Network Planning and Topology Management', 'OP_NOC':'Network Operations Center', 'OP_NA':'Service Operations Center', 'OP_FO':'Field Operations',
    'OP_IM':'Inventory Management', 'OP_SO':'Products and Services', 'OP_CX':'Customer Experience', 'OP_NO':'Network Optimization',
    'OP_AO':'Autonomous Operations', 'OP_OT':'Other Topics'
}

operation_sub_group_dict = {
    'OP_CX_01':'Customer Experience Management',
    'OP_CX_02':'Customer Information Management',
    'OP_CX_03':'Customer Order Management',
    'OP_CX_04':'Customer Behavior Analysis',
    'OP_FO_01':'Asset Management',
    'OP_FO_02':'Work Order Management',
    'OP_IM_01':'Inventory Management',
    'OP_IM_02':'Supply Chain Fulfillment',
    'OP_TM_01':'Network Planning',
    'OP_TM_02':'Network Deployment',
    'OP_TM_03':'Network Topology Management',
    'OP_NA_01':'Service Analysis',
    'OP_NA_02':'Service Management',
    'OP_NA_03':'Service Problem Management',
    'OP_NA_04':'Service Quality and Performance Management',
    'OP_NOC_1':'RAN Network Performance Management',
    'OP_NOC_2':'RAN Network Trouble Management',
    'OP_NOC_3':'Core Network Performance Management',
    'OP_NOC_4':'Core Network Trouble Management',
    'OP_NOC_5':'IP Network Performance Management',
    'OP_NOC_6':'IP and Backhaul Network Trouble Management',
    'OP_NOC_7':'Network Usage Management',
    'OP_NOC_8':'E2E Network Performance Management',
    'OP_NO_01':'Network Capacity Management',
    'OP_NO_02':'Network Optimization for RAN',
    'OP_NO_03':'Network Optimization for Core',
    'OP_NO_04':'Network Optimization for IP and Backhaul',
    'OP_NO_05':'Network Optimization for QoE',
    'OP_NO_06':'Network Traffic Management',
    'OP_NO_07':'Anomaly Management',
    'OP_SO_01':'Product and Service Configuration & Activation',
    'OP_SO_02':'Product and Service Operational Analysis',
    'OP_SO_03':'Product and Service Performance Management',
    'OP_SO_04':'Product and Service Problem Management',
    'OP_SO_05':'Security Management',
    'OP_SO_06':'Service Offer Management',
    'OP_AO_01':'Autonomous Operations Platform and People',
    'OP_AO_02':'Autonomous Operations Culture',
    'OP_AO_03':'Autonomous Operations Business Strategy',
    'OP_OT_01':'B2B2X Partner Engagement',
    'OP_OT_02':'Employee Engagement',
    'OP_OT_03':'Engagement of Smart Things'
}