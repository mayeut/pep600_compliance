.. SETUP VARIABLES
.. |license-status| image:: https://img.shields.io/badge/license-MIT-blue.svg
  :target: https://github.com/mayeut/pep600_compliance/blob/master/LICENSE
.. END OF SETUP

.. begin distro_badges
.. |alt-sisyphus| image:: https://img.shields.io/static/v1?label=alt&message=sisyphus%20(rolling)&color=purple
.. |alt-p9| image:: https://img.shields.io/static/v1?label=alt&message=p9%20(unknown)&color=lightgray
.. |alt-p8| image:: https://img.shields.io/static/v1?label=alt&message=p8%20(unknown)&color=lightgray
.. |amazonlinux-2| image:: https://img.shields.io/static/v1?label=amazonlinux&message=2%20(EOL%3A2023-06-30)&color=green&logo=amazon-aws&logoColor=white
.. |amazonlinux-1| image:: https://img.shields.io/static/v1?label=amazonlinux&message=1%20(EOL%3A2020-12-31%20/%20LTS%3A2023-06-30)&color=green&logo=amazon-aws&logoColor=white
.. |archlinux-latest| image:: https://img.shields.io/static/v1?label=archlinux&message=latest%20(rolling)&color=purple&logo=arch-linux&logoColor=white
.. |centos-8| image:: https://img.shields.io/static/v1?label=centos&message=8%20(EOL%3A2029-05-31)&color=green&logo=centos&logoColor=white
.. |centos-7| image:: https://img.shields.io/static/v1?label=centos&message=7%20(EOL%3A2024-06-30)&color=green&logo=centos&logoColor=white
.. |centos-6| image:: https://img.shields.io/static/v1?label=centos&message=6%20(EOL%3A2020-11-30)&color=yellow&logo=centos&logoColor=white
.. |clearlinux-latest| image:: https://img.shields.io/static/v1?label=clearlinux&message=latest%20(rolling)&color=purple
.. |clefos-7| image:: https://img.shields.io/static/v1?label=clefos&message=7%20(EOL%3A2024-06-30)&color=green
.. |debian-experimental| image:: https://img.shields.io/static/v1?label=debian&message=experimental%20(rolling)&color=purple&logo=debian&logoColor=white
.. |debian-unstable| image:: https://img.shields.io/static/v1?label=debian&message=unstable%20(rolling)&color=purple&logo=debian&logoColor=white
.. |debian-testing| image:: https://img.shields.io/static/v1?label=debian&message=testing%20(rolling)&color=purple&logo=debian&logoColor=white
.. |debian-10| image:: https://img.shields.io/static/v1?label=debian&message=10%20(EOL%3A2022-07-31%20/%20LTS%3A2024-06-30)&color=green&logo=debian&logoColor=white
.. |debian-9| image:: https://img.shields.io/static/v1?label=debian&message=9%20(EOL%3A2020-07-05%20/%20LTS%3A2022-06-30)&color=green&logo=debian&logoColor=white
.. |debian-8| image:: https://img.shields.io/static/v1?label=debian&message=8%20(EOL%3A2018-06-06%20/%20LTS%3A2020-06-30%20/%20ELTS%3A2022-06-30)&color=red&logo=debian&logoColor=white
.. |debian-7| image:: https://img.shields.io/static/v1?label=debian&message=7%20(EOL%3A2016-04-26%20/%20LTS%3A2018-05-31%20/%20ELTS%3A2020-06-30)&color=black&logo=debian&logoColor=white
.. |fedora-rawhide| image:: https://img.shields.io/static/v1?label=fedora&message=rawhide%20(rolling)&color=purple&logo=fedora&logoColor=white
.. |fedora-33| image:: https://img.shields.io/static/v1?label=fedora&message=33%20(unknown)&color=lightgray&logo=fedora&logoColor=white
.. |fedora-32| image:: https://img.shields.io/static/v1?label=fedora&message=32%20(unknown)&color=lightgray&logo=fedora&logoColor=white
.. |fedora-31| image:: https://img.shields.io/static/v1?label=fedora&message=31%20(EOL%3A2020-11-17)&color=black&logo=fedora&logoColor=white
.. |fedora-30| image:: https://img.shields.io/static/v1?label=fedora&message=30%20(EOL%3A2020-05-26)&color=black&logo=fedora&logoColor=white
.. |fedora-29| image:: https://img.shields.io/static/v1?label=fedora&message=29%20(EOL%3A2019-11-26)&color=black&logo=fedora&logoColor=white
.. |fedora-28| image:: https://img.shields.io/static/v1?label=fedora&message=28%20(EOL%3A2019-05-28)&color=black&logo=fedora&logoColor=white
.. |fedora-27| image:: https://img.shields.io/static/v1?label=fedora&message=27%20(EOL%3A2018-11-30)&color=black&logo=fedora&logoColor=white
.. |fedora-26| image:: https://img.shields.io/static/v1?label=fedora&message=26%20(EOL%3A2018-05-29)&color=black&logo=fedora&logoColor=white
.. |fedora-25| image:: https://img.shields.io/static/v1?label=fedora&message=25%20(EOL%3A2017-12-12)&color=black&logo=fedora&logoColor=white
.. |fedora-24| image:: https://img.shields.io/static/v1?label=fedora&message=24%20(EOL%3A2017-08-08)&color=black&logo=fedora&logoColor=white
.. |fedora-23| image:: https://img.shields.io/static/v1?label=fedora&message=23%20(EOL%3A2016-12-20)&color=black&logo=fedora&logoColor=white
.. |fedora-22| image:: https://img.shields.io/static/v1?label=fedora&message=22%20(EOL%3A2016-07-19)&color=black&logo=fedora&logoColor=white
.. |fedora-21| image:: https://img.shields.io/static/v1?label=fedora&message=21%20(EOL%3A2015-12-01)&color=black&logo=fedora&logoColor=white
.. |fedora-20| image:: https://img.shields.io/static/v1?label=fedora&message=20%20(EOL%3A2015-06-23)&color=black&logo=fedora&logoColor=white
.. |mageia-7| image:: https://img.shields.io/static/v1?label=mageia&message=7%20(EOL%3A2021-02-08)&color=yellow
.. |mageia-6| image:: https://img.shields.io/static/v1?label=mageia&message=6%20(EOL%3A2019-09-30)&color=black
.. |mageia-5| image:: https://img.shields.io/static/v1?label=mageia&message=5%20(EOL%3A2017-12-31)&color=black
.. |manylinux-2014| image:: https://img.shields.io/static/v1?label=manylinux&message=2014%20(EOL%3A2024-06-30)&color=green&logo=python&logoColor=white
.. |manylinux-2010| image:: https://img.shields.io/static/v1?label=manylinux&message=2010%20(EOL%3A2020-11-30)&color=yellow&logo=python&logoColor=white
.. |manylinux-1| image:: https://img.shields.io/static/v1?label=manylinux&message=1%20(EOL%3A2017-03-31)&color=black&logo=python&logoColor=white
.. |opensuse-tumbleweed| image:: https://img.shields.io/static/v1?label=opensuse&message=tumbleweed%20(rolling)&color=purple&logo=opensuse&logoColor=white
.. |opensuse-15.2| image:: https://img.shields.io/static/v1?label=opensuse&message=15.2%20(EOL%3A2021-12-31)&color=green&logo=opensuse&logoColor=white
.. |opensuse-15.1| image:: https://img.shields.io/static/v1?label=opensuse&message=15.1%20(EOL%3A2020-11-30)&color=yellow&logo=opensuse&logoColor=white
.. |opensuse-15.0| image:: https://img.shields.io/static/v1?label=opensuse&message=15.0%20(EOL%3A2019-12-03)&color=black&logo=opensuse&logoColor=white
.. |opensuse-42.3| image:: https://img.shields.io/static/v1?label=opensuse&message=42.3%20(EOL%3A2019-07-01)&color=black&logo=opensuse&logoColor=white
.. |opensuse-42.2| image:: https://img.shields.io/static/v1?label=opensuse&message=42.2%20(EOL%3A2018-01-26)&color=black&logo=opensuse&logoColor=white
.. |opensuse-42.1| image:: https://img.shields.io/static/v1?label=opensuse&message=42.1%20(EOL%3A2017-05-17)&color=black&logo=opensuse&logoColor=white
.. |opensuse-13.2| image:: https://img.shields.io/static/v1?label=opensuse&message=13.2%20(EOL%3A2017-01-17)&color=black&logo=opensuse&logoColor=white
.. |oraclelinux-8| image:: https://img.shields.io/static/v1?label=oraclelinux&message=8%20(EOL%3A2029-07-31)&color=green&logo=oracle&logoColor=white
.. |oraclelinux-7| image:: https://img.shields.io/static/v1?label=oraclelinux&message=7%20(EOL%3A2024-07-31)&color=green&logo=oracle&logoColor=white
.. |oraclelinux-6| image:: https://img.shields.io/static/v1?label=oraclelinux&message=6%20(EOL%3A2021-03-31%20/%20ELTS%3A2024-03-31)&color=yellow&logo=oracle&logoColor=white
.. |photon-3.0| image:: https://img.shields.io/static/v1?label=photon&message=3.0%20(unknown)&color=lightgray&logo=vmware&logoColor=white
.. |photon-2.0| image:: https://img.shields.io/static/v1?label=photon&message=2.0%20(unknown)&color=lightgray&logo=vmware&logoColor=white
.. |photon-1.0| image:: https://img.shields.io/static/v1?label=photon&message=1.0%20(unknown)&color=lightgray&logo=vmware&logoColor=white
.. |rhubi-8| image:: https://img.shields.io/static/v1?label=rhubi&message=8%20(EOL%3A2029-05-31)&color=green&logo=red-hat&logoColor=white
.. |rhubi-7| image:: https://img.shields.io/static/v1?label=rhubi&message=7%20(EOL%3A2024-06-30)&color=green&logo=red-hat&logoColor=white
.. |slackware-current| image:: https://img.shields.io/static/v1?label=slackware&message=current%20(rolling)&color=purple&logo=slackware&logoColor=white
.. |slackware-14.2| image:: https://img.shields.io/static/v1?label=slackware&message=14.2%20(unknown)&color=lightgray&logo=slackware&logoColor=white
.. |slackware-14.1| image:: https://img.shields.io/static/v1?label=slackware&message=14.1%20(unknown)&color=lightgray&logo=slackware&logoColor=white
.. |slackware-14.0| image:: https://img.shields.io/static/v1?label=slackware&message=14.0%20(unknown)&color=lightgray&logo=slackware&logoColor=white
.. |ubuntu-rolling| image:: https://img.shields.io/static/v1?label=ubuntu&message=rolling%20(rolling)&color=purple&logo=ubuntu&logoColor=white
.. |ubuntu-20.10| image:: https://img.shields.io/static/v1?label=ubuntu&message=20.10%20(EOL%3A2021-07-17)&color=green&logo=ubuntu&logoColor=white
.. |ubuntu-20.04| image:: https://img.shields.io/static/v1?label=ubuntu&message=20.04%20(EOL%3A2025-04-30%20/%20ELTS%3A2030-04-30)&color=green&logo=ubuntu&logoColor=white
.. |ubuntu-19.10| image:: https://img.shields.io/static/v1?label=ubuntu&message=19.10%20(EOL%3A2020-07-17)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-19.04| image:: https://img.shields.io/static/v1?label=ubuntu&message=19.04%20(EOL%3A2020-01-23)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-18.10| image:: https://img.shields.io/static/v1?label=ubuntu&message=18.10%20(EOL%3A2019-07-18)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-18.04| image:: https://img.shields.io/static/v1?label=ubuntu&message=18.04%20(EOL%3A2023-04-30%20/%20ELTS%3A2028-04-30)&color=green&logo=ubuntu&logoColor=white
.. |ubuntu-17.10| image:: https://img.shields.io/static/v1?label=ubuntu&message=17.10%20(EOL%3A2018-07-19)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-17.04| image:: https://img.shields.io/static/v1?label=ubuntu&message=17.04%20(EOL%3A2018-01-13)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-16.10| image:: https://img.shields.io/static/v1?label=ubuntu&message=16.10%20(EOL%3A2017-07-20)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-16.04| image:: https://img.shields.io/static/v1?label=ubuntu&message=16.04%20(EOL%3A2021-04-30%20/%20ELTS%3A2024-04-30)&color=yellow&logo=ubuntu&logoColor=white
.. |ubuntu-15.10| image:: https://img.shields.io/static/v1?label=ubuntu&message=15.10%20(EOL%3A2016-07-28)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-15.04| image:: https://img.shields.io/static/v1?label=ubuntu&message=15.04%20(EOL%3A2016-02-04)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-14.10| image:: https://img.shields.io/static/v1?label=ubuntu&message=14.10%20(EOL%3A2015-07-23)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-14.04| image:: https://img.shields.io/static/v1?label=ubuntu&message=14.04%20(EOL%3A2019-04-25%20/%20ELTS%3A2022-04-30)&color=red&logo=ubuntu&logoColor=white
.. |ubuntu-13.10| image:: https://img.shields.io/static/v1?label=ubuntu&message=13.10%20(EOL%3A2014-07-17)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-13.04| image:: https://img.shields.io/static/v1?label=ubuntu&message=13.04%20(EOL%3A2014-01-27)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-12.10| image:: https://img.shields.io/static/v1?label=ubuntu&message=12.10%20(EOL%3A2014-05-16)&color=black&logo=ubuntu&logoColor=white
.. |ubuntu-12.04| image:: https://img.shields.io/static/v1?label=ubuntu&message=12.04%20(EOL%3A2017-04-28%20/%20ELTS%3A2019-04-30)&color=black&logo=ubuntu&logoColor=white
.. end distro_badges

