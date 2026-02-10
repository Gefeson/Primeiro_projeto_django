#!/usr/bin/env bash
set -o errexit

# instala as dependências
pip install -r requirements.txt

# coleta arquivos estáticos
python manage.py collectstatic --no-input

# aplica migrações
python manage.py migrate

# cria superusuário se variáveis existirem
if [ -n "$SUPERUSER_NAME" ]; then
python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="$SUPERUSER_NAME").exists():
    User.objects.create_superuser(
        "$SUPERUSER_NAME",
        "$SUPERUSER_EMAIL",
        "$SUPERUSER_PASSWORD"
    )
    print("Superuser criado com sucesso!")
else:
    print("Superuser já existe!")
EOF
fi
