.. SETUP VARIABLES
.. |license-status| image:: https://img.shields.io/badge/license-MIT-blue.svg
  :target: https://github.com/mayeut/pep600_compliance/blob/master/LICENSE
.. END OF SETUP

PEP600 compliance check
=======================

|license-status|

This project aims to define manylinux policies according to
`PEP600 <https://www.python.org/dev/peps/pep-0600/>`_.

In order to do that, the project analyses symbols found on different linux distros.


Acceptable distros to build wheels
==================================

The following table has been generated automatically to give an idea of acceptable
distros to build manylinux wheels given different manylinux policies.

.. begin base_images_x86_64
.. csv-table:: x86_64
   :header: "policy", "distros"

   "manylinux_2_12", "centos 6"
   "manylinux_2_15", "ubuntu 12.04"
   "manylinux_2_19", "ubuntu 14.04"
   "manylinux_2_23", "ubuntu 16.04"
   "manylinux_2_24", "debian 9"
   "manylinux_2_31", "debian bullseye, ubuntu 20.04"
.. end base_images_x86_64

.. begin base_images_i686
.. csv-table:: i686
   :header: "policy", "distros"

   "manylinux_2_12", "centos 6"
   "manylinux_2_15", "ubuntu 12.04"
   "manylinux_2_17", "centos 7"
   "manylinux_2_19", "ubuntu 14.04"
   "manylinux_2_23", "ubuntu 16.04"
   "manylinux_2_24", "debian 9"
   "manylinux_2_27", "ubuntu 18.04"
   "manylinux_2_28", "debian 10"
   "manylinux_2_31", "debian bullseye"
.. end base_images_i686

.. begin base_images_aarch64
.. csv-table:: aarch64
   :header: "policy", "distros"

   "manylinux_2_17", "centos 7"
   "manylinux_2_19", "ubuntu 14.04"
   "manylinux_2_23", "ubuntu 16.04"
   "manylinux_2_24", "debian 9"
   "manylinux_2_31", "debian bullseye, ubuntu 20.04"
.. end base_images_aarch64

.. begin base_images_ppc64le
.. csv-table:: ppc64le
   :header: "policy", "distros"

   "manylinux_2_17", "centos 7"
   "manylinux_2_19", "ubuntu 14.04"
   "manylinux_2_23", "ubuntu 16.04"
   "manylinux_2_24", "debian 9"
   "manylinux_2_27", "ubuntu 18.04"
   "manylinux_2_28", "centos 8, debian 10"
   "manylinux_2_31", "debian bullseye, ubuntu 20.04"
.. end base_images_ppc64le

.. begin base_images_s390x
.. csv-table:: s390x
   :header: "policy", "distros"

   "manylinux_2_17", "clefos 7"
   "manylinux_2_23", "ubuntu 16.04"
   "manylinux_2_24", "debian 9"
   "manylinux_2_27", "ubuntu 18.04"
   "manylinux_2_28", "debian 10"
   "manylinux_2_31", "debian bullseye, ubuntu 20.04"
.. end base_images_s390x

.. begin base_images_armv7l
.. csv-table:: armv7l
   :header: "policy", "distros"

   "manylinux_2_13", "debian 7"
   "manylinux_2_19", "ubuntu 14.04"
   "manylinux_2_23", "ubuntu 16.04"
   "manylinux_2_24", "debian 9"
   "manylinux_2_27", "ubuntu 18.04"
   "manylinux_2_28", "debian 10"
   "manylinux_2_31", "debian bullseye, ubuntu 20.04"
.. end base_images_armv7l

Distro compatibility
====================

This table allows to know what distributions are tested.
If your favorite distro does not appear here:

- you can check the glibc version over at distrowatch.com
- you can create a PR in order for it to be referenced

.. begin compatibility_x86_64
.. csv-table:: x86_64
   :header: "policy", "distros"

   "manylinux_2_12", "centos 6, oraclelinux 6"
   "manylinux_2_13", "debian 7"
   "manylinux_2_15", "slackware 14.0, ubuntu 12.04, ubuntu 12.10"
   "manylinux_2_17", "amazonlinux 1, centos 7, oraclelinux 7, rhubi 7, slackware 14.1, ubuntu 13.04, ubuntu 13.10"
   "manylinux_2_18", "fedora 20"
   "manylinux_2_19", "debian 8, opensuse 13.2, opensuse 42.1, ubuntu 14.04, ubuntu 14.10"
   "manylinux_2_20", "fedora 21, mageia 5"
   "manylinux_2_21", "fedora 22, ubuntu 15.04, ubuntu 15.10"
   "manylinux_2_22", "fedora 23, mageia 6, opensuse 42.2, opensuse 42.3, photon 1.0"
   "manylinux_2_23", "alt p8, fedora 24, slackware 14.2, ubuntu 16.04"
   "manylinux_2_24", "debian 9, fedora 25, ubuntu 16.10, ubuntu 17.04"
   "manylinux_2_25", "fedora 26"
   "manylinux_2_26", "amazonlinux 2, fedora 27, opensuse 15.0, opensuse 15.1, opensuse 15.2, photon 2.0, ubuntu 17.10"
   "manylinux_2_27", "alt p9, fedora 28, ubuntu 18.04"
   "manylinux_2_28", "centos 8, debian 10, fedora 29, oraclelinux 8, photon 3.0, rhubi 8, ubuntu 18.10"
   "manylinux_2_29", "fedora 30, mageia 7, ubuntu 19.04"
   "manylinux_2_30", "alt sisyphus, archlinux 20191006, archlinux 20191105, archlinux 20191205, archlinux 20200106, archlinux 20200205, fedora 31, ubuntu 19.10"
   "manylinux_2_31", "archlinux 20200306, clearlinux latest, debian bullseye, fedora 32, opensuse tumbleweed, ubuntu 20.04"
   "manylinux_2_32", "archlinux 20200908, fedora 33, ubuntu 20.10"
   "manylinux_2_32_9000", "fedora 34"