PEP600 compliance check
=======================

|license-status|

This project aims to define manylinux policies according to
`PEP600 <https://www.python.org/dev/peps/pep-0600/>`_.

In order to do that, the project analyses symbols found on different linux distros.

End-Of-Life information can be found in `EOL <./EOL.rst>`_.

The following is a summary of the full analysis that can be found in `DETAILS <./DETAILS.rst>`_.


Acceptable distros to build wheels
==================================

The following table has been generated automatically to give an idea of acceptable
distros to build manylinux wheels given different manylinux policies.

.. begin base_images
.. csv-table:: base images
   :header: "policy", "distros"

   "manylinux_2_5", "|manylinux-1|"
   "manylinux_2_12", "|centos-6| |manylinux-2010|"
   "manylinux_2_15", "|ubuntu-12.04|"
   "manylinux_2_17", "|centos-7| |clefos-7| |manylinux-2014|"
   "manylinux_2_19", "|ubuntu-14.04|"
   "manylinux_2_23", "|ubuntu-16.04|"
   "manylinux_2_24", "|debian-9|"
   "manylinux_2_31", "|ubuntu-20.04|"
.. end base_images

Distro compatibility
====================

This table allows to know what distributions are tested.
If your favorite distro does not appear here:

- you can check the glibc version over at distrowatch.com
- you can create a PR in order for it to be referenced

