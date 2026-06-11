import random

from datetime import date, timedelta
from typing import Tuple

from ..db.models import (
    Candidate, CandidateEducation, CandidateGDPR, CandidateWorkExperience,
    ClientContact, ClientCorporation,
)
from ..db.session import SessionLocal


def c(eid, fn, ln, gen, dob, city, zipcode, state, mobile, email, source, avail, status, category, skills):
    return Candidate(
        external_id=eid, first_name=fn, last_name=ln, gender=gen,
        date_of_birth=dob, address_city=city, address_zip=zipcode,
        address_state=state, address_country_id="NL",
        mobile=mobile, email=email, source=source,
        date_available=avail, status=status,
        business_sector_id="IT", category=category, skill_id=skills,
    )


def edu(eid, cid, degree, school, city, start, end, comments=None):
    return CandidateEducation(
        external_id=eid, candidate_external_id=cid,
        degree=degree, school=school, city=city,
        start_date=start, end_date=end, comments=comments,
    )


def wx(eid, cid, title, company, start, end, comments=None):
    return CandidateWorkExperience(
        external_id=eid, candidate_external_id=cid,
        title=title, company_name=company,
        start_date=start, end_date=end, comments=comments,
    )


def gdpr(cid, purpose, basis, sent, received, source):
    return CandidateGDPR(
        candidate_external_id=cid, consent_purpose=purpose,
        legal_basis=basis, date_last_sent=sent,
        date_last_received=received, consent_source=source,
    )

