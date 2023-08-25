Installation
============

Follow these steps to install and set up the project:

1. Clone the repository:

   .. code-block:: shell

      git clone https://github.com/Akhtyrtsev/artists.git
      or
      git@github.com:Akhtyrtsev/artists.git

2. Configure environment variables:

   Create a `.env` file and add your configuration variables.

    Required env variables can be found in configuration section

3. Use make command to build docker containers:

   .. code-block:: shell

      make build

4. Use make command to run docker containers:

   .. code-block:: shell

      make run

4. Run migrations:

   .. code-block:: shell

      make migrate