.. begin compatibility
.. csv-table:: compatibility
   :header: "policy", "distros"

   "manylinux_2_5", "|manylinux-1|"
   "manylinux_2_12", "|centos-6| |manylinux-2010| |oraclelinux-6|"
   "manylinux_2_13", "|debian-7|"
   "manylinux_2_15", "|slackware-14.0| |ubuntu-12.04| |ubuntu-12.10|"
   "manylinux_2_17", "|amazonlinux-1| |centos-7| |clefos-7| |manylinux-2014| |oraclelinux-7| |rhubi-7| |slackware-14.1| |ubuntu-13.04| |ubuntu-13.10|"
   "manylinux_2_18", "|fedora-20|"
   "manylinux_2_19", "|debian-8| |opensuse-13.2| |opensuse-42.1| |ubuntu-14.04| |ubuntu-14.10|"
   "manylinux_2_20", "|fedora-21| |mageia-5|"
   "manylinux_2_21", "|fedora-22| |ubuntu-15.04| |ubuntu-15.10|"
   "manylinux_2_22", "|fedora-23| |mageia-6| |opensuse-42.2| |opensuse-42.3| |photon-1.0|"
   "manylinux_2_23", "|alt-p8| |fedora-24| |slackware-14.2| |ubuntu-16.04|"
   "manylinux_2_24", "|debian-9| |fedora-25| |ubuntu-16.10| |ubuntu-17.04|"
   "manylinux_2_25", "|fedora-26|"
   "manylinux_2_26", "|amazonlinux-2| |fedora-27| |opensuse-15.0| |opensuse-15.1| |opensuse-15.2| |photon-2.0| |ubuntu-17.10|"
   "manylinux_2_27", "|alt-p9| |fedora-28| |ubuntu-18.04|"
   "manylinux_2_28", "|centos-8| |debian-10| |fedora-29| |oraclelinux-8| |photon-3.0| |rhubi-8| |ubuntu-18.10|"
   "manylinux_2_29", "|fedora-30| |mageia-7| |ubuntu-19.04|"
   "manylinux_2_30", "|alt-sisyphus| |fedora-31| |slackware-current| |ubuntu-19.10|"
   "manylinux_2_31", "|clearlinux-latest| |debian-experimental| |debian-testing| |debian-unstable| |fedora-32| |ubuntu-20.04|"
   "manylinux_2_32", "|archlinux-latest| |fedora-33| |opensuse-tumbleweed| |ubuntu-20.10| |ubuntu-rolling|"
   "manylinux_2_32_9000", "|fedora-rawhide|"
.. end compatibility

Known compatibility issues
==========================

List of known compatibility issues

.. begin compatibility_issues
.. csv-table:: Compatibility Issues
   :header: "distro", "incompatible policy", "unavailable libraries"

   "|photon-1.0|", "", "libGL.so.1, libICE.so.6, libSM.so.6, libX11.so.6, libXext.so.6, libXrender.so.1"
   "|photon-2.0|", "", "libGL.so.1, libICE.so.6, libSM.so.6, libX11.so.6, libXext.so.6, libXrender.so.1"
   "|photon-3.0|", "", "libGL.so.1, libICE.so.6, libSM.so.6, libX11.so.6, libXext.so.6, libXrender.so.1"
   "|rhubi-8|", "", "libnsl.so.1"
   "|ubuntu-13.04|", "manylinux_2_17", ""
.. end compatibility_issues