CANDIDATES = [
    c("CV-00101","Pieter","van den Berg","M",date(1986,3,14),"Amsterdam","1012 AB","Noord-Holland","+31 6 28493751","p.vandenberg@email.nl","LinkedIn",date(2025,2,1),"Freelancer","Software Engineering","Java,Spring Boot,AWS"),
    c("CV-00102","Fatima","El Amrani","F",date(1995,7,22),"Rotterdam","3011 BK","Zuid-Holland","+31 6 51934827","f.elamrani@email.nl","Direct",date(2026,2,19),"New","Cloud Engineering","Azure,Terraform,Kubernetes"),
    c("CV-00103","Bas","Jansen","M",date(1982,11,5),"Utrecht","3512 JE","Utrecht","+31 6 43928174","b.jansen@email.nl","Referral",date(2025,6,1),"Employed","DevOps","Kubernetes,Docker,CI/CD,Ansible"),
    c("CV-00104","Anouk","de Vries","F",date(1993,4,30),"Eindhoven","5611 AZ","Noord-Brabant","+31 6 17384926","a.devries@email.nl","LinkedIn",date(2025,12,15),"Freelancer","Data Engineering","Python,Spark,dbt,Snowflake"),
    c("CV-00105","Thomas","Bakker","M",date(1989,9,17),"Den Haag","2511 CR","Zuid-Holland","+31 6 92847361","t.bakker@email.nl","Indeed",date(2026,1,1),"Freelancer","Cybersecurity","SIEM,Penetration Testing,ISO27001"),
    c("CV-00106","Lena","Müller","F",date(1991,6,8),"Amsterdam","1017 SZ","Noord-Holland","+31 6 63748291","l.muller@email.nl","LinkedIn",date(2026,3,1),"Employed","Software Engineering","Python,Django,PostgreSQL,React"),
    c("CV-00107","Joris","Vermeer","M",date(1984,1,25),"Groningen","9711 HK","Groningen","+31 6 84736291","j.vermeer@email.nl","Referral",date(2025,9,1),"Freelancer","Solutions Architecture","AWS,GCP,Microservices,Event-Driven"),
    c("CV-00108","Sara","Kowalski","F",date(1997,12,3),"Amsterdam","1054 LM","Noord-Holland","+31 6 29384756","s.kowalski@email.nl","Direct",date(2026,4,1),"New","Data Science","Python,ML,TensorFlow,Pandas"),
    c("CV-00109","Kevin","Smits","M",date(1988,8,19),"Breda","4811 ZG","Noord-Brabant","+31 6 57483920","k.smits@email.nl","LinkedIn",date(2025,11,1),"Employed","Software Engineering",".NET,C#,Azure,SQL Server"),
    c("CV-00110","Nadia","Benali","F",date(1990,2,14),"Utrecht","3521 VX","Utrecht","+31 6 73849261","n.benali@email.nl","Referral",date(2026,1,15),"Freelancer","IT Management","ITIL,Prince2,Agile,Scrum"),
    c("CV-00111","Lars","Andersen","M",date(1985,5,11),"Haarlem","2011 VB","Noord-Holland","+31 6 94857362","l.andersen@email.nl","LinkedIn",date(2026,2,1),"Freelancer","DevOps","Linux,Bash,Jenkins,GitLab CI,Terraform"),
    c("CV-00112","Isabelle","Dupont","F",date(1994,10,27),"Maastricht","6211 EM","Limburg","+31 6 38492716","i.dupont@email.nl","Direct",date(2026,6,1),"Employed","Software Engineering","Java,Kotlin,Microservices,Kafka"),
    c("CV-00113","Mehmet","Yilmaz","M",date(1987,3,6),"Amsterdam","1097 DN","Noord-Holland","+31 6 62839471","m.yilmaz@email.nl","LinkedIn",date(2025,10,1),"Freelancer","Cloud Engineering","AWS,CloudFormation,Lambda,EKS"),
    c("CV-00114","Sophie","van Dijk","F",date(1992,8,15),"Rotterdam","3072 AP","Zuid-Holland","+31 6 47382916","s.vandijk@email.nl","Referral",date(2026,3,15),"New","Data Engineering","SQL,Airflow,BigQuery,dbt"),
    c("CV-00115","Rafael","Gomez","M",date(1983,12,22),"Leiden","2312 BK","Zuid-Holland","+31 6 58473920","r.gomez@email.nl","LinkedIn",date(2025,8,1),"Employed","Solutions Architecture","Azure,SAP,Integration,TOGAF"),

    # --- Frontend (CV-00116 – CV-00125) ---
    c("CV-00116","Emma","Visser","F",date(1994,5,3),"Amsterdam","1055 KL","Noord-Holland","+31 6 11122233","e.visser@email.nl","LinkedIn",date(2026,3,1),"Freelancer","Frontend Development","React,TypeScript,Next.js,GraphQL"),
    c("CV-00117","Daan","Bosman","M",date(1991,8,14),"Rotterdam","3014 GH","Zuid-Holland","+31 6 22233344","d.bosman@email.nl","Direct",date(2025,11,1),"Employed","Frontend Development","Angular,RxJS,NgRx,Jest"),
    c("CV-00118","Yasmine","Oussama","F",date(1996,2,19),"Utrecht","3521 AL","Utrecht","+31 6 33344455","y.oussama@email.nl","LinkedIn",date(2026,6,1),"New","Frontend Development","Vue.js,Nuxt,Tailwind,Cypress"),
    c("CV-00119","Ruben","Hartman","M",date(1989,11,7),"Haarlem","2023 BT","Noord-Holland","+31 6 44455566","r.hartman@email.nl","Referral",date(2026,1,15),"Freelancer","Frontend Development","React,Redux,Node.js,AWS Amplify"),
    c("CV-00120","Chloé","Bernard","F",date(1993,6,25),"Amsterdam","1016 VR","Noord-Holland","+31 6 55566677","c.bernard@email.nl","LinkedIn",date(2025,9,1),"Employed","Frontend Development","React Native,TypeScript,Expo,Firebase"),
    c("CV-00121","Niels","Kuijpers","M",date(1988,3,12),"Eindhoven","5612 HN","Noord-Brabant","+31 6 66677788","n.kuijpers@email.nl","Direct",date(2026,2,1),"Freelancer","Frontend Development","Angular,Java,Spring,REST APIs"),
    c("CV-00122","Aisha","Nkosi","F",date(1997,9,30),"Amsterdam","1093 KV","Noord-Holland","+31 6 77788899","a.nkosi@email.nl","LinkedIn",date(2026,4,1),"New","Frontend Development","React,Storybook,Figma,Accessibility"),
    c("CV-00123","Finn","Dijkstra","M",date(1990,1,18),"Groningen","9711 EP","Groningen","+31 6 88899900","f.dijkstra@email.nl","Referral",date(2025,10,15),"Freelancer","Frontend Development","Vue.js,React,TypeScript,Webpack"),
    c("CV-00124","Mila","Petrovic","F",date(1995,7,8),"Den Haag","2512 EM","Zuid-Holland","+31 6 99900011","m.petrovic@email.nl","LinkedIn",date(2026,5,1),"Employed","Frontend Development","React,GraphQL,Apollo,styled-components"),
    c("CV-00125","Tim","van Leeuwen","M",date(1986,4,22),"Amersfoort","3812 JK","Utrecht","+31 6 10011122","t.vanleeuwen@email.nl","Direct",date(2025,12,1),"Freelancer","Frontend Development","Angular,Micro Frontends,Performance,Webpack"),

    # --- Backend (CV-00126 – CV-00135) ---
    c("CV-00126","Mark","de Groot","M",date(1987,10,5),"Amsterdam","1019 EX","Noord-Holland","+31 6 21122334","m.degroot@email.nl","LinkedIn",date(2026,1,1),"Freelancer","Backend Development","Node.js,TypeScript,PostgreSQL,Redis"),
    c("CV-00127","Priya","Sharma","F",date(1992,3,16),"Rotterdam","3032 AG","Zuid-Holland","+31 6 32233445","p.sharma@email.nl","Direct",date(2025,8,1),"Employed","Backend Development","Python,FastAPI,Celery,MongoDB"),
    c("CV-00128","Erik","Nilsson","M",date(1985,12,1),"Amsterdam","1077 ZT","Noord-Holland","+31 6 43344556","e.nilsson@email.nl","Referral",date(2026,3,15),"Freelancer","Backend Development","Go,gRPC,Kubernetes,PostgreSQL"),
    c("CV-00129","Laila","Benjelloun","F",date(1994,8,27),"Leiden","2316 XA","Zuid-Holland","+31 6 54455667","l.benjelloun@email.nl","LinkedIn",date(2026,6,1),"New","Backend Development","Python,Django,REST,Celery,Docker"),
    c("CV-00130","Sander","Molenaar","M",date(1990,6,3),"Utrecht","3524 CB","Utrecht","+31 6 65566778","s.molenaar@email.nl","Direct",date(2025,11,15),"Freelancer","Backend Development","Rust,WebAssembly,Microservices,gRPC"),
    c("CV-00131","Ines","Garcia","F",date(1993,1,14),"Amsterdam","1054 RV","Noord-Holland","+31 6 76677889","i.garcia@email.nl","LinkedIn",date(2026,2,1),"Employed","Backend Development","Ruby on Rails,PostgreSQL,Redis,AWS"),
    c("CV-00132","Wouter","Hendricks","M",date(1988,9,21),"Breda","4816 CC","Noord-Brabant","+31 6 87788990","w.hendricks@email.nl","Referral",date(2025,10,1),"Freelancer","Backend Development","PHP,Laravel,MySQL,Docker,Vue.js"),
    c("CV-00133","Zara","Hassan","F",date(1996,11,9),"Amsterdam","1062 KP","Noord-Holland","+31 6 98899001","z.hassan@email.nl","LinkedIn",date(2026,5,1),"New","Backend Development","Node.js,Express,MongoDB,GraphQL"),
    c("CV-00134","Arjan","Brouwer","M",date(1983,7,30),"Nijmegen","6512 BT","Gelderland","+31 6 09900112","a.brouwer@email.nl","Direct",date(2026,1,15),"Freelancer","Backend Development","Go,Microservices,Event-Driven,Kafka"),
    c("CV-00135","Vera","Konings","F",date(1991,4,17),"Tilburg","5032 ML","Noord-Brabant","+31 6 11012123","v.konings@email.nl","LinkedIn",date(2025,9,15),"Employed","Backend Development","Python,Flask,SQLAlchemy,Elasticsearch"),

    # --- Cloud Engineering (CV-00136 – CV-00143) ---
    c("CV-00136","Rick","Oosterhout","M",date(1989,2,8),"Amsterdam","1098 XB","Noord-Holland","+31 6 22123234","r.oosterhout@email.nl","LinkedIn",date(2026,2,15),"Freelancer","Cloud Engineering","GCP,BigQuery,Dataflow,Terraform"),
    c("CV-00137","Samira","Tahir","F",date(1993,6,19),"Rotterdam","3071 PR","Zuid-Holland","+31 6 33234345","s.tahir@email.nl","Direct",date(2025,11,1),"Employed","Cloud Engineering","Azure,Kubernetes,Helm,ArgoCD"),
    c("CV-00138","Bart","Willems","M",date(1986,10,3),"Eindhoven","5615 GC","Noord-Brabant","+31 6 44345456","b.willems@email.nl","Referral",date(2026,4,1),"Freelancer","Cloud Engineering","Multi-Cloud,AWS,Azure,GCP,FinOps"),
    c("CV-00139","Hana","Novak","F",date(1995,3,27),"Zwolle","8011 MR","Overijssel","+31 6 55456567","h.novak@email.nl","LinkedIn",date(2026,7,1),"New","Cloud Engineering","AWS,Lambda,API Gateway,CDK"),
    c("CV-00140","Gerard","Prins","M",date(1984,8,15),"Den Haag","2595 AN","Zuid-Holland","+31 6 66567678","g.prins@email.nl","Direct",date(2025,10,1),"Freelancer","Cloud Engineering","GCP,Anthos,Cloud Run,Istio"),
    c("CV-00141","Naomi","Vos","F",date(1992,12,4),"Utrecht","3511 KA","Utrecht","+31 6 77678789","n.vos@email.nl","LinkedIn",date(2026,3,1),"Employed","Cloud Engineering","Azure,DevOps,Pipelines,ARM Templates"),
    c("CV-00142","Stefan","Klaassen","M",date(1987,5,22),"Arnhem","6826 AB","Gelderland","+31 6 88789890","s.klaassen@email.nl","Referral",date(2026,1,1),"Freelancer","Cloud Engineering","AWS,ECS,EKS,Fargate,Observability"),
    c("CV-00143","Dana","Wolff","F",date(1990,9,11),"Haarlem","2015 CK","Noord-Holland","+31 6 99890901","d.wolff@email.nl","LinkedIn",date(2025,12,1),"Freelancer","Cloud Engineering","GCP,Kubernetes,Terraform,Prometheus"),

    # --- DevOps / SRE (CV-00144 – CV-00151) ---
    c("CV-00144","Jurgen","Hendriks","M",date(1985,1,16),"Amsterdam","1043 GH","Noord-Holland","+31 6 10901012","j.hendriks@email.nl","Direct",date(2026,2,1),"Freelancer","Site Reliability Engineering","SRE,Prometheus,Grafana,PagerDuty,Go"),
    c("CV-00145","Myrthe","van Rijn","F",date(1993,7,29),"Rotterdam","3066 PB","Zuid-Holland","+31 6 21012123","m.vanrijn@email.nl","LinkedIn",date(2025,9,1),"Employed","DevOps","GitOps,ArgoCD,Flux,Kubernetes,Helm"),
    c("CV-00146","Florian","Berger","M",date(1988,4,6),"Amsterdam","1091 DZ","Noord-Holland","+31 6 32123234","f.berger@email.nl","Referral",date(2026,5,1),"Freelancer","DevOps","Platform Engineering,Backstage,GitHub Actions,Terraform"),
    c("CV-00147","Roos","Smeets","F",date(1994,10,20),"Eindhoven","5611 BK","Noord-Brabant","+31 6 43234345","r.smeets@email.nl","LinkedIn",date(2026,1,1),"New","DevOps","Jenkins,Ansible,Docker,AWS,Python"),
    c("CV-00148","Koen","de Leeuw","M",date(1982,3,5),"Utrecht","3515 GE","Utrecht","+31 6 54345456","k.deleeuw@email.nl","Direct",date(2025,11,1),"Freelancer","Site Reliability Engineering","SRE,Chaos Engineering,Reliability,Linux,Go"),
    c("CV-00149","Bilal","Arslan","M",date(1991,8,17),"Amsterdam","1068 MV","Noord-Holland","+31 6 65456567","b.arslan@email.nl","LinkedIn",date(2026,4,1),"Employed","DevOps","Azure DevOps,Kubernetes,Terraform,Python"),
    c("CV-00150","Hannah","de Wit","F",date(1989,5,2),"Groningen","9726 GC","Groningen","+31 6 76567678","h.dewit@email.nl","Referral",date(2026,3,1),"Freelancer","DevOps","CI/CD,GitLab,Docker,Kubernetes,Monitoring"),
    c("CV-00151","Erwin","Timmermans","M",date(1984,11,28),"Tilburg","5037 DA","Noord-Brabant","+31 6 87678789","e.timmermans@email.nl","Direct",date(2025,10,15),"Freelancer","Site Reliability Engineering","SRE,Observability,OpenTelemetry,AWS,Scala"),

    # --- Data Science / ML (CV-00152 – CV-00159) ---
    c("CV-00152","Julia","Bergmann","F",date(1993,4,11),"Amsterdam","1071 CS","Noord-Holland","+31 6 98789890","j.bergmann@email.nl","LinkedIn",date(2026,2,1),"Employed","Machine Learning Engineering","Python,PyTorch,MLflow,Kubeflow,AWS SageMaker"),
    c("CV-00153","Ahmed","El Khattabi","M",date(1990,9,3),"Rotterdam","3051 HK","Zuid-Holland","+31 6 09890901","a.elkhattabi@email.nl","Direct",date(2026,1,1),"Freelancer","Data Science","Python,scikit-learn,XGBoost,Feature Engineering"),
    c("CV-00154","Lotte","Baas","F",date(1996,1,25),"Utrecht","3583 EZ","Utrecht","+31 6 10901012","l.baas@email.nl","LinkedIn",date(2026,5,1),"New","Data Science","Python,NLP,BERT,LangChain,RAG"),
    c("CV-00155","Victor","Popescu","M",date(1988,6,14),"Amsterdam","1081 KC","Noord-Holland","+31 6 21012123","v.popescu@email.nl","Referral",date(2025,11,1),"Freelancer","Machine Learning Engineering","Python,TensorFlow,Vertex AI,GCP,MLOps"),
    c("CV-00156","Sofie","Claes","F",date(1994,10,7),"Maastricht","6229 HN","Limburg","+31 6 32123234","s.claes@email.nl","LinkedIn",date(2026,3,1),"Employed","Data Science","R,Python,Statistics,A/B Testing,Tableau"),
    c("CV-00157","Mikael","Lindqvist","M",date(1987,2,19),"Amsterdam","1052 ZV","Noord-Holland","+31 6 43234345","m.lindqvist@email.nl","Direct",date(2026,1,1),"Freelancer","Machine Learning Engineering","LLMs,Fine-tuning,RAG,LangChain,OpenAI API"),
    c("CV-00158","Noor","van den Heuvel","F",date(1997,8,6),"Nijmegen","6544 RT","Gelderland","+31 6 54345456","n.vandenheuvel@email.nl","LinkedIn",date(2026,6,1),"New","Data Science","Python,Pandas,Spark,Statistics,Visualization"),
    c("CV-00159","Olivier","Fontaine","M",date(1985,3,30),"Amsterdam","1060 AB","Noord-Holland","+31 6 65456567","o.fontaine@email.nl","Referral",date(2025,9,1),"Freelancer","Machine Learning Engineering","Python,Recommendation Systems,Real-Time ML,Kafka"),

    # --- Mobile (CV-00160 – CV-00165) ---
    c("CV-00160","Lieke","Janssen","F",date(1994,6,9),"Amsterdam","1016 EG","Noord-Holland","+31 6 76567678","l.janssen@email.nl","LinkedIn",date(2026,2,1),"Employed","Mobile Development","iOS,Swift,SwiftUI,Combine,XCTest"),
    c("CV-00161","Nathan","Kramer","M",date(1990,1,28),"Rotterdam","3082 NA","Zuid-Holland","+31 6 87678789","n.kramer@email.nl","Direct",date(2025,10,1),"Freelancer","Mobile Development","Android,Kotlin,Jetpack Compose,Coroutines"),
    c("CV-00162","Anita","Pawlak","F",date(1993,9,16),"Utrecht","3582 KL","Utrecht","+31 6 98789890","a.pawlak@email.nl","LinkedIn",date(2026,4,1),"Employed","Mobile Development","React Native,TypeScript,Redux,Detox"),
    c("CV-00163","Jeroen","van Essen","M",date(1987,5,4),"Arnhem","6821 DB","Gelderland","+31 6 09890901","j.vanessen@email.nl","Referral",date(2026,1,15),"Freelancer","Mobile Development","Flutter,Dart,Firebase,BLoC,iOS+Android"),
    c("CV-00164","Manon","Lecomte","F",date(1995,12,22),"Amsterdam","1034 SE","Noord-Holland","+31 6 10901012","m.lecomte@email.nl","LinkedIn",date(2026,6,1),"New","Mobile Development","iOS,Swift,Objective-C,Core Data,ARKit"),
    c("CV-00165","Stijn","Dekker","M",date(1988,8,13),"Haarlem","2021 BZ","Noord-Holland","+31 6 21012123","s.dekker@email.nl","Direct",date(2025,11,1),"Freelancer","Mobile Development","Android,Kotlin,MVVM,Dagger,CI/CD"),

    # --- QA / Test Engineering (CV-00166 – CV-00170) ---
    c("CV-00166","Iris","Manders","F",date(1992,3,7),"Amsterdam","1019 VP","Noord-Holland","+31 6 32123234","i.manders@email.nl","LinkedIn",date(2026,2,1),"Employed","Test Engineering","Selenium,Playwright,Python,BDD,Cucumber"),
    c("CV-00167","Owen","Jacobs","M",date(1989,10,19),"Rotterdam","3042 AK","Zuid-Holland","+31 6 43234345","o.jacobs@email.nl","Direct",date(2025,9,15),"Freelancer","Test Engineering","JMeter,k6,Performance Testing,API Testing,Postman"),
    c("CV-00168","Denise","Hofmann","F",date(1994,7,1),"Utrecht","3531 GX","Utrecht","+31 6 54345456","d.hofmann@email.nl","LinkedIn",date(2026,5,1),"New","Test Engineering","Cypress,Playwright,TypeScript,CI/CD,SDET"),
    c("CV-00169","Michel","Willems","M",date(1985,1,23),"Eindhoven","5654 PA","Noord-Brabant","+31 6 65456567","m.willems2@email.nl","Referral",date(2026,1,1),"Freelancer","Test Engineering","Test Automation,Robot Framework,Python,Azure DevOps"),
    c("CV-00170","Tess","Vermeer","F",date(1997,5,14),"Amsterdam","1042 AH","Noord-Holland","+31 6 76567678","t.vermeer@email.nl","LinkedIn",date(2026,8,1),"New","Test Engineering","Manual Testing,Agile,JIRA,Zephyr,API Testing"),

    # --- Cybersecurity (CV-00171 – CV-00175) ---
    c("CV-00171","Patrick","Wolters","M",date(1984,9,2),"Amsterdam","1083 HN","Noord-Holland","+31 6 87678789","p.wolters@email.nl","Direct",date(2025,10,1),"Freelancer","Cybersecurity","SOC,SIEM,Splunk,Threat Hunting,Incident Response"),
    c("CV-00172","Leila","Ahmadi","F",date(1991,4,15),"Rotterdam","3022 CB","Zuid-Holland","+31 6 98789890","l.ahmadi@email.nl","LinkedIn",date(2026,3,1),"Employed","Cybersecurity","Pentesting,Burp Suite,OWASP,Red Team,CEH"),
    c("CV-00173","Dennis","van Houten","M",date(1987,11,27),"Den Haag","2541 EK","Zuid-Holland","+31 6 09890901","d.vanhouten@email.nl","Referral",date(2026,1,1),"Freelancer","Cybersecurity","Cloud Security,AWS Security,Zero Trust,IAM,CSPM"),
    c("CV-00174","Amber","Schouten","F",date(1995,2,18),"Amsterdam","1075 VK","Noord-Holland","+31 6 10901012","a.schouten@email.nl","LinkedIn",date(2026,5,1),"New","Cybersecurity","GRC,ISO27001,DORA,Risk Management,Compliance"),
    c("CV-00175","Rik","van der Berg","M",date(1982,7,9),"Utrecht","3584 AA","Utrecht","+31 6 21012123","r.vanderberg@email.nl","Direct",date(2025,11,15),"Freelancer","Cybersecurity","AppSec,SAST,DAST,DevSecOps,OWASP Top 10"),

    # --- SAP / ERP (CV-00176 – CV-00180) ---
    c("CV-00176","Hans","Becker","M",date(1979,6,6),"Amsterdam","1078 LG","Noord-Holland","+31 6 32123234","h.becker@email.nl","Referral",date(2026,1,1),"Freelancer","SAP Consulting","SAP S/4HANA,FI/CO,ABAP,Migration"),
    c("CV-00177","Claudia","Peters","F",date(1983,10,31),"Rotterdam","3054 NB","Zuid-Holland","+31 6 43234345","c.peters@email.nl","Direct",date(2025,10,1),"Employed","SAP Consulting","SAP MM,PP,WM,S/4HANA,Fiori"),
    c("CV-00178","Thijs","van Wijk","M",date(1986,3,23),"Eindhoven","5622 EK","Noord-Brabant","+31 6 54345456","t.vanwijk@email.nl","LinkedIn",date(2026,3,1),"Freelancer","ERP Consulting","Oracle ERP,Finance,Supply Chain,OIC"),
    c("CV-00179","Karen","Brandt","F",date(1980,8,12),"Utrecht","3581 GZ","Utrecht","+31 6 65456567","k.brandt@email.nl","Referral",date(2026,2,1),"Freelancer","SAP Consulting","SAP BW/4HANA,Analytics,BEx,SAC,Reporting"),
    c("CV-00180","Martijn","Hols","M",date(1988,1,4),"Amsterdam","1017 AH","Noord-Holland","+31 6 76567678","m.hols@email.nl","LinkedIn",date(2025,12,1),"Employed","SAP Consulting","SAP CRM,C4C,S/4HANA SD,Integration"),

    # --- IT Management / PM / Scrum (CV-00181 – CV-00185) ---
    c("CV-00181","Simone","van Beek","F",date(1981,4,19),"Amsterdam","1082 MT","Noord-Holland","+31 6 87678789","s.vanbeek@email.nl","Direct",date(2025,11,1),"Freelancer","IT Management","CTO Advisory,IT Strategy,Budgeting,Governance"),
    c("CV-00182","Jesse","Peeters","M",date(1986,9,8),"Rotterdam","3061 VN","Zuid-Holland","+31 6 98789890","j.peeters@email.nl","LinkedIn",date(2026,2,1),"Employed","Programme Management","Agile,SAFe,Programme Delivery,Stakeholder Mgmt"),
    c("CV-00183","Lara","Vogel","F",date(1992,12,26),"Utrecht","3542 AD","Utrecht","+31 6 09890901","l.vogel@email.nl","Referral",date(2026,4,1),"Freelancer","Scrum Mastery","Scrum,Kanban,Coaching,Facilitation,LeSS"),
    c("CV-00184","Pieter","de Haas","M",date(1977,5,15),"Den Haag","2516 AK","Zuid-Holland","+31 6 10901012","p.dehaas@email.nl","Direct",date(2025,10,1),"Freelancer","IT Management","ITIL,Service Management,SIAM,Vendor Mgmt"),
    c("CV-00185","Wendy","Fontijn","F",date(1983,2,3),"Amsterdam","1066 CX","Noord-Holland","+31 6 21012123","w.fontijn@email.nl","LinkedIn",date(2026,1,15),"Employed","Product Management","Product Ownership,Roadmap,B2B SaaS,OKRs"),

    # --- Database / BI (CV-00186 – CV-00190) ---
    c("CV-00186","Geert","van Loon","M",date(1980,7,17),"Amsterdam","1087 GN","Noord-Holland","+31 6 32123234","g.vanloon@email.nl","Referral",date(2026,2,1),"Freelancer","Database Administration","Oracle DBA,PostgreSQL,Performance Tuning,RAC"),
    c("CV-00187","Maja","Kowal","F",date(1989,11,5),"Rotterdam","3039 KE","Zuid-Holland","+31 6 43234345","m.kowal@email.nl","Direct",date(2025,9,1),"Employed","Business Intelligence","Power BI,DAX,SQL Server,SSAS,Azure Synapse"),
    c("CV-00188","Chris","Boersma","M",date(1985,4,28),"Utrecht","3551 RB","Utrecht","+31 6 54345456","c.boersma@email.nl","LinkedIn",date(2026,3,1),"Freelancer","Database Administration","SQL Server DBA,SSIS,SSRS,Always On,Azure SQL"),
    c("CV-00189","Amy","de Jong","F",date(1993,8,14),"Eindhoven","5614 HZ","Noord-Brabant","+31 6 65456567","a.dejong@email.nl","Referral",date(2026,6,1),"New","Business Intelligence","Tableau,Looker,dbt,BigQuery,Analytics Engineering"),
    c("CV-00190","Leon","Vermaat","M",date(1982,1,9),"Haarlem","2024 ZV","Noord-Holland","+31 6 76567678","l.vermaat@email.nl","Direct",date(2025,11,1),"Freelancer","Database Administration","MongoDB,Redis,Cassandra,NoSQL Architecture"),

    # --- Network / Infrastructure (CV-00191 – CV-00193) ---
    c("CV-00191","Frank","Schipper","M",date(1979,3,14),"Amsterdam","1096 AG","Noord-Holland","+31 6 87678789","f.schipper@email.nl","Referral",date(2026,1,1),"Freelancer","Network Engineering","Cisco,CCNP,SD-WAN,BGP,OSPF,VPN"),
    c("CV-00192","Bianca","Kuiper","F",date(1986,10,25),"Rotterdam","3045 AN","Zuid-Holland","+31 6 98789890","b.kuiper@email.nl","Direct",date(2025,12,1),"Employed","Network Engineering","Juniper,Palo Alto,Network Security,Firewall,Zero Trust"),
    c("CV-00193","Robbert","van den Bosch","M",date(1981,6,7),"Utrecht","3555 KT","Utrecht","+31 6 09890901","r.vandenbosch@email.nl","LinkedIn",date(2026,4,1),"Freelancer","Infrastructure Engineering","VMware,vSphere,vSAN,NSX,HCI,Nutanix"),

    # --- Salesforce / ServiceNow (CV-00194 – CV-00196) ---
    c("CV-00194","Nicole","de Bruin","F",date(1988,2,21),"Amsterdam","1079 MH","Noord-Holland","+31 6 10901012","n.debruin@email.nl","LinkedIn",date(2026,2,1),"Freelancer","Salesforce Development","Salesforce,Apex,LWC,Sales Cloud,Service Cloud"),
    c("CV-00195","Bas","Vrijman","M",date(1984,7,3),"Rotterdam","3068 AV","Zuid-Holland","+31 6 21012123","b.vrijman@email.nl","Direct",date(2025,10,1),"Employed","ServiceNow Development","ServiceNow,ITSM,ITOM,Flow Designer,Scripting"),
    c("CV-00196","Suzan","Haan","F",date(1991,5,16),"Utrecht","3527 GE","Utrecht","+31 6 32123234","s.haan@email.nl","Referral",date(2026,3,15),"Freelancer","Salesforce Consulting","Salesforce,Marketing Cloud,CDP,CPQ,Pardot"),

    # --- Business Analysis / Architecture (CV-00197 – CV-00200) ---
    c("CV-00197","Tom","Groen","M",date(1983,9,29),"Amsterdam","1057 CK","Noord-Holland","+31 6 43234345","t.groen@email.nl","LinkedIn",date(2026,1,1),"Freelancer","Business Analysis","Business Analysis,BABOK,UML,Process Modelling,Agile"),
    c("CV-00198","Roos","Vliet","F",date(1990,4,12),"Rotterdam","3077 BG","Zuid-Holland","+31 6 54345456","r.vliet@email.nl","Direct",date(2025,11,15),"Employed","Business Analysis","Requirements Engineering,BPMN,Stakeholder Mgmt,SQL"),
    c("CV-00199","Kees","Overbeek","M",date(1978,12,18),"Den Haag","2595 BM","Zuid-Holland","+31 6 65456567","k.overbeek@email.nl","Referral",date(2026,3,1),"Freelancer","IT Architecture","Enterprise Architecture,TOGAF,Archimate,IT Strategy"),
    c("CV-00200","Lisa","Franken","F",date(1987,6,24),"Amsterdam","1015 HG","Noord-Holland","+31 6 76567678","l.franken@email.nl","LinkedIn",date(2026,5,1),"Employed","IT Architecture","Solution Architecture,Azure,Domain-Driven Design,API Design"),
]

