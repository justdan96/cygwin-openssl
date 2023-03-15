# cygwin-openssl
OpenSSL in Cygwin in Fedora. Fork of yselkowitz/cygwin-openssl. 

## Releases
For the latest release see https://github.com/justdan96/cygwin-openssl/releases.

## Creation
In the `scripts` folder there are scripts for generating the RPMs. There is a `justfile` for creating the RPMs for each version of Fedora. In the same folder is a `Dockerfile`, this Dockerfile creates the environment for building the RPM and then runs the commands to package the RPM. There are some slight hacks to get around issues with packaging on Fedora, I've chosen to keep these in the `Dockerfile` rather than the `spec` file.
