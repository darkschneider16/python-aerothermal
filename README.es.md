# python-aerothermal

python-aerothermal es una solución para registrar los consumos de electricidad desde la red de distribución i-DE y anotarlos en *Zabbix*.

Hay que preparar el servidor para lanzar un *script* diario hecho en *bash* que invoca al código en *Python* que realmente realiza todo el trabajo.

## Instalación

Lo primero que se debe hacer es crear un fichero de credenciales que nos permiten acceder al *frontend* de i-DE. Hay un ejemplo .ini en el repositorio que puede ser copiado al directorio */etc*, con los datos correctos, y que sólo tenga acceso un usuario sin privilegios con el que se realizará todo el proceso.
Para verificar el éxito, o fracaso, del *script* debemos crear un archivo de *log* en */var/log*, de nuevo, sólo con acceso de escritura para el usuario anteriormente creado así como la creación de un fichero *logrotate*, también en el repositorio, para evitar que el tamaño del *log* crezca sin medida.
También se debe crear el entorno virtual de *Python* que nos permita independizarnos de las librería del sistema evitando posibles problemas con actualizaciones globales. Este entorno lo crearemos dentro del directorio del usuario creado:

```bash
python -m venv ~/.venv
```

El *script* de *bash* que llamará al código hecho en *Python* verificará que este entorno virtual está correctamente configurado antes de invocar el *script* en *Python*.

## Uso

Una vez que todo lo anterior está configurado podemos crear el *cronjob* sólo para el usuario:

```text
0 8 * * *   /bin/bash /home/metrics/python-aerothermal/zabbix_iber.sh -c /etc/credentials.ini -l /var/log/zabbix-iber.log >/dev/null 2>&1
```

La línea anterior fur creada con el comando ```crontab -e``` y se pueden ver los ficheros nombrados con anterioridad.

La configuración del servidor *Zabbix* y del agente pueden ser consultados en mi [blog](https://libreadmin.es/new-post-just-to-remember-using-david-bowie-lets-dance/) y en [mi repositorio de GitHub](https://github.com/darkschneider16/home-infrastructure). En el futuro publicaré cómo crear el ítem en el que se anotan estas lecturas y quizá una plantilla con más datos relacionados.

## Pruebas

En el repositorio también se puede encontrar una prueba preliminar para desarrollar el proyecto mediante la tecnología BDD (Behaviour Driver Development) usando para ello la librería *Python* llamada *behave. Si quieres probarla, o mejor aún, contribuir completando las pruebas, se debe instalar en el entorno virtual creado:

```bash
(.venv) pip install behave
```

## Contribuciones

Las contribuciones son bienvenidas. Para cambios mayores se agradecería, antes que un *Pull Request*, un *issue* en el que podamos hablar sobre lo que se quiere cambiar.

## Licencia

He incluido en el proyecto la librería del usuario [hectorespert](https://github.com/hectorespert) llamada [python-oligo](https://github.com/hectorespert/python-oligo).

He licenciado el código de la misma forma y he incluido un par de métodos que necesitaba para este proyecto en concreto. Espero haber respetado el espíritu de la librería original ya que además, el repositorio está archivado.
