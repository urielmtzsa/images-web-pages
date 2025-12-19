FROM public.ecr.aws/lambda/python:3.9

# Copiar dependencias
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copiar código
COPY app.py ./

# Definir el handler
CMD ["app.handler"]