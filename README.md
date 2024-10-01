Drilling MVP
---
Drilling MVP is an application designed to improve the performance of drilling rigs and sensors on them
# Technologies Used:
- FastAPI
- SQLAlchemy, Alembic
- uvicorn

# Installation:
## 1. Cloning a repository

`git clone git@github.com:Lerokkkk/drilling_mvp.git`

`cd drilling_mvp`
## 2. Create Virtual Environment:
`python -m venv venv`
## 3. Activate Virtual Environment:
`venv\Scripts\activate`
## 4.Install Dependcies:
`pip install -r requirements.txt`
## 5. Run Migrations:
`alembic upgrade head`
## 6. Run server:
`uvicorn src.main:app --env-file your_file --reload`