.. end compatibility_x86_64

.. begin compatibility_i686
.. csv-table:: i686
   :header: "policy", "distros"

   "manylinux_2_12", "centos 6"
   "manylinux_2_13", "debian 7"
   "manylinux_2_15", "ubuntu 12.04"
   "manylinux_2_17", "centos 7"
   "manylinux_2_19", "debian 8, ubuntu 14.04"
   "manylinux_2_21", "ubuntu 15.04, ubuntu 15.10"
   "manylinux_2_23", "alt p8, ubuntu 16.04"
   "manylinux_2_24", "debian 9, ubuntu 16.10, ubuntu 17.04"
   "manylinux_2_26", "ubuntu 17.10"
   "manylinux_2_27", "alt p9, ubuntu 18.04"
   "manylinux_2_28", "debian 10, ubuntu 18.10"
   "manylinux_2_29", "ubuntu 19.04"
   "manylinux_2_30", "alt sisyphus, ubuntu 19.10"
   "manylinux_2_31", "debian bullseye, opensuse tumbleweed"
.. end compatibility_i686

.. begin compatibility_aarch64
.. csv-table:: aarch64
   :header: "policy", "distros"

   "manylinux_2_17", "centos 7, oraclelinux 7"
   "manylinux_2_19", "ubuntu 14.04"
   "manylinux_2_23", "ubuntu 16.04"
   "manylinux_2_24", "debian 9, ubuntu 16.10, ubuntu 17.04"
   "manylinux_2_25", "fedora 26"
   "manylinux_2_26", "amazonlinux 2, fedora 27, opensuse 15.0, opensuse 15.1, opensuse 15.2, ubuntu 17.10"
   "manylinux_2_27", "alt p9, fedora 28, ubuntu 18.04"
   "manylinux_2_28", "centos 8, debian 10, fedora 29, oraclelinux 8, photon 3.0, rhubi 8, ubuntu 18.10"
   "manylinux_2_29", "fedora 30, mageia 7, ubuntu 19.04"
   "manylinux_2_30", "alt sisyphus, fedora 31, ubuntu 19.10"
   "manylinux_2_31", "debian bullseye, fedora 32, opensuse tumbleweed, ubuntu 20.04"
   "manylinux_2_32", "fedora 33, ubuntu 20.10"
   "manylinux_2_32_9000", "fedora 34"
.. end compatibility_aarch64

.. begin compatibility_ppc64le
.. csv-table:: ppc64le
   :header: "policy", "distros"

   "manylinux_2_17", "centos 7, rhubi 7"
   "manylinux_2_19", "ubuntu 14.04"
   "manylinux_2_23", "ubuntu 16.04"
   "manylinux_2_24", "debian 9, ubuntu 16.10, ubuntu 17.04"
   "manylinux_2_25", "fedora 26"
   "manylinux_2_26", "fedora 27, opensuse 15.0, ubuntu 17.10"
   "manylinux_2_27", "alt p9, fedora 28, ubuntu 18.04"
   "manylinux_2_28", "centos 8, debian 10, fedora 29, rhubi 8, ubuntu 18.10"
   "manylinux_2_29", "fedora 30, ubuntu 19.04"
   "manylinux_2_30", "alt sisyphus, fedora 31, ubuntu 19.10"
   "manylinux_2_31", "debian bullseye, fedora 32, opensuse tumbleweed, ubuntu 20.04"
   "manylinux_2_32", "ubuntu 20.10"
.. end compatibility_ppc64le

.. begin compatibility_s390x
.. csv-table:: s390x
   :header: "policy", "distros"

   "manylinux_2_17", "clefos 7, rhubi 7"
   "manylinux_2_23", "ubuntu 16.04"
   "manylinux_2_24", "debian 9, ubuntu 16.10, ubuntu 17.04"
   "manylinux_2_26", "ubuntu 17.10"
   "manylinux_2_27", "fedora 28, ubuntu 18.04"
   "manylinux_2_28", "debian 10, fedora 29, rhubi 8, ubuntu 18.10"
   "manylinux_2_29", "fedora 30, ubuntu 19.04"
   "manylinux_2_30", "fedora 31, ubuntu 19.10"
   "manylinux_2_31", "debian bullseye, fedora 32, ubuntu 20.04"
   "manylinux_2_32", "ubuntu 20.10"
.. end compatibility_s390x

.. begin compatibility_armv7l
.. csv-table:: armv7l
   :header: "policy", "distros"

   "manylinux_2_13", "debian 7"
   "manylinux_2_19", "debian 8, ubuntu 14.04"
   "manylinux_2_23", "ubuntu 16.04"
   "manylinux_2_24", "debian 9, ubuntu 16.10, ubuntu 17.04"
   "manylinux_2_26", "opensuse 15.1, opensuse 15.2, ubuntu 17.10"
   "manylinux_2_27", "ubuntu 18.04"
   "manylinux_2_28", "debian 10, ubuntu 18.10"
   "manylinux_2_29", "ubuntu 19.04"
   "manylinux_2_30", "ubuntu 19.10"
   "manylinux_2_31", "debian bullseye, opensuse tumbleweed, ubuntu 20.04"
   "manylinux_2_32", "ubuntu 20.10"
.. end compatibility_armv7l
