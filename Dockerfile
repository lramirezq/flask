FROM amazon/aws-lambda-python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY src/*  ${LAMBDA_TASK_ROOT}

RUN python ${LAMBDA_TASK_ROOT}/db.py 

CMD ["app.handler"]