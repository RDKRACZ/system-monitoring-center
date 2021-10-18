#!/usr/bin/env python3
from setuptools import setup, find_packages, os
import sys

changelog = 'debian/changelog'
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = ""
    f = open('src/__version__', 'w')
    f.write(version)
    f.close()


def files_in_folder(folder):
    file_paths = []
    for file in [filename for filename in os.listdir(folder)]:
        file_paths.append(folder + file)
    return file_paths

PREFIX="/usr"
if "--flatpak" in sys.argv:
    PREFIX="/app"
    sys.argv.remove("--flatpak")

if PREFIX == "/app":
    os.rename("integration/tr.org.pardus.system-monitoring-center.desktop", "integration/tr.org.pardus.pkexec.system-monitoring-center." + "system-monitoring-center.desktop")
    os.rename("icons/apps/system-monitoring-center.svg", "icons/apps/tr.org.pardus.pkexec.system-monitoring-center." + "system-monitoring-center.svg")
    icon_list = os.listdir("icons/actions/")
    for icon in icon_list:
        os.rename("icons/actions/" + icon, "icons/actions/tr.org.pardus.pkexec.system-monitoring-center." + icon)

data_files = [
    (f"{PREFIX}/share/applications/", ["integration/tr.org.pardus.system-monitoring-center.desktop"]),
    (f"{PREFIX}/share/locale/tr/LC_MESSAGES/", ["translations/tr/system-monitoring-center.mo"]),
    (f"{PREFIX}/share/system-monitoring-center/src/", files_in_folder("src/")),
    (f"{PREFIX}/share/system-monitoring-center/ui/", files_in_folder("ui/")),
    (f"{PREFIX}/share/icons/hicolor/scalable/actions/", files_in_folder("icons/actions/")),
    (f"{PREFIX}/share/icons/hicolor/scalable/apps/", ["icons/apps/system-monitoring-center.svg"]),
    (f"{PREFIX}/share/polkit-1/actions/", ["integration/tr.org.pardus.pkexec.system-monitoring-center.policy"]),
    (f"{PREFIX}/bin/", ["integration/system-monitoring-center"])
]

setup(
    name="System Monitoring Center",
    version=version,
    packages=find_packages(),
    scripts=["integration/system-monitoring-center"],
    install_requires=["PyGObject"],
    data_files=data_files,
    author="Hakan Dündar",
    author_email="hakandundar34coding@gmail.com",
    description="Provides information about system performance and usage.",
    license="GPLv3",
    keywords="system monitor task manager center performance speed frequency cpu usage ram usage swap memory memory usage storage network usage download speed fps frame ratio processes users startup programs services environment variables shell variables os",
    url="https://kod.pardus.org.tr/Hakan/system-monitoring-center",
)
