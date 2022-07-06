import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.core.config import settings

logger = logging.getLogger(__name__)

M_PROFILE = [
    {'time': 1, 'value': 100},
    {'time': 4, 'value': 110},
    {'time': 7, 'value': 110},
    {'time': 10, 'value': 120},
    {'time': 13, 'value': 100},
    {'time': 16, 'value': 110},
    {'time': 19, 'value': 110},
    {'time': 22, 'value': 120}
]

M_LEVELS = ['Low', 'Moderate', 'High']
M_APPS = ['LNG Cold Recovery', 'Cooling Peak Load Shifting']

M_PARAMS = {
    'app': M_APPS[0],
    'pressure': 2.0,
    'upper_temperature': -10.0,
    'lower_temperature': 100.0,
    'accuracy_level': M_LEVELS[0]
}

M_CASE= [
    {
        'params' : M_PARAMS,
        'flowrate': M_PROFILE,
    }
]

M_RESULT={
    'type': 'Sensible Packed Bed',
    'htf': "Air",
    'material': "Granite",
    'cost': 100,
    'run_time': 10452,
    'case_id': 1
}

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.user.UserCreate(
                first_name="Initial Super User",
                email=settings.FIRST_SUPERUSER,
                is_superuser=True,
                is_user=True,
                password=settings.FIRST_SUPERUSER_PW,
            )
            user = crud.user.create(db, obj_in=user_in)
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
            
        """ 
        if not user.cases:
            for case in M_CASE:
                case_in = schemas.case.CaseCreate(
                    submitter_id=user.id
                )
                case_created = crud.case.create(db, obj_in=case_in)

                params_in = schemas.case.CaseParamsCreate(
                    **case['params']
                )
                params_in.case_id = case_created.id
                param = crud.caseparams.create(db, obj_in=params_in)
                
                for item in case['flowrate']:
                    profile_in = schemas.flowprofile.FlowProfileCreate(**item)
                    profile_in.params_id = param.id
                    crud.flowprofile.create(db, obj_in=profile_in)
                
                result_in = schemas.result.ResultCreate(**M_RESULT)
                result_in.case_id = case_created.id
                crud.result.create(db, obj_in=result_in)
        """
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
