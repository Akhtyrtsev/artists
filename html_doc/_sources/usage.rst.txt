Usage
=====

Learn how to use your project's features effectively. Check `Makefile` for more details

Getting Started
---------------

1. Build all necessary containers:

   .. code-block:: shell

    make build

2. Clean all containers related with this project

   .. code-block:: shell

    make clean
3. Run development server (run containers)

   .. code-block:: shell

    make run

4. Stop development server (run containers)

   .. code-block:: shell

    make down

5. Check django-server output

   .. code-block:: shell

    make django-logs

6. Check celery worker output

   .. code-block:: shell

    make celery-logs

7. Check celery-beat container output

   .. code-block:: shell

    make celery-beat logs


8. Make migrations for new/updated models

   .. code-block:: shell

    make makemigrations

9. Apply migrations

   .. code-block:: shell

    make migrate

10. Apply migrations

   .. code-block:: shell

    make migrate

11. Open django shell

   .. code-block:: shell

    make shell

12. Run tests

   .. code-block:: shell

    make test

12. Build updated docs

   .. code-block:: shell

    sphinx-build -b html docs html_doc

Access the admin panel at http://localhost:8000/admin/.

In order to update documentation go to /docs directory make necessary changes in corresponding
modules and than build a new version of it using command from root directory



python sphinx package must be installed