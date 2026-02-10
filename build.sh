#!/user/bin/env bash
#Interrompe a execução se algum comando falhar
set -o errexit

#instala as dependencias
pip install -r requirements.txt

#coleta arquivos estaticos
python manage.py collectstatic --no-input

#aplica as migrações do banco de dados
python manage.py migrate

#cria superusuario se não existir
if [ "$SUPERUSER_NAME" ]; then
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$SUPERUSER_NAME').exit():
    User.objects.creat_superuser('$SUPERUSER_NAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
    print("Superuser criado com sucesso!)
else:
    print("Superuser já existe!")
END
fi