EDUCATION = [
    edu("EDU-001","CV-00101","MSc Software Engineering","TU Delft","Delft",date(2010,9,1),date(2012,6,30)),
    edu("EDU-002","CV-00101","BSc Computer Science","Vrije Universiteit Amsterdam","Amsterdam",date(2007,9,1),date(2010,6,30)),
    edu("EDU-003","CV-00102","MSc Cloud Computing","University of Amsterdam","Amsterdam",date(2018,9,1),date(2020,6,30)),
    edu("EDU-004","CV-00102","BSc Information Technology","Hogeschool Rotterdam","Rotterdam",date(2015,9,1),date(2018,6,30)),
    edu("EDU-005","CV-00103","BSc Computer Science","Utrecht University","Utrecht",date(2001,9,1),date(2005,6,30)),
    edu("EDU-006","CV-00104","MSc Data Science","Eindhoven University of Technology","Eindhoven",date(2016,9,1),date(2018,6,30)),
    edu("EDU-007","CV-00104","BSc Applied Mathematics","Eindhoven University of Technology","Eindhoven",date(2013,9,1),date(2016,6,30)),
    edu("EDU-008","CV-00105","MSc Information Security","Radboud University","Nijmegen",date(2012,9,1),date(2014,6,30)),
    edu("EDU-009","CV-00105","BSc Computer Science","Haagse Hogeschool","Den Haag",date(2009,9,1),date(2012,6,30)),
    edu("EDU-010","CV-00106","MSc Computer Science","University of Amsterdam","Amsterdam",date(2015,9,1),date(2017,6,30)),
    edu("EDU-011","CV-00106","BSc Software Development","Hogeschool van Amsterdam","Amsterdam",date(2012,9,1),date(2015,6,30)),
    edu("EDU-012","CV-00107","MSc Computer Science","University of Groningen","Groningen",date(2007,9,1),date(2009,6,30)),
    edu("EDU-013","CV-00107","BSc Computer Science","University of Groningen","Groningen",date(2004,9,1),date(2007,6,30)),
    edu("EDU-014","CV-00108","MSc Artificial Intelligence","VU Amsterdam","Amsterdam",date(2020,9,1),date(2022,6,30)),
    edu("EDU-015","CV-00108","BSc Data Science","University of Amsterdam","Amsterdam",date(2017,9,1),date(2020,6,30)),
    edu("EDU-016","CV-00109","BSc Software Engineering","Avans Hogeschool","Breda",date(2007,9,1),date(2011,6,30)),
    edu("EDU-017","CV-00110","MSc Business Information Management","Rotterdam School of Management","Rotterdam",date(2013,9,1),date(2015,6,30)),
    edu("EDU-018","CV-00110","BSc Information Management","Tilburg University","Tilburg",date(2010,9,1),date(2013,6,30)),
    edu("EDU-019","CV-00111","BSc Computer Science","University of Groningen","Groningen",date(2004,9,1),date(2008,6,30)),
    edu("EDU-020","CV-00112","MSc Software Engineering","Maastricht University","Maastricht",date(2017,9,1),date(2019,6,30)),
    edu("EDU-021","CV-00112","BSc Computer Science","Maastricht University","Maastricht",date(2014,9,1),date(2017,6,30)),
    edu("EDU-022","CV-00113","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2006,9,1),date(2010,6,30)),
    edu("EDU-023","CV-00114","MSc Data Engineering","TU Delft","Delft",date(2016,9,1),date(2018,6,30)),
    edu("EDU-024","CV-00114","BSc Applied Mathematics","Leiden University","Leiden",date(2013,9,1),date(2016,6,30)),
    edu("EDU-025","CV-00115","MSc Information Architecture","University of Amsterdam","Amsterdam",date(2007,9,1),date(2009,6,30)),
    edu("EDU-026","CV-00115","BSc Computer Science","Universitat Politècnica de Catalunya","Barcelona",date(2004,9,1),date(2007,6,30)),
    edu("EDU-027","CV-00116","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2012,9,1),date(2016,6,30)),
    edu("EDU-028","CV-00116","Frontend Bootcamp","Codaisseur","Amsterdam",date(2016,9,1),date(2016,12,31),"Intensive 12-week frontend development bootcamp."),
    edu("EDU-029","CV-00117","BSc Information Technology","Hogeschool Rotterdam","Rotterdam",date(2010,9,1),date(2014,6,30)),
    edu("EDU-030","CV-00118","MSc Web Technologies","Utrecht University","Utrecht",date(2019,9,1),date(2021,6,30)),
    edu("EDU-031","CV-00118","BSc Computer Science","Hogeschool Utrecht","Utrecht",date(2016,9,1),date(2019,6,30)),
    edu("EDU-032","CV-00119","BSc Software Engineering","Hogeschool van Amsterdam","Amsterdam",date(2008,9,1),date(2012,6,30)),
    edu("EDU-033","CV-00120","MSc Human-Computer Interaction","VU Amsterdam","Amsterdam",date(2016,9,1),date(2018,6,30)),
    edu("EDU-034","CV-00120","BSc Computer Science","University of Amsterdam","Amsterdam",date(2013,9,1),date(2016,6,30)),
    edu("EDU-035","CV-00121","BSc Computer Science","Fontys Hogeschool","Eindhoven",date(2007,9,1),date(2011,6,30)),
    edu("EDU-036","CV-00122","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2016,9,1),date(2020,6,30)),
    edu("EDU-037","CV-00123","BSc Information Technology","Hanze Hogeschool","Groningen",date(2009,9,1),date(2013,6,30)),
    edu("EDU-038","CV-00124","MSc Computer Science","TU Delft","Delft",date(2018,9,1),date(2020,6,30)),
    edu("EDU-039","CV-00124","BSc Software Engineering","Haagse Hogeschool","Den Haag",date(2015,9,1),date(2018,6,30)),
    edu("EDU-040","CV-00125","MSc Computer Science","Utrecht University","Utrecht",date(2009,9,1),date(2011,6,30)),
    edu("EDU-041","CV-00125","BSc Computer Science","Utrecht University","Utrecht",date(2006,9,1),date(2009,6,30)),
    edu("EDU-042","CV-00126","BSc Computer Science","University of Amsterdam","Amsterdam",date(2006,9,1),date(2010,6,30)),
    edu("EDU-043","CV-00127","MSc Data Science","Erasmus University","Rotterdam",date(2015,9,1),date(2017,6,30)),
    edu("EDU-044","CV-00127","BSc Mathematics","University of Amsterdam","Amsterdam",date(2012,9,1),date(2015,6,30)),
    edu("EDU-045","CV-00128","MSc Computer Science","University of Amsterdam","Amsterdam",date(2008,9,1),date(2010,6,30)),
    edu("EDU-046","CV-00128","BSc Computer Science","VU Amsterdam","Amsterdam",date(2005,9,1),date(2008,6,30)),
    edu("EDU-047","CV-00129","BSc Computer Science","Leiden University","Leiden",date(2013,9,1),date(2017,6,30)),
    edu("EDU-048","CV-00130","MSc Computer Science","TU Eindhoven","Eindhoven",date(2013,9,1),date(2015,6,30)),
    edu("EDU-049","CV-00130","BSc Computer Science","TU Eindhoven","Eindhoven",date(2010,9,1),date(2013,6,30)),
    edu("EDU-050","CV-00131","BSc Computer Science","University of Amsterdam","Amsterdam",date(2012,9,1),date(2016,6,30)),
    edu("EDU-051","CV-00132","BSc IT & Business","Avans Hogeschool","Breda",date(2007,9,1),date(2011,6,30)),
    edu("EDU-052","CV-00133","BSc Software Development","Hogeschool van Amsterdam","Amsterdam",date(2015,9,1),date(2019,6,30)),
    edu("EDU-053","CV-00134","MSc Computer Science","Radboud University","Nijmegen",date(2006,9,1),date(2008,6,30)),
    edu("EDU-054","CV-00134","BSc Computer Science","Radboud University","Nijmegen",date(2003,9,1),date(2006,6,30)),
    edu("EDU-055","CV-00135","BSc Computer Science","Fontys Hogeschool","Tilburg",date(2010,9,1),date(2014,6,30)),
    edu("EDU-056","CV-00136","MSc Computer Science","VU Amsterdam","Amsterdam",date(2012,9,1),date(2014,6,30)),
    edu("EDU-057","CV-00136","BSc Computer Science","VU Amsterdam","Amsterdam",date(2009,9,1),date(2012,6,30)),
    edu("EDU-058","CV-00137","BSc Information Technology","Hogeschool Rotterdam","Rotterdam",date(2012,9,1),date(2016,6,30)),
    edu("EDU-059","CV-00138","MSc Computer Science","TU Delft","Delft",date(2009,9,1),date(2011,6,30)),
    edu("EDU-060","CV-00138","BSc Computer Science","TU Delft","Delft",date(2006,9,1),date(2009,6,30)),
    edu("EDU-061","CV-00139","BSc Computer Science","Windesheim","Zwolle",date(2014,9,1),date(2018,6,30)),
    edu("EDU-062","CV-00140","MSc Computer Science","TU Delft","Delft",date(2007,9,1),date(2009,6,30)),
    edu("EDU-063","CV-00140","BSc Computer Science","Haagse Hogeschool","Den Haag",date(2004,9,1),date(2007,6,30)),
    edu("EDU-064","CV-00141","BSc Information Technology","Hogeschool Utrecht","Utrecht",date(2011,9,1),date(2015,6,30)),
    edu("EDU-065","CV-00142","BSc Computer Science","HAN University","Arnhem",date(2006,9,1),date(2010,6,30)),
    edu("EDU-066","CV-00143","MSc Computer Science","University of Amsterdam","Amsterdam",date(2013,9,1),date(2015,6,30)),
    edu("EDU-067","CV-00143","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2010,9,1),date(2013,6,30)),
    edu("EDU-068","CV-00144","MSc Computer Science","VU Amsterdam","Amsterdam",date(2008,9,1),date(2010,6,30)),
    edu("EDU-069","CV-00144","BSc Computer Science","VU Amsterdam","Amsterdam",date(2005,9,1),date(2008,6,30)),
    edu("EDU-070","CV-00145","BSc Information Technology","Hogeschool Rotterdam","Rotterdam",date(2012,9,1),date(2016,6,30)),
    edu("EDU-071","CV-00146","MSc Computer Science","University of Amsterdam","Amsterdam",date(2011,9,1),date(2013,6,30)),
    edu("EDU-072","CV-00146","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2008,9,1),date(2011,6,30)),
    edu("EDU-073","CV-00147","BSc Computer Science","Fontys Hogeschool","Eindhoven",date(2013,9,1),date(2017,6,30)),
    edu("EDU-074","CV-00148","MSc Computer Science","Utrecht University","Utrecht",date(2005,9,1),date(2007,6,30)),
    edu("EDU-075","CV-00148","BSc Computer Science","Utrecht University","Utrecht",date(2002,9,1),date(2005,6,30)),
    edu("EDU-076","CV-00149","BSc Information Technology","Hogeschool van Amsterdam","Amsterdam",date(2010,9,1),date(2014,6,30)),
    edu("EDU-077","CV-00150","BSc Computer Science","Hanze Hogeschool","Groningen",date(2008,9,1),date(2012,6,30)),
    edu("EDU-078","CV-00151","MSc Computer Science","TU Eindhoven","Eindhoven",date(2007,9,1),date(2009,6,30)),
    edu("EDU-079","CV-00151","BSc Computer Science","Fontys Hogeschool","Eindhoven",date(2004,9,1),date(2007,6,30)),
    edu("EDU-080","CV-00152","MSc Artificial Intelligence","University of Amsterdam","Amsterdam",date(2016,9,1),date(2018,6,30)),
    edu("EDU-081","CV-00152","BSc Computer Science","University of Amsterdam","Amsterdam",date(2013,9,1),date(2016,6,30)),
    edu("EDU-082","CV-00153","MSc Data Science","Erasmus University","Rotterdam",date(2013,9,1),date(2015,6,30)),
    edu("EDU-083","CV-00153","BSc Mathematics","Leiden University","Leiden",date(2010,9,1),date(2013,6,30)),
    edu("EDU-084","CV-00154","MSc Artificial Intelligence","Utrecht University","Utrecht",date(2019,9,1),date(2022,6,30)),
    edu("EDU-085","CV-00154","BSc Computer Science","Utrecht University","Utrecht",date(2016,9,1),date(2019,6,30)),
    edu("EDU-086","CV-00155","MSc Machine Learning","TU Delft","Delft",date(2011,9,1),date(2013,6,30)),
    edu("EDU-087","CV-00155","BSc Computer Science","TU Delft","Delft",date(2008,9,1),date(2011,6,30)),
    edu("EDU-088","CV-00156","MSc Statistics","Maastricht University","Maastricht",date(2017,9,1),date(2019,6,30)),
    edu("EDU-089","CV-00156","BSc Mathematics","Maastricht University","Maastricht",date(2014,9,1),date(2017,6,30)),
    edu("EDU-090","CV-00157","MSc Artificial Intelligence","VU Amsterdam","Amsterdam",date(2010,9,1),date(2012,6,30)),
    edu("EDU-091","CV-00157","BSc Computer Science","University of Amsterdam","Amsterdam",date(2007,9,1),date(2010,6,30)),
    edu("EDU-092","CV-00158","BSc Data Science","Radboud University","Nijmegen",date(2016,9,1),date(2020,6,30)),
    edu("EDU-093","CV-00159","MSc Computer Science","TU Delft","Delft",date(2008,9,1),date(2010,6,30)),
    edu("EDU-094","CV-00159","BSc Computer Science","Hogeschool Rotterdam","Rotterdam",date(2005,9,1),date(2008,6,30)),
    edu("EDU-095","CV-00160","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2013,9,1),date(2017,6,30)),
    edu("EDU-096","CV-00161","BSc Computer Science","Hogeschool Rotterdam","Rotterdam",date(2009,9,1),date(2013,6,30)),
    edu("EDU-097","CV-00162","BSc Information Technology","Hogeschool Utrecht","Utrecht",date(2012,9,1),date(2016,6,30)),
    edu("EDU-098","CV-00163","BSc Computer Science","HAN University","Arnhem",date(2006,9,1),date(2010,6,30)),
    edu("EDU-099","CV-00164","BSc Software Engineering","Hogeschool van Amsterdam","Amsterdam",date(2014,9,1),date(2018,6,30)),
    edu("EDU-100","CV-00165","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2007,9,1),date(2011,6,30)),
    edu("EDU-101","CV-00166","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2011,9,1),date(2015,6,30)),
    edu("EDU-102","CV-00167","BSc Information Technology","Hogeschool Rotterdam","Rotterdam",date(2008,9,1),date(2012,6,30)),
    edu("EDU-103","CV-00168","BSc Computer Science","Hogeschool Utrecht","Utrecht",date(2013,9,1),date(2017,6,30)),
    edu("EDU-104","CV-00169","BSc Software Engineering","Fontys Hogeschool","Eindhoven",date(2004,9,1),date(2008,6,30)),
    edu("EDU-105","CV-00170","BSc Software Development","Hogeschool van Amsterdam","Amsterdam",date(2016,9,1),date(2020,6,30)),
    edu("EDU-106","CV-00171","MSc Information Security","Radboud University","Nijmegen",date(2007,9,1),date(2009,6,30)),
    edu("EDU-107","CV-00171","BSc Computer Science","Radboud University","Nijmegen",date(2004,9,1),date(2007,6,30)),
    edu("EDU-108","CV-00172","BSc Computer Science","Hogeschool Rotterdam","Rotterdam",date(2010,9,1),date(2014,6,30)),
    edu("EDU-109","CV-00173","MSc Information Security","TU Delft","Delft",date(2010,9,1),date(2012,6,30)),
    edu("EDU-110","CV-00173","BSc Computer Science","Haagse Hogeschool","Den Haag",date(2007,9,1),date(2010,6,30)),
    edu("EDU-111","CV-00174","BSc Business IT & Management","Hogeschool van Amsterdam","Amsterdam",date(2014,9,1),date(2018,6,30)),
    edu("EDU-112","CV-00175","MSc Computer Science","Utrecht University","Utrecht",date(2005,9,1),date(2007,6,30)),
    edu("EDU-113","CV-00175","BSc Computer Science","Utrecht University","Utrecht",date(2002,9,1),date(2005,6,30)),
    edu("EDU-114","CV-00176","MSc Business Informatics","University of Amsterdam","Amsterdam",date(2002,9,1),date(2005,6,30)),
    edu("EDU-115","CV-00176","BSc Computer Science","VU Amsterdam","Amsterdam",date(1999,9,1),date(2002,6,30)),
    edu("EDU-116","CV-00177","BSc Information Technology","Hogeschool Rotterdam","Rotterdam",date(2002,9,1),date(2006,6,30)),
    edu("EDU-117","CV-00178","BSc Computer Science","Fontys Hogeschool","Eindhoven",date(2005,9,1),date(2009,6,30)),
    edu("EDU-118","CV-00179","MSc Business Information Management","Tilburg University","Tilburg",date(2003,9,1),date(2005,6,30)),
    edu("EDU-119","CV-00179","BSc Information Systems","Tilburg University","Tilburg",date(2000,9,1),date(2003,6,30)),
    edu("EDU-120","CV-00180","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2007,9,1),date(2011,6,30)),
    edu("EDU-121","CV-00181","MSc Business Administration","VU Amsterdam","Amsterdam",date(2004,9,1),date(2006,6,30)),
    edu("EDU-122","CV-00181","BSc Computer Science","VU Amsterdam","Amsterdam",date(2001,9,1),date(2004,6,30)),
    edu("EDU-123","CV-00182","BSc Information Technology","Hogeschool Rotterdam","Rotterdam",date(2005,9,1),date(2009,6,30)),
    edu("EDU-124","CV-00183","BSc Computer Science","Hogeschool Utrecht","Utrecht",date(2011,9,1),date(2015,6,30)),
    edu("EDU-125","CV-00184","MSc Information Management","Tilburg University","Tilburg",date(2001,9,1),date(2003,6,30)),
    edu("EDU-126","CV-00184","BSc Computer Science","Haagse Hogeschool","Den Haag",date(1998,9,1),date(2001,6,30)),
    edu("EDU-127","CV-00185","MSc Business Information Systems","University of Amsterdam","Amsterdam",date(2006,9,1),date(2008,6,30)),
    edu("EDU-128","CV-00185","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2003,9,1),date(2006,6,30)),
    edu("EDU-129","CV-00186","BSc Computer Science","VU Amsterdam","Amsterdam",date(1999,9,1),date(2003,6,30)),
    edu("EDU-130","CV-00187","MSc Business Intelligence","Erasmus University","Rotterdam",date(2012,9,1),date(2014,6,30)),
    edu("EDU-131","CV-00187","BSc Information Technology","Hogeschool Rotterdam","Rotterdam",date(2009,9,1),date(2012,6,30)),
    edu("EDU-132","CV-00188","BSc Computer Science","Hogeschool Utrecht","Utrecht",date(2004,9,1),date(2008,6,30)),
    edu("EDU-133","CV-00189","BSc Data Science","TU Eindhoven","Eindhoven",date(2012,9,1),date(2016,6,30)),
    edu("EDU-134","CV-00190","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2001,9,1),date(2005,6,30)),
    edu("EDU-135","CV-00191","BSc Network Engineering","Haagse Hogeschool","Den Haag",date(1998,9,1),date(2002,6,30)),
    edu("EDU-136","CV-00192","BSc Information Technology","Hogeschool Rotterdam","Rotterdam",date(2005,9,1),date(2009,6,30)),
    edu("EDU-137","CV-00193","BSc Computer Science","Hogeschool Utrecht","Utrecht",date(2000,9,1),date(2004,6,30)),
    edu("EDU-138","CV-00194","BSc Information Technology","Hogeschool van Amsterdam","Amsterdam",date(2007,9,1),date(2011,6,30)),
    edu("EDU-139","CV-00195","BSc Computer Science","Hogeschool Rotterdam","Rotterdam",date(2003,9,1),date(2007,6,30)),
    edu("EDU-140","CV-00196","BSc Business IT & Management","Hogeschool Utrecht","Utrecht",date(2010,9,1),date(2014,6,30)),
    edu("EDU-141","CV-00197","MSc Business Analysis","VU Amsterdam","Amsterdam",date(2006,9,1),date(2008,6,30)),
    edu("EDU-142","CV-00197","BSc Information Management","VU Amsterdam","Amsterdam",date(2003,9,1),date(2006,6,30)),
    edu("EDU-143","CV-00198","BSc Information Technology","Hogeschool Rotterdam","Rotterdam",date(2009,9,1),date(2013,6,30)),
    edu("EDU-144","CV-00199","MSc Computer Science","TU Delft","Delft",date(2001,9,1),date(2003,6,30)),
    edu("EDU-145","CV-00199","BSc Computer Science","Haagse Hogeschool","Den Haag",date(1998,9,1),date(2001,6,30)),
    edu("EDU-146","CV-00200","MSc Software Engineering","TU Delft","Delft",date(2010,9,1),date(2012,6,30)),
    edu("EDU-147","CV-00200","BSc Computer Science","Hogeschool van Amsterdam","Amsterdam",date(2007,9,1),date(2010,6,30)),
]

WORK_EXPERIENCE = [
    wx("WX-001","CV-00101","Senior Java Developer","ING Bank",date(2019,4,1),None,"Lead developer on core banking microservices platform. Migrated legacy monolith to Spring Boot microservices on AWS, reducing deployment time by 70%."),
    wx("WX-002","CV-00101","Java Developer","Rabobank",date(2015,1,1),date(2019,3,31),"Built RESTful APIs for payment processing. Worked in an Agile team of 8 developers."),
    wx("WX-003","CV-00101","Junior Java Developer","Capgemini",date(2012,7,1),date(2014,12,31),"Developed back-end services for government client projects."),
    wx("WX-004","CV-00102","Azure Cloud Engineer","Microsoft",date(2022,3,1),None,"Designed and implemented Azure Landing Zones for enterprise clients. Achieved AZ-900, AZ-104, and AZ-305 certifications."),
    wx("WX-005","CV-00102","Cloud Engineer","Sogeti",date(2020,7,1),date(2022,2,28),"Managed Azure infrastructure for retail and logistics clients. Implemented Infrastructure as Code with Terraform."),
    wx("WX-006","CV-00103","Senior DevOps Engineer","ASML",date(2018,6,1),None,"Architected and maintained CI/CD pipelines for 30+ development teams. Reduced release cycle from 2 weeks to 2 days. Led Kubernetes platform migration."),
    wx("WX-007","CV-00103","DevOps Engineer","Philips",date(2014,2,1),date(2018,5,31),"Implemented Docker containerisation strategy across healthcare software division."),
    wx("WX-008","CV-00103","Linux System Administrator","Atos",date(2010,9,1),date(2014,1,31),"Managed on-premise server infrastructure for financial sector clients."),
    wx("WX-009","CV-00104","Senior Data Engineer","Booking.com",date(2021,3,1),None,"Built real-time data pipelines processing 5M+ events per day using Kafka and Spark. Migrated data warehouse to Snowflake."),
    wx("WX-010","CV-00104","Data Engineer","ABN AMRO",date(2018,7,1),date(2021,2,28),"Designed dbt models for financial reporting. Built Airflow DAGs for regulatory reporting pipelines."),
    wx("WX-011","CV-00105","Senior Security Consultant","PwC Netherlands",date(2019,1,1),None,"Lead penetration tester and security auditor. Performed red team assessments for FTSE 100 clients. Certified CISSP and OSCP."),
    wx("WX-012","CV-00105","Security Analyst","Fox-IT",date(2014,8,1),date(2018,12,31),"Incident response and threat hunting. Investigated APT campaigns targeting Dutch financial sector."),
    wx("WX-013","CV-00106","Senior Full Stack Developer","Adyen",date(2020,1,1),None,"Built merchant dashboard features used by 50k+ businesses. Python/Django backend, React frontend. Improved page load time by 40%."),
    wx("WX-014","CV-00106","Full Stack Developer","TomTom",date(2017,7,1),date(2019,12,31),"Developed web interfaces for fleet management platform. Introduced TypeScript and improved test coverage from 30% to 80%."),
    wx("WX-015","CV-00107","Principal Solutions Architect","Amazon Web Services",date(2017,4,1),None,"Pre-sales and technical architecture for enterprise and startup clients across Benelux. Specialise in event-driven architectures and serverless. AWS Certified Solutions Architect Professional."),
    wx("WX-016","CV-00107","Cloud Architect","Accenture",date(2012,6,1),date(2017,3,31),"Designed multi-cloud architectures for insurance and banking clients."),
    wx("WX-017","CV-00107","Software Engineer","Exact Software",date(2009,7,1),date(2012,5,31),"Developed accounting and ERP modules."),
    wx("WX-018","CV-00108","Data Scientist","Ahold Delhaize",date(2022,9,1),None,"Built demand forecasting models reducing stock-outs by 15%. Developed NLP pipeline for customer feedback analysis using BERT."),
    wx("WX-019","CV-00108","Junior Data Scientist","Deloitte Analytics",date(2022,2,1),date(2022,8,31),"Graduate intake. Worked on predictive maintenance models for manufacturing client."),
    wx("WX-020","CV-00109","Lead .NET Developer","Exact Software",date(2018,3,1),None,"Technical lead for a squad of 6 developers building SaaS accounting platform. Migrated WinForms desktop app to cloud-native ASP.NET Core."),
    wx("WX-021","CV-00109","Senior .NET Developer","Cegeka",date(2014,1,1),date(2018,2,28),"Built enterprise resource planning integrations using C# and Azure Service Bus."),
    wx("WX-022","CV-00109",".NET Developer","Sogeti",date(2011,7,1),date(2013,12,31),"Government and healthcare projects using ASP.NET MVC and SQL Server."),
    wx("WX-023","CV-00110","IT Programme Manager","NS (Dutch Railways)",date(2019,9,1),None,"Managed €8M digital transformation programme across 5 workstreams. Implemented SAFe Agile across 12 delivery teams."),
    wx("WX-024","CV-00110","IT Project Manager","Capgemini",date(2015,3,1),date(2019,8,31),"Delivered ERP and CRM implementations for retail and logistics clients. Prince2 Practitioner certified."),
    wx("WX-025","CV-00111","Senior DevOps Engineer","Booking.com",date(2018,1,1),None,"Platform engineering for a team responsible for 1000+ microservices. Built internal developer portal. GitLab CI/Terraform for IaC."),
    wx("WX-026","CV-00111","DevOps / Linux Engineer","KPN",date(2012,4,1),date(2017,12,31),"Managed telco infrastructure and automated deployment of network provisioning services."),
    wx("WX-027","CV-00111","System Administrator","Imtech",date(2008,6,1),date(2012,3,31),"Linux and Windows server administration for manufacturing and utilities clients."),
    wx("WX-028","CV-00112","Senior Kotlin Developer","bol.com",date(2021,2,1),None,"Built event-driven microservices for the order fulfilment domain using Kotlin, Kafka, and PostgreSQL. Improved order processing throughput by 3x."),
    wx("WX-029","CV-00112","Java Developer","Mediaan",date(2019,7,1),date(2021,1,31),"Developed backend APIs for healthcare and retail clients using Java and Spring."),
    wx("WX-030","CV-00113","AWS Cloud Engineer","Coolblue",date(2018,9,1),None,"Designed and maintained AWS infrastructure serving 400k+ daily users. Cost optimisation saved €200k annually. AWS Certified DevOps Engineer Professional."),
    wx("WX-031","CV-00113","Cloud & Infrastructure Engineer","Atos",date(2014,5,1),date(2018,8,31),"Migrated on-premise workloads to AWS for banking and insurance clients."),
    wx("WX-032","CV-00113","Infrastructure Engineer","Dimension Data",date(2010,8,1),date(2014,4,30),"Managed VMware and Cisco infrastructure for enterprise clients."),
    wx("WX-033","CV-00114","Data Engineer","Heineken",date(2022,1,1),None,"Built and maintained supply chain analytics platform on GCP BigQuery. Developed dbt models for 20+ business domains."),
    wx("WX-034","CV-00114","Junior Data Engineer","Deloitte",date(2018,9,1),date(2021,12,31),"Designed Airflow pipelines for financial data reporting. SQL performance tuning for data warehouse."),
    wx("WX-035","CV-00115","Enterprise Solutions Architect","Capgemini",date(2016,3,1),None,"Lead architect for Azure and SAP integration projects in manufacturing and retail. TOGAF 9.2 certified. Managed architecture governance for programmes up to €15M."),
    wx("WX-036","CV-00115","Senior Integration Consultant","IBM",date(2011,6,1),date(2016,2,28),"SAP PI/PO middleware and API integration for logistics and utilities sector."),
    wx("WX-037","CV-00115","Software Developer","Indra",date(2009,1,1),date(2011,5,31),"Java development for government and telecom clients in Spain."),
    wx("WX-038","CV-00116","Senior React Developer","Adyen",date(2021,4,1),None,"Built checkout components used by millions globally. Led migration from class components to React hooks."),
    wx("WX-039","CV-00116","React Developer","Coolblue",date(2018,7,1),date(2021,3,31),"Developed product detail pages and checkout flows. A/B testing with 10M+ impressions."),
    wx("WX-040","CV-00116","Junior Frontend Developer","Capgemini",date(2016,9,1),date(2018,6,30),"Built Angular apps for government clients."),
    wx("WX-041","CV-00117","Senior Angular Developer","bol.com",date(2020,1,1),None,"Migrated legacy AngularJS to Angular 16. Improved bundle size by 45%."),
    wx("WX-042","CV-00117","Angular Developer","Rabobank",date(2016,9,1),date(2019,12,31),"Built customer self-service portal for retail banking."),
    wx("WX-043","CV-00118","Vue.js Developer","TomTom",date(2022,6,1),None,"Rebuilt fleet dashboard UI in Vue 3 / Nuxt. End-to-end tested with Cypress."),
    wx("WX-044","CV-00118","Frontend Developer","Wehkamp",date(2021,7,1),date(2022,5,31),"Developed product listing and search pages."),
    wx("WX-045","CV-00119","Lead Frontend Developer","Nationale-Nederlanden",date(2019,3,1),None,"Technical lead for 5-person frontend team. Migrated insurance platform to React/Redux."),
    wx("WX-046","CV-00119","React Developer","Accenture",date(2015,1,1),date(2019,2,28),"Delivered React frontends for banking and insurance clients."),
    wx("WX-047","CV-00120","Senior React Native Developer","ABN AMRO",date(2021,1,1),None,"Led mobile banking app rebuild in React Native. 4.7 star rating on App Store."),
    wx("WX-048","CV-00120","React Native Developer","Backbase",date(2018,7,1),date(2020,12,31),"Built cross-platform mobile banking components for international clients."),
    wx("WX-049","CV-00121","Frontend Tech Lead","Exact Software",date(2018,2,1),None,"Tech lead for Angular frontend of SaaS accounting platform. Mentored 4 junior developers."),
    wx("WX-050","CV-00121","Angular/Java Developer","Sogeti",date(2013,9,1),date(2018,1,31),"Full stack development for government digital services."),
    wx("WX-051","CV-00122","Frontend Developer","Booking.com",date(2023,3,1),None,"Built accessible UI components for hotel search. Web accessibility WCAG 2.1 AA certified."),
    wx("WX-052","CV-00123","Senior Vue.js Developer","NN Group",date(2019,9,1),None,"Rebuilt customer portal in Vue.js. Reduced page load time by 60%."),
    wx("WX-053","CV-00123","Frontend Developer","KPN",date(2015,1,1),date(2019,8,31),"Developed Angular apps for telecom customer portal."),
    wx("WX-054","CV-00124","Senior Frontend Developer","ING Bank",date(2022,2,1),None,"Built GraphQL-powered financial dashboard used by 500k+ customers."),
    wx("WX-055","CV-00124","React Developer","Capgemini",date(2020,7,1),date(2022,1,31),"Frontend development for digital transformation projects."),
    wx("WX-056","CV-00125","Principal Frontend Engineer","ASML",date(2017,9,1),None,"Defined frontend architecture for engineering tooling used by chip design teams globally."),
    wx("WX-057","CV-00125","Senior Frontend Developer","Philips",date(2013,7,1),date(2017,8,31),"Developed Angular-based medical device management dashboards."),
    wx("WX-058","CV-00126","Senior Node.js Developer","Takeaway.com (Just Eat)",date(2020,3,1),None,"Built order routing and restaurant APIs handling 2M+ daily transactions."),
    wx("WX-059","CV-00126","Node.js Developer","NS (Dutch Railways)",date(2016,9,1),date(2020,2,28),"Developed journey planning APIs. Migrated monolith to microservices."),
    wx("WX-060","CV-00127","Senior Python Developer","Coolblue",date(2021,6,1),None,"Built recommendation engine and pricing APIs with FastAPI. Managed async task processing with Celery."),
    wx("WX-061","CV-00127","Python Developer","Deloitte",date(2017,7,1),date(2021,5,31),"Data pipelines and REST APIs for financial analytics clients."),
    wx("WX-062","CV-00128","Principal Go Engineer","TomTom",date(2018,4,1),None,"Built high-throughput location services in Go. 99.99% uptime SLA. gRPC APIs serving 50M+ requests/day."),
    wx("WX-063","CV-00128","Senior Go Developer","Booking.com",date(2014,7,1),date(2018,3,31),"Developed pricing and availability microservices."),
    wx("WX-064","CV-00129","Python Developer","Ahold Delhaize",date(2023,1,1),None,"Built Django REST APIs for supply chain management platform."),
    wx("WX-065","CV-00130","Rust Systems Engineer","Siemens",date(2021,9,1),None,"Built WebAssembly modules for industrial IoT dashboard. Memory-safe systems programming."),
    wx("WX-066","CV-00130","Senior Backend Developer","ASML",date(2017,7,1),date(2021,8,31),"Designed gRPC services for semiconductor manufacturing automation."),
    wx("WX-067","CV-00131","Senior Ruby on Rails Developer","Catawiki",date(2019,4,1),None,"Built auction bidding engine and payment processing APIs. Ruby on Rails with PostgreSQL."),
    wx("WX-068","CV-00131","Ruby Developer","Springest",date(2016,9,1),date(2019,3,31),"E-commerce and marketplace backend development."),
    wx("WX-069","CV-00132","Lead PHP Developer","Transip",date(2018,6,1),None,"Led backend team building cloud hosting control panel. Laravel, Vue.js, MySQL."),
    wx("WX-070","CV-00132","PHP Developer","Byte (hosting)",date(2013,7,1),date(2018,5,31),"Built PHP applications for domain registration and hosting management."),
    wx("WX-071","CV-00133","Node.js Developer","Picnic",date(2023,4,1),None,"Built delivery logistics APIs with Node.js and MongoDB. GraphQL interface for mobile apps."),
    wx("WX-072","CV-00134","Senior Go Engineer","Philips",date(2017,1,1),None,"Designed event-driven backend for medical data streaming. HIPAA-compliant architecture."),
    wx("WX-073","CV-00134","Backend Developer","Atos",date(2012,7,1),date(2016,12,31),"Built REST APIs and integration services for healthcare and government."),
    wx("WX-074","CV-00135","Senior Python Developer","CBRE",date(2020,9,1),None,"Built Elasticsearch-powered property search APIs. Flask, SQLAlchemy, Docker."),
    wx("WX-075","CV-00135","Python Developer","ING Bank",date(2016,7,1),date(2020,8,31),"Developed risk calculation services with Python and PostgreSQL."),
    wx("WX-076","CV-00136","Senior GCP Data Engineer","Randstad",date(2020,2,1),None,"Built Dataflow pipelines processing 10M+ records/day on GCP. Terraform IaC for all infrastructure."),
    wx("WX-077","CV-00136","GCP Cloud Engineer","Capgemini",date(2016,7,1),date(2020,1,31),"Migrated on-premise data warehouse to BigQuery for retail clients."),
    wx("WX-078","CV-00137","Azure DevOps Engineer","NS (Dutch Railways)",date(2021,9,1),None,"Automated infrastructure deployments with Azure DevOps pipelines and Kubernetes."),
    wx("WX-079","CV-00137","Cloud Engineer","Sogeti",date(2018,6,1),date(2021,8,31),"Azure cloud migrations for manufacturing and logistics clients."),
    wx("WX-080","CV-00138","Multi-Cloud Architect","Deloitte",date(2018,1,1),None,"FinOps and multi-cloud strategy for Fortune 500 clients. Reduced cloud spend by 30%."),
    wx("WX-081","CV-00138","Cloud Engineer","Atos",date(2013,7,1),date(2017,12,31),"AWS and Azure infrastructure for banking and insurance."),
    wx("WX-082","CV-00139","AWS Cloud Engineer","Achmea",date(2023,3,1),None,"Designed serverless insurance claims platform on AWS Lambda and API Gateway."),
    wx("WX-083","CV-00140","GCP Cloud Architect","Google (contractor)",date(2019,6,1),None,"Designed Anthos-based hybrid cloud solutions for enterprise clients in Benelux."),
    wx("WX-084","CV-00140","Cloud Engineer","Capgemini",date(2013,7,1),date(2019,5,31),"GCP and AWS infrastructure automation for telecom clients."),
    wx("WX-085","CV-00141","Azure Cloud Engineer","ABN AMRO",date(2020,4,1),None,"Managed Azure Landing Zone and DevOps pipelines for 200+ developers."),
    wx("WX-086","CV-00141","Cloud Engineer","Cegeka",date(2017,7,1),date(2020,3,31),"Azure infrastructure and migrations for healthcare and government."),
    wx("WX-087","CV-00142","Senior AWS Engineer","Nationale-Nederlanden",date(2019,1,1),None,"Architected ECS Fargate platform for 50+ microservices. Built observability stack with Datadog."),
    wx("WX-088","CV-00142","AWS Engineer","Imtech",date(2014,9,1),date(2018,12,31),"Managed AWS infrastructure for utilities and industrial clients."),
    wx("WX-089","CV-00143","Senior GCP Engineer","Booking.com",date(2020,3,1),None,"Built Kubernetes-native data platform on GCP. Prometheus/Grafana observability stack."),
    wx("WX-090","CV-00143","Cloud Engineer","Sogeti",date(2017,7,1),date(2020,2,28),"GCP and AWS infrastructure for retail and logistics clients."),
    wx("WX-091","CV-00144","Senior SRE","Adyen",date(2018,9,1),None,"Built reliability framework for payments platform processing €300B/year. SLO/SLI governance across 80+ services."),
    wx("WX-092","CV-00144","DevOps Engineer","ING Bank",date(2014,1,1),date(2018,8,31),"CI/CD pipelines and container platform for digital banking services."),
    wx("WX-093","CV-00145","DevOps Engineer","bol.com",date(2021,4,1),None,"GitOps implementation with ArgoCD and Flux for 200+ microservices."),
    wx("WX-094","CV-00145","DevOps Engineer","Backbase",date(2018,7,1),date(2021,3,31),"Built Kubernetes platform for mobile banking deployments."),
    wx("WX-095","CV-00146","Platform Engineer","Booking.com",date(2019,6,1),None,"Built internal developer platform with Backstage. GitHub Actions CI/CD for 1000+ repositories."),
    wx("WX-096","CV-00146","DevOps Engineer","TomTom",date(2015,7,1),date(2019,5,31),"CI/CD automation and Terraform IaC for location services infrastructure."),
    wx("WX-097","CV-00147","DevOps Engineer","ASML",date(2022,9,1),None,"Jenkins and Ansible automation for semiconductor equipment software deployments."),
    wx("WX-098","CV-00148","Principal SRE","Rabobank",date(2016,3,1),None,"Led SRE practice for core banking platform. Chaos engineering and game days. Reduced MTTR by 60%."),
    wx("WX-099","CV-00148","SRE / DevOps Engineer","Accenture",date(2009,7,1),date(2016,2,28),"Reliability engineering for banking and telecom clients."),
    wx("WX-100","CV-00149","Azure DevOps Engineer","Randstad",date(2020,6,1),None,"Azure Kubernetes Service platform for 100+ applications. Python automation tooling."),
    wx("WX-101","CV-00149","DevOps Engineer","Sogeti",date(2016,7,1),date(2020,5,31),"CI/CD and infrastructure automation for manufacturing clients."),
    wx("WX-102","CV-00150","DevOps Engineer","Heineken",date(2019,4,1),None,"GitLab CI/CD and Docker containerisation for supply chain applications."),
    wx("WX-103","CV-00150","DevOps Engineer","Cegeka",date(2014,7,1),date(2019,3,31),"Infrastructure automation for healthcare and insurance clients."),
    wx("WX-104","CV-00151","Senior SRE","Exact Software",date(2017,9,1),None,"SRE lead for SaaS accounting platform. OpenTelemetry observability rollout across 30 services."),
    wx("WX-105","CV-00151","DevOps Engineer","Philips",date(2012,7,1),date(2017,8,31),"CI/CD and cloud automation for healthcare software division."),
    wx("WX-106","CV-00152","ML Engineer","Ahold Delhaize",date(2021,4,1),None,"Deployed demand forecasting model to production with MLflow and Kubeflow. 20% reduction in food waste."),
    wx("WX-107","CV-00152","Data Scientist","Deloitte Analytics",date(2018,7,1),date(2021,3,31),"Predictive analytics and NLP for retail and insurance clients."),
    wx("WX-108","CV-00153","Senior Data Scientist","ING Bank",date(2020,3,1),None,"Built credit risk scoring models. XGBoost-based PD models used in production for €1B+ loan portfolio."),
    wx("WX-109","CV-00153","Data Scientist","ABN AMRO",date(2017,7,1),date(2020,2,28),"Fraud detection and AML transaction monitoring models."),
    wx("WX-110","CV-00154","NLP / LLM Engineer","Booking.com",date(2023,6,1),None,"Built RAG-based customer support system using LangChain and OpenAI. Deflected 35% of support tickets."),
    wx("WX-111","CV-00155","Senior ML Engineer","Coolblue",date(2019,3,1),None,"Built personalisation and recommendation models on Vertex AI. Increased conversion by 8%."),
    wx("WX-112","CV-00155","ML Engineer","Accenture AI",date(2015,7,1),date(2019,2,28),"Computer vision and NLP solutions for retail and manufacturing clients."),
    wx("WX-113","CV-00156","Data Scientist","Heineken",date(2022,1,1),None,"A/B testing framework and consumer behaviour analytics. Tableau dashboards for marketing analytics."),
    wx("WX-114","CV-00156","Data Analyst","Achmea",date(2019,7,1),date(2021,12,31),"Statistical analysis and R modelling for insurance pricing."),
    wx("WX-115","CV-00157","LLM / Generative AI Engineer","Adyen",date(2022,9,1),None,"Fine-tuned LLMs for merchant support automation. RAG pipeline over 500k+ help articles."),
    wx("WX-116","CV-00157","ML Engineer","ING Bank",date(2017,4,1),date(2022,8,31),"NLP-based document classification and risk scoring models."),
    wx("WX-117","CV-00158","Junior Data Scientist","Nationale-Nederlanden",date(2023,9,1),None,"Customer churn prediction models and data visualisation."),
    wx("WX-118","CV-00159","Principal ML Engineer","bol.com",date(2016,3,1),None,"Built real-time recommendation engine serving 12M+ users. Kafka-based feature store."),
    wx("WX-119","CV-00159","Senior Data Scientist","Takeaway.com",date(2012,7,1),date(2016,2,28),"Demand forecasting and delivery time prediction models."),
    wx("WX-120","CV-00160","Senior iOS Developer","ABN AMRO",date(2020,9,1),None,"Led iOS development for retail banking app with 2M+ active users. SwiftUI migration."),
    wx("WX-121","CV-00160","iOS Developer","ING Bank",date(2017,7,1),date(2020,8,31),"Developed iOS banking app features and payments UI."),
    wx("WX-122","CV-00161","Senior Android Developer","Rabobank",date(2019,5,1),None,"Built Kotlin/Jetpack Compose Android banking app. Biometric authentication and payment features."),
    wx("WX-123","CV-00161","Android Developer","NS (Dutch Railways)",date(2015,7,1),date(2019,4,30),"Developed NS journey planner Android app. 500k+ downloads."),
    wx("WX-124","CV-00162","React Native Developer","Backbase",date(2021,3,1),None,"Built white-label mobile banking SDK in React Native used by 20+ banks."),
    wx("WX-125","CV-00162","Mobile Developer","Capgemini",date(2018,7,1),date(2021,2,28),"iOS and Android development for retail and logistics clients."),
    wx("WX-126","CV-00163","Senior Flutter Developer","PostNL",date(2020,6,1),None,"Built Flutter delivery tracking app for iOS and Android. 1M+ downloads, 4.6 star rating."),
    wx("WX-127","CV-00163","Mobile Developer","Sogeti",date(2014,7,1),date(2020,5,31),"iOS and Android development for government and healthcare clients."),
    wx("WX-128","CV-00164","iOS Developer","Booking.com",date(2021,9,1),None,"Developed hotel booking and payments features in Swift. ARKit integration for room previews."),
    wx("WX-129","CV-00165","Senior Android Developer","Coolblue",date(2019,1,1),None,"Built shopping app for Android with 2M+ users. MVVM, Dagger, Coroutines."),
    wx("WX-130","CV-00165","Android Developer","MediaMarkt",date(2014,7,1),date(2018,12,31),"E-commerce Android app development. Push notifications and personalisation features."),
    wx("WX-131","CV-00166","Senior SDET","Adyen",date(2020,6,1),None,"Built Selenium and Playwright test frameworks for payment checkout. 90% automated regression coverage."),
    wx("WX-132","CV-00166","Test Automation Engineer","Rabobank",date(2017,7,1),date(2020,5,31),"BDD test automation with Cucumber and Python for digital banking."),
    wx("WX-133","CV-00167","Performance Test Engineer","NS (Dutch Railways)",date(2019,3,1),None,"JMeter and k6 performance testing for journey planning APIs. Identified 40% latency regression."),
    wx("WX-134","CV-00167","Test Engineer","Sogeti",date(2014,7,1),date(2019,2,28),"Performance and functional testing for government and finance clients."),
    wx("WX-135","CV-00168","SDET","ABN AMRO",date(2022,4,1),None,"Playwright E2E test suite for online banking. Integrated into GitHub Actions CI/CD."),
    wx("WX-136","CV-00169","Test Automation Engineer","ASML",date(2019,7,1),None,"Robot Framework test automation for semiconductor manufacturing software."),
    wx("WX-137","CV-00169","Senior Test Engineer","Capgemini",date(2011,7,1),date(2019,6,30),"Test automation and performance testing for banking and insurance clients."),
    wx("WX-138","CV-00170","Junior Test Engineer","ING Bank",date(2024,1,1),None,"Manual and exploratory testing for digital banking features. JIRA and Zephyr."),
    wx("WX-139","CV-00171","SOC Lead Analyst","Rabobank",date(2017,3,1),None,"Led threat hunting team. Reduced mean time to detect (MTTD) from 18 hours to 3 hours with Splunk."),
    wx("WX-140","CV-00171","Security Analyst","Fox-IT",date(2012,7,1),date(2017,2,28),"Incident response and digital forensics for banking and government clients."),
    wx("WX-141","CV-00172","Senior Penetration Tester","Securify",date(2020,3,1),None,"Web application and API pentesting. OWASP Top 10, HackTheBox Pro Hacker rank."),
    wx("WX-142","CV-00172","Security Consultant","Deloitte Cyber",date(2016,7,1),date(2020,2,28),"Red team assessments and security architecture reviews."),
    wx("WX-143","CV-00173","Cloud Security Architect","ING Bank",date(2019,9,1),None,"Zero Trust architecture and AWS security guardrails for cloud migration programme."),
    wx("WX-144","CV-00173","Security Engineer","Sogeti",date(2014,7,1),date(2019,8,31),"Cloud security assessments for banking and insurance clients."),
    wx("WX-145","CV-00174","GRC Analyst","ABN AMRO",date(2023,3,1),None,"ISO 27001 and DORA compliance. Maintained risk register for IT organisation."),
    wx("WX-146","CV-00175","AppSec Lead","Booking.com",date(2016,9,1),None,"Defined application security standards. SAST/DAST tooling rollout across 500+ repositories."),
    wx("WX-147","CV-00175","Security Engineer","Accenture",date(2010,7,1),date(2016,8,31),"DevSecOps implementation and application security reviews."),
    wx("WX-148","CV-00176","SAP S/4HANA Programme Lead","Shell",date(2018,1,1),None,"Led €20M SAP S/4HANA migration for energy trading division. 500+ users impacted."),
    wx("WX-149","CV-00176","SAP FI/CO Consultant","Accenture",date(2009,7,1),date(2017,12,31),"SAP finance implementations for oil, gas, and manufacturing clients."),
    wx("WX-150","CV-00177","SAP MM/WM Consultant","Capgemini",date(2015,3,1),None,"SAP S/4HANA supply chain implementations for logistics and retail."),
    wx("WX-151","CV-00177","SAP Consultant","IBM",date(2009,7,1),date(2015,2,28),"SAP implementations for FMCG and manufacturing clients."),
    wx("WX-152","CV-00178","Oracle ERP Consultant","Deloitte",date(2017,4,1),None,"Oracle Cloud ERP implementations for finance and supply chain. Oracle Integration Cloud."),
    wx("WX-153","CV-00178","Oracle Consultant","Sogeti",date(2011,7,1),date(2017,3,31),"Oracle E-Business Suite implementations for public sector."),
    wx("WX-154","CV-00179","SAP BW/4HANA Architect","NS (Dutch Railways)",date(2016,9,1),None,"Designed enterprise analytics platform on SAP BW/4HANA and SAC for 200+ reports."),
    wx("WX-155","CV-00179","SAP BI Consultant","Atos",date(2010,7,1),date(2016,8,31),"SAP BW reporting implementations for manufacturing and utilities."),
    wx("WX-156","CV-00180","SAP CRM Consultant","Heineken",date(2019,3,1),None,"SAP C4C and S/4HANA SD implementation for global sales operations."),
    wx("WX-157","CV-00180","SAP Developer","Accenture",date(2013,7,1),date(2019,2,28),"ABAP development and CRM customisations for FMCG clients."),
    wx("WX-158","CV-00181","Interim IT Director","Randstad",date(2020,1,1),None,"Interim CTO role during digital transformation. Managed €15M IT budget and team of 45."),
    wx("WX-159","CV-00181","IT Manager","Achmea",date(2014,3,1),date(2019,12,31),"Managed IT governance and vendor portfolio for insurance division."),
    wx("WX-160","CV-00182","IT Programme Manager","PostNL",date(2021,6,1),None,"Delivered €12M SAFe digital transformation programme. 12 Agile teams across 3 value streams."),
    wx("WX-161","CV-00182","Project Manager","Sogeti",date(2014,7,1),date(2021,5,31),"IT project delivery for logistics, banking, and public sector clients."),
    wx("WX-162","CV-00183","Senior Scrum Master / Agile Coach","bol.com",date(2020,9,1),None,"Coached 4 cross-functional teams using LeSS. Facilitated PI Planning for 80+ people."),
    wx("WX-163","CV-00183","Scrum Master","Rabobank",date(2017,7,1),date(2020,8,31),"Scrum Master for digital banking squads. Agile transformations."),
    wx("WX-164","CV-00184","ITSM Manager","KPN",date(2009,3,1),None,"IT service management lead. ITIL v4 Expert. Managed SIAM model with 8 external suppliers."),
    wx("WX-165","CV-00185","Senior Product Manager","Adyen",date(2019,9,1),None,"Product owner for merchant onboarding platform. Grew NPS from 38 to 67 in 2 years."),
    wx("WX-166","CV-00185","Product Manager","TomTom",date(2013,7,1),date(2019,8,31),"B2B SaaS product management for fleet and navigation API products."),
    wx("WX-167","CV-00186","Senior Oracle DBA","Shell",date(2015,3,1),None,"Managed 50+ Oracle databases for energy trading. RAC and Data Guard configurations."),
    wx("WX-168","CV-00186","Oracle DBA","Atos",date(2007,7,1),date(2015,2,28),"Database administration for government and financial sector clients."),
    wx("WX-169","CV-00187","Senior BI Developer","Achmea",date(2019,4,1),None,"Built Power BI reports for claims and risk management. Azure Synapse Analytics data warehouse."),
    wx("WX-170","CV-00187","BI Developer","Capgemini",date(2015,7,1),date(2019,3,31),"SSAS cubes and SQL Server SSRS reporting for insurance and banking."),
    wx("WX-171","CV-00188","SQL Server DBA","ING Bank",date(2016,1,1),None,"Managed 200+ SQL Server instances. Always On AG, SSIS/SSRS, Azure SQL migration."),
    wx("WX-172","CV-00188","SQL Server DBA","Sogeti",date(2010,7,1),date(2015,12,31),"SQL Server database management for government and healthcare clients."),
    wx("WX-173","CV-00189","Analytics Engineer","Booking.com",date(2022,9,1),None,"Built dbt models and Looker dashboards for 20+ business domains on BigQuery."),
    wx("WX-174","CV-00190","Senior NoSQL Architect","Takeaway.com",date(2017,6,1),None,"Designed MongoDB and Cassandra schemas for order management and customer data."),
    wx("WX-175","CV-00190","Database Engineer","Capgemini",date(2010,7,1),date(2017,5,31),"Database design and optimisation for retail and logistics clients."),
    wx("WX-176","CV-00191","Senior Network Engineer","KPN",date(2014,3,1),None,"Designed SD-WAN rollout for 500+ enterprise branch offices. Cisco and Fortinet infrastructure."),
    wx("WX-177","CV-00191","Network Engineer","Colt Technology",date(2006,7,1),date(2014,2,28),"MPLS network design and BGP routing for enterprise clients."),
    wx("WX-178","CV-00192","Network Security Engineer","Rabobank",date(2018,6,1),None,"Palo Alto Next-Gen Firewall and Zero Trust network architecture. Micro-segmentation rollout."),
    wx("WX-179","CV-00192","Network Engineer","Dimension Data",date(2012,7,1),date(2018,5,31),"Network infrastructure projects for banking and healthcare clients."),
    wx("WX-180","CV-00193","Senior VMware Architect","Shell",date(2015,9,1),None,"vSphere and vSAN architecture for 10,000+ VM environment. NSX-T micro-segmentation."),
    wx("WX-181","CV-00193","Infrastructure Engineer","HP Enterprise",date(2008,7,1),date(2015,8,31),"VMware and Cisco UCS infrastructure for enterprise clients."),
    wx("WX-182","CV-00194","Senior Salesforce Developer","Philips",date(2019,3,1),None,"Built custom Salesforce CPQ and Service Cloud integrations using Apex and LWC."),
    wx("WX-183","CV-00194","Salesforce Developer","Capgemini",date(2015,7,1),date(2019,2,28),"Salesforce Sales Cloud implementations for manufacturing and healthcare."),
    wx("WX-184","CV-00195","Senior ServiceNow Developer","Rabobank",date(2019,1,1),None,"Built ITSM and ITOM modules in ServiceNow. Custom Flow Designer workflows and REST integrations."),
    wx("WX-185","CV-00195","ServiceNow Developer","Cegeka",date(2014,7,1),date(2018,12,31),"ServiceNow ITSM implementations for banking and insurance."),
    wx("WX-186","CV-00196","Salesforce Marketing Cloud Consultant","Heineken",date(2020,9,1),None,"Built multi-channel marketing journeys in Marketing Cloud for 40 global markets."),
    wx("WX-187","CV-00196","Salesforce Consultant","Accenture",date(2016,7,1),date(2020,8,31),"Salesforce CRM and CPQ implementations for FMCG and retail clients."),
    wx("WX-188","CV-00197","Senior Business Analyst","ABN AMRO",date(2018,4,1),None,"Business analysis for digital mortgage and lending platform. BPMN process models and requirements."),
    wx("WX-189","CV-00197","Business Analyst","Sogeti",date(2011,7,1),date(2018,3,31),"Requirements engineering and process analysis for banking and government."),
    wx("WX-190","CV-00198","Business Analyst","ING Bank",date(2020,3,1),None,"Requirements engineering for customer onboarding and KYC platform. JIRA and Confluence."),
    wx("WX-191","CV-00198","Junior Business Analyst","Capgemini",date(2016,7,1),date(2020,2,28),"Business and functional analysis for digital transformation projects."),
    wx("WX-192","CV-00199","Enterprise Architect","NS (Dutch Railways)",date(2012,9,1),None,"TOGAF-based enterprise architecture governance for €200M+ IT landscape. Archimate modelling."),
    wx("WX-193","CV-00199","IT Architect","Atos",date(2007,7,1),date(2012,8,31),"IT architecture for government and public sector clients."),
    wx("WX-194","CV-00200","Solution Architect","Adyen",date(2019,6,1),None,"Domain-driven design and API-first architecture for payment platform. Azure microservices."),
    wx("WX-195","CV-00200","Solution Architect","Accenture",date(2014,7,1),date(2019,5,31),"Cloud architecture and DDD for banking and fintech clients."),
]

GDPR = [
    gdpr("CV-00101","Recruitment processing","Consent",date(2024,3,1),date(2024,3,2),"Email"),
    gdpr("CV-00102","Recruitment processing","Consent",date(2026,2,19),date(2026,2,19),"Portal"),
    gdpr("CV-00103","Recruitment processing","Legitimate interest",date(2024,11,8),date(2024,11,10),"Email"),
    gdpr("CV-00104","Recruitment processing","Consent",date(2024,6,22),date(2024,6,23),"LinkedIn"),
    gdpr("CV-00105","Recruitment processing","Consent",date(2025,1,15),date(2025,1,16),"Email"),
]

CORPORATIONS = [
    ClientCorporation(external_id="CC-001", name="ING Group", main_phone="+31 20 563 9111", company_url="www.ing.nl", address_line1="Bijlmerdreef 106", address_city="Amsterdam", address_zip="1102 CT", address_state="Noord-Holland", address_country_id="NL", status="Active", company_description="Dutch multinational banking and financial services corporation.", business_sector_list="Banking,Finance"),
    ClientCorporation(external_id="CC-002", name="ASML", main_phone="+31 40 268 3000", company_url="www.asml.com", address_line1="De Run 6501", address_city="Veldhoven", address_zip="5504 DR", address_state="Noord-Brabant", address_country_id="NL", status="Active", company_description="World's leading manufacturer of chip-making equipment.", business_sector_list="Semiconductor,Technology"),
    ClientCorporation(external_id="CC-003", name="Booking.com", main_phone="+31 20 715 0000", company_url="www.booking.com", address_line1="Herengracht 597", address_city="Amsterdam", address_zip="1017 CE", address_state="Noord-Holland", address_country_id="NL", status="Active", company_description="Global online travel and accommodation platform.", business_sector_list="Technology,Travel"),
    ClientCorporation(external_id="CC-004", name="Adyen", main_phone="+31 20 240 1240", company_url="www.adyen.com", address_line1="Simon Carmiggeltstraat 6", address_city="Amsterdam", address_zip="1011 DJ", address_state="Noord-Holland", address_country_id="NL", status="Active", company_description="Global payment technology company.", business_sector_list="Fintech,Payments"),
    ClientCorporation(external_id="CC-005", name="Philips", main_phone="+31 20 597 7777", company_url="www.philips.com", address_line1="Breitner Center, Amstelplein 2", address_city="Amsterdam", address_zip="1096 BC", address_state="Noord-Holland", address_country_id="NL", status="Active", company_description="Health technology company focused on diagnostics and connected care.", business_sector_list="Healthcare,Technology"),
]

CONTACTS = [
    ClientContact(external_id="CTK-001", client_corporation_external_id="CC-001", first_name="Mark", last_name="Hendriksen", title="Head of IT Recruitment", email1="m.hendriksen@ing.nl", phone="+31 6 11223344", address_city="Amsterdam", status="Active"),
    ClientContact(external_id="CTK-002", client_corporation_external_id="CC-002", first_name="Julia", last_name="Vermeulen", title="Senior Technical Recruiter", email1="j.vermeulen@asml.com", phone="+31 6 55667788", address_city="Veldhoven", status="Active"),
    ClientContact(external_id="CTK-003", client_corporation_external_id="CC-003", first_name="David", last_name="Chen", title="Engineering Manager", email1="d.chen@booking.com", phone="+31 6 99001122", address_city="Amsterdam", status="Active"),
    ClientContact(external_id="CTK-004", client_corporation_external_id="CC-004", first_name="Anna", last_name="de Boer", title="Tech Lead", email1="a.deboer@adyen.com", phone="+31 6 33445566", address_city="Amsterdam", status="Active"),
    ClientContact(external_id="CTK-005", client_corporation_external_id="CC-005", first_name="Peter", last_name="Visser", title="IT Director", email1="p.visser@philips.com", phone="+31 6 77889900", address_city="Amsterdam", status="Active"),
]

def _generate_bulk(
    start_num: int,
    count: int,
) -> Tuple:

    rng = random.Random(42)

    first_names_m = [
        "Adam","Alex","Alexander","Alexei","André","Arjan","Arno","Bart","Ben","Boris",
        "Bram","Chris","Daniel","David","Dennis","Dirk","Dylan","Emil","Erwin","Ethan",
        "Ewout","Florian","Frits","George","Glen","Guido","Hans","Henrik","Hugo","Ivan",
        "Jack","Jan","Jens","Jerome","Jesse","Jim","Job","Joel","Johan","Jonas",
        "Jonathan","Joost","Jordan","Jos","Julien","Kevin","Lars","Luca","Luuk","Maarten",
        "Marc","Martijn","Mathias","Max","Michael","Michiel","Milan","Mohamed","Nathan","Nico",
        "Niels","Noah","Noel","Oliver","Oscar","Patrick","Paul","Peter","Philip","Piet",
        "Pieter","Raoul","Remco","René","Rick","Robert","Robin","Roelof","Roland","Ruben",
        "Rutger","Ryan","Sam","Sander","Sebastian","Simon","Stefan","Stef","Stephan","Steven",
        "Thomas","Thijs","Tim","Tom","Victor","Vincent","Wim","Wouter","Xander","Yannick",
    ]
    first_names_f = [
        "Aafke","Aimée","Alicia","Alina","Amber","Amy","Anita","Anna","Annelies","Annemieke",
        "Anouk","Astrid","Bianca","Carla","Carmen","Charlotte","Chloé","Claudia","Dana","Deborah",
        "Denise","Diana","Elena","Elise","Elke","Ellen","Emma","Esther","Eva","Eveline",
        "Fatima","Femke","Fleur","Floor","Floortje","Gabrielle","Gina","Hannah","Hanna","Ilse",
        "Inge","Iris","Isabelle","Jana","Jasmine","Jennifer","Jessica","Julie","Karen","Katja",
        "Laura","Layla","Lena","Lies","Linde","Lisa","Loes","Lotte","Louisa","Luna",
        "Lydia","Maaike","Manon","Maria","Mariam","Marieke","Marissa","Maud","Maya","Mia",
        "Miriam","Monique","Nadia","Nathalie","Nicole","Nikki","Noor","Olivia","Patricia","Petra",
        "Roos","Rosa","Sabine","Sara","Sarah","Silke","Simone","Sofie","Sophie","Stephanie",
        "Suse","Suzanne","Tessa","Tineke","Vera","Victoria","Wendy","Yasmine","Yvonne","Zoë",
    ]
    last_names = [
        "Aalbers","Aarts","Appel","Bakker","Barendregt","Beek","Berg","Berger","Blom","Boer",
        "Bos","Bosch","Bosman","Brandt","Broek","Brouwer","Claes","Claessen","Coenen","Cools",
        "Dam","Dekker","Dijkstra","Driessen","Dijk","Engel","Franken","Franssen","Geerts","Gerritsen",
        "Groot","Haan","Hendriks","Henssen","Hermans","Hoek","Hoffman","Hout","Jacobs","Jansen",
        "Jong","Jongen","Klaassen","Klein","Knol","Konings","Kooij","Kramer","Kuiper","Laan",
        "Leeuw","Linden","Looijen","Maassen","Manders","Martens","Meijer","Molenaar","Mulder","Nijs",
        "Nijssen","Oosterom","Peters","Pieters","Pijl","Pol","Prins","Roos","Sanders","Schipper",
        "Scholten","Schouten","Smeets","Smit","Smits","Snijders","Steen","Stork","Timmermans","Ven",
        "Verbeek","Verbeke","Vermeer","Vermeulen","Vis","Visser","Vliet","Vogel","Vos","Vries",
        "Willems","Willemsen","Wit","Wolf","Wolters","Zijlstra","Zwart","van Beek","van Dijk","van Leeuwen",
    ]

    cities = [
        ("Amsterdam","1011 AB","Noord-Holland"),
        ("Rotterdam","3011 BK","Zuid-Holland"),
        ("Utrecht","3512 JE","Utrecht"),
        ("Eindhoven","5611 AZ","Noord-Brabant"),
        ("Den Haag","2511 CR","Zuid-Holland"),
        ("Haarlem","2011 VB","Noord-Holland"),
        ("Groningen","9711 HK","Groningen"),
        ("Leiden","2312 BK","Zuid-Holland"),
        ("Tilburg","5032 ML","Noord-Brabant"),
        ("Nijmegen","6512 BT","Gelderland"),
        ("Breda","4811 ZG","Noord-Brabant"),
        ("Arnhem","6826 AB","Gelderland"),
        ("Maastricht","6211 EM","Limburg"),
        ("Zwolle","8011 MR","Overijssel"),
        ("Amersfoort","3812 JK","Utrecht"),
        ("Enschede","7511 JB","Overijssel"),
        ("Apeldoorn","7311 KZ","Gelderland"),
        ("Deventer","7411 JE","Overijssel"),
        ("Delft","2611 AC","Zuid-Holland"),
        ("Dordrecht","3311 GR","Zuid-Holland"),
        ("Alkmaar","1811 LC","Noord-Holland"),
        ("Venlo","5911 AA","Limburg"),
        ("Leeuwarden","8911 AA","Friesland"),
        ("Zaandam","1501 BV","Noord-Holland"),
        ("Hilversum","1211 AA","Noord-Holland"),
    ]

    categories = [
        ("Software Engineering",     ["Java,Spring Boot,AWS","Python,Django,PostgreSQL","Node.js,TypeScript,React","C#,.NET,Azure,SQL Server","Kotlin,Spring,Microservices","Scala,Akka,Kafka","Ruby on Rails,PostgreSQL,Redis"]),
        ("Cloud Engineering",        ["AWS,Terraform,Kubernetes","Azure,Bicep,AKS","GCP,BigQuery,Dataflow","Multi-Cloud,FinOps,Landing Zones","AWS,CDK,Lambda,API Gateway"]),
        ("DevOps",                   ["Kubernetes,Helm,ArgoCD,GitOps","CI/CD,GitHub Actions,Terraform,Docker","Jenkins,Ansible,Linux,Bash","Azure DevOps,Pipelines,Python","GitLab CI,Docker,Prometheus,Grafana"]),
        ("Site Reliability Engineering", ["SRE,Prometheus,Grafana,PagerDuty","Chaos Engineering,Reliability,Go","OpenTelemetry,Observability,AWS","SLO,SLI,Error Budgets,Python"]),
        ("Data Engineering",         ["Python,Spark,dbt,Snowflake","SQL,Airflow,BigQuery,dbt","Kafka,Flink,Delta Lake,Python","Azure Data Factory,Synapse,PySpark"]),
        ("Data Science",             ["Python,scikit-learn,XGBoost,Pandas","R,Statistics,A/B Testing,Tableau","Python,NLP,BERT,LangChain","Python,ML,Forecasting,Feature Engineering"]),
        ("Machine Learning Engineering", ["Python,PyTorch,MLflow,Kubeflow","LLMs,RAG,LangChain,OpenAI API","Python,TensorFlow,Vertex AI,MLOps","Recommendation Systems,Kafka,Real-Time ML"]),
        ("Frontend Development",     ["React,TypeScript,Next.js,GraphQL","Angular,RxJS,NgRx,Jest","Vue.js,Nuxt,Tailwind,Cypress","React Native,Expo,Firebase,TypeScript"]),
        ("Backend Development",      ["Node.js,TypeScript,PostgreSQL,Redis","Python,FastAPI,Celery,MongoDB","Go,gRPC,Kubernetes,PostgreSQL","Rust,WebAssembly,gRPC,Microservices"]),
        ("Cybersecurity",            ["SOC,SIEM,Splunk,Threat Hunting","Pentesting,Burp Suite,OWASP,CEH","Cloud Security,AWS Security,Zero Trust,IAM","GRC,ISO27001,DORA,Risk Management","AppSec,SAST,DAST,DevSecOps"]),
        ("IT Management",            ["ITIL,Prince2,Agile,Scrum","CTO Advisory,IT Strategy,Governance","ITSM,SIAM,Vendor Management,ITIL","Product Ownership,OKRs,B2B SaaS,Roadmap"]),
        ("Mobile Development",       ["iOS,Swift,SwiftUI,Combine","Android,Kotlin,Jetpack Compose","Flutter,Dart,Firebase,BLoC","React Native,TypeScript,Redux,Detox"]),
        ("Test Engineering",         ["Selenium,Playwright,Python,BDD","Cypress,TypeScript,CI/CD,SDET","JMeter,k6,Performance Testing,API Testing","Robot Framework,Python,Azure DevOps"]),
        ("SAP Consulting",           ["SAP S/4HANA,FI/CO,ABAP,Migration","SAP MM,PP,WM,S/4HANA,Fiori","SAP BW/4HANA,Analytics,SAC,Reporting"]),
        ("Business Intelligence",    ["Power BI,DAX,SQL Server,Azure Synapse","Tableau,Looker,dbt,BigQuery","Qlik,SQL,SSRS,Analytics Engineering"]),
        ("Database Administration",  ["Oracle DBA,PostgreSQL,Performance Tuning","SQL Server DBA,SSIS,Always On,Azure SQL","MongoDB,Redis,Cassandra,NoSQL Architecture"]),
        ("Solutions Architecture",   ["AWS,GCP,Microservices,Event-Driven","Azure,SAP,Integration,TOGAF","Domain-Driven Design,API Design,Cloud-Native"]),
        ("IT Architecture",          ["Enterprise Architecture,TOGAF,Archimate","Solution Architecture,Azure,DDD,API Design"]),
        ("Business Analysis",        ["Business Analysis,BABOK,UML,BPMN","Requirements Engineering,Stakeholder Mgmt,SQL"]),
        ("Network Engineering",      ["Cisco,CCNP,SD-WAN,BGP,OSPF","Juniper,Palo Alto,Network Security,Zero Trust"]),
    ]

    sources      = ["LinkedIn","Direct","Referral","Indeed","Website"]
    statuses     = ["Freelancer","Employed","New","Freelancer","Employed"]
    gdpr_bases   = ["Consent","Legitimate interest","Consent","Consent"]
    gdpr_sources = ["Email","Portal","LinkedIn","Email"]

    employers = [
        "ING Bank","Rabobank","ABN AMRO","Accenture","Capgemini","Sogeti","Deloitte","KPMG","PwC",
        "ASML","Philips","Shell","Unilever","Heineken","bol.com","Booking.com","Adyen","TomTom",
        "Exact Software","AFAS","Cegeka","Ctac","Atos","Infosys","Cognizant","Wipro","IBM",
        "Microsoft","Google","Amazon","Oracle","SAP","Salesforce","ServiceNow","Palo Alto Networks",
        "Coolblue","Takeaway.com","Ahold Delhaize","NS","ProRail","Rijksoverheid","Gemeente Amsterdam",
        "VodafoneZiggo","KPN","T-Mobile","Randstad","Hays","Yacht","USG People",
    ]

    degrees_bsc = [
        "BSc Computer Science","BSc Software Engineering","BSc Information Technology",
        "BSc Applied Mathematics","BSc Electrical Engineering","BSc Business Informatics",
        "BSc ICT","BSc Data Science","BSc Informatica",
    ]
    degrees_msc = [
        "MSc Computer Science","MSc Software Engineering","MSc Data Science",
        "MSc Artificial Intelligence","MSc Information Security","MSc Cloud Computing",
        "MSc Business Information Technology","MSc Embedded Systems","MSc Human-Computer Interaction",
    ]
    universities = [
        ("TU Delft","Delft"),("University of Amsterdam","Amsterdam"),("VU Amsterdam","Amsterdam"),
        ("Utrecht University","Utrecht"),("Eindhoven University of Technology","Eindhoven"),
        ("University of Groningen","Groningen"),("Radboud University","Nijmegen"),
        ("Tilburg University","Tilburg"),("Maastricht University","Maastricht"),
        ("Hogeschool van Amsterdam","Amsterdam"),("Hogeschool Rotterdam","Rotterdam"),
        ("Avans Hogeschool","Breda"),("Fontys Hogeschool","Eindhoven"),
        ("HAN University","Nijmegen"),("Saxion University","Enschede"),
        ("Haagse Hogeschool","Den Haag"),("NHL Stenden","Leeuwarden"),
    ]

    cands, edus, wxs, gdprs_out = [], [], [], []
    edu_counter = 200
    wx_counter  = 300

    for i in range(count):
        num     = start_num + i
        cid     = f"CV-{num:05d}"
        gender  = rng.choice(["M", "F"])
        fn      = rng.choice(first_names_m if gender == "M" else first_names_f)
        ln      = rng.choice(last_names)
        birth_y = rng.randint(1975, 2000)
        birth_m = rng.randint(1, 12)
        birth_d = rng.randint(1, 28)
        dob     = date(birth_y, birth_m, birth_d)

        city, zipcode, state = rng.choice(cities)
        phone_digits = "".join(str(rng.randint(0, 9)) for _ in range(8))
        phone = f"+31 6 {phone_digits[:4]} {phone_digits[4:]}"

        slug  = fn.lower().replace(" ", "").replace("é","e").replace("è","e").replace("ë","e").replace("ö","o").replace("ü","u")
        lslug = ln.lower().replace(" ", "").replace("é","e").replace("è","e").replace("ë","e").replace("ö","o").replace("ü","u")
        email = f"{slug[0]}.{lslug}{num}@email.nl"

        source     = rng.choice(sources)
        status     = rng.choice(statuses)
        cat_entry  = rng.choice(categories)
        category   = cat_entry[0]
        skills     = rng.choice(cat_entry[1])

        avail_days = rng.randint(-180, 540)
        avail_date = date(2025, 6, 1) + timedelta(days=avail_days)

        cands.append(c(cid, fn, ln, gender, dob, city, zipcode, state,
                       phone, email, source, avail_date, status, category, skills))

        has_msc = rng.random() < 0.55
        grad_year = max(birth_y + 18, 2000)

        if has_msc:
            bsc_start = date(grad_year, 9, 1)
            bsc_end   = date(grad_year + 3, 6, 30)
            msc_start = date(grad_year + 3, 9, 1)
            msc_end   = date(grad_year + 5, 6, 30)
            bsc_uni, bsc_city = rng.choice(universities)
            msc_uni, msc_city = rng.choice(universities)
            edu_counter += 1
            edus.append(edu(f"EDU-{edu_counter:04d}", cid,
                            rng.choice(degrees_bsc), bsc_uni, bsc_city, bsc_start, bsc_end))
            edu_counter += 1
            edus.append(edu(f"EDU-{edu_counter:04d}", cid,
                            rng.choice(degrees_msc), msc_uni, msc_city, msc_start, msc_end))
        else:
            bsc_start = date(grad_year, 9, 1)
            bsc_end   = date(grad_year + 4, 6, 30)
            bsc_uni, bsc_city = rng.choice(universities)
            edu_counter += 1
            edus.append(edu(f"EDU-{edu_counter:04d}", cid,
                            rng.choice(degrees_bsc), bsc_uni, bsc_city, bsc_start, bsc_end))

        num_roles   = rng.randint(2, 3)
        titles = {
            "Software Engineering":     ["Software Engineer","Senior Software Engineer","Lead Developer","Principal Engineer"],
            "Cloud Engineering":        ["Cloud Engineer","Senior Cloud Engineer","Cloud Architect","Platform Engineer"],
            "DevOps":                   ["DevOps Engineer","Senior DevOps Engineer","Platform Engineer","DevOps Lead"],
            "Site Reliability Engineering": ["SRE","Senior SRE","Site Reliability Engineer","Lead SRE"],
            "Data Engineering":         ["Data Engineer","Senior Data Engineer","Lead Data Engineer","Analytics Engineer"],
            "Data Science":             ["Data Scientist","Senior Data Scientist","Principal Data Scientist","Junior Data Scientist"],
            "Machine Learning Engineering": ["ML Engineer","Senior ML Engineer","ML Scientist","MLOps Engineer"],
            "Frontend Development":     ["Frontend Developer","Senior Frontend Developer","UI Engineer","Frontend Lead"],
            "Backend Development":      ["Backend Developer","Senior Backend Developer","Backend Lead","API Developer"],
            "Cybersecurity":            ["Security Analyst","Senior Security Consultant","Penetration Tester","Security Engineer"],
            "IT Management":            ["IT Manager","Programme Manager","Scrum Master","Product Owner"],
            "Mobile Development":       ["Mobile Developer","iOS Developer","Android Developer","Senior Mobile Engineer"],
            "Test Engineering":         ["Test Engineer","QA Engineer","SDET","Senior Test Automation Engineer"],
            "SAP Consulting":           ["SAP Consultant","Senior SAP Consultant","SAP Solution Architect","SAP Functional Analyst"],
            "Business Intelligence":    ["BI Developer","Senior BI Developer","Analytics Engineer","BI Architect"],
            "Database Administration":  ["DBA","Senior DBA","Database Engineer","Database Architect"],
            "Solutions Architecture":   ["Solutions Architect","Senior Solutions Architect","Enterprise Architect","Cloud Architect"],
            "IT Architecture":          ["IT Architect","Enterprise Architect","Solution Architect"],
            "Business Analysis":        ["Business Analyst","Senior Business Analyst","Functional Analyst","Lead BA"],
            "Network Engineering":      ["Network Engineer","Senior Network Engineer","Network Architect"],
        }
        role_titles = titles.get(category, ["IT Consultant","Senior IT Consultant"])

        current_end = None
        for r in range(num_roles):
            title     = rng.choice(role_titles)
            employer  = rng.choice(employers)
            role_yrs  = rng.randint(2, 5)
            if r == 0 and status in ("Freelancer", "New"):
                end_date  = None
                start_date = date(2025, 1, 1) - timedelta(days=rng.randint(180, 1095))
            else:
                if current_end is None:
                    current_end = date(2024, rng.randint(1, 12), 1)
                end_date   = current_end
                start_date = date(current_end.year - role_yrs, current_end.month, 1)
                current_end = date(start_date.year - 1, start_date.month, 1)

            wx_counter += 1
            wxs.append(wx(f"WX-{wx_counter:04d}", cid, title, employer, start_date, end_date))

        sent_date = date(2024, rng.randint(1, 12), rng.randint(1, 28))
        recv_date = date(sent_date.year, sent_date.month, min(sent_date.day + 2, 28))
        gdprs_out.append(gdpr(cid, "Recruitment processing",
                               rng.choice(gdpr_bases), sent_date, recv_date,
                               rng.choice(gdpr_sources)))

    return cands, edus, wxs, gdprs_out


_bulk = _generate_bulk(
    start_num=201,
    count=900,
)
CANDIDATES     += _bulk[0]
EDUCATION      += _bulk[1]
WORK_EXPERIENCE += _bulk[2]
GDPR           += _bulk[3]


def seed() -> None:
    with SessionLocal() as session:
        print("Clearing existing data...")
        session.query(CandidateGDPR).delete()
        session.query(CandidateWorkExperience).delete()
        session.query(CandidateEducation).delete()
        session.query(ClientContact).delete()
        session.query(ClientCorporation).delete()
        session.query(Candidate).delete()
        session.commit()

        print(f"Inserting {len(CANDIDATES)} candidates...")
        session.add_all(CANDIDATES)
        session.flush()

        print(f"Inserting {len(EDUCATION)} education records...")
        session.add_all(EDUCATION)

        print(f"Inserting {len(WORK_EXPERIENCE)} work experience records...")
        session.add_all(WORK_EXPERIENCE)

        print(f"Inserting {len(GDPR)} GDPR records...")
        session.add_all(GDPR)

        print(f"Inserting {len(CORPORATIONS)} client corporations...")
        session.add_all(CORPORATIONS)
        session.flush()

        print(f"Inserting {len(CONTACTS)} client contacts...")
        session.add_all(CONTACTS)

        session.commit()
        print(f"\nDone. {len(CANDIDATES)} candidates | {len(EDUCATION)} education | "
              f"{len(WORK_EXPERIENCE)} work experience | {len(CORPORATIONS)} corporations")


if __name__ == "__main__":
    seed()
