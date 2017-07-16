FROM i386/debian:jessie-backports

# Forked from github.com/meier-rene/MSConvertGUI-docker
# Separated steps to get more granular security analysis on quay.

RUN apt-get update && \
    apt-get -y install wget

RUN echo "deb http://dl.winehq.org/wine-builds/debian/ jessie main" >> \
      /etc/apt/sources.list.d/winehq.list && \
    wget http://dl.winehq.org/wine-builds/Release.key -qO- | apt-key add - && \
    apt-get update

RUN apt-get -y install \
      bzip2 \
      winehq-staging \
      winbind \
      xvfb

RUN apt-get -y clean && \
    rm -rf \
      /var/lib/apt/lists/* \
      /usr/share/doc \
      /usr/share/doc-base \
      /usr/share/man \
      /usr/share/locale \
      /usr/share/zoneinfo \

RUN wget https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks \
      -O /usr/local/bin/winetricks && chmod +x /usr/local/bin/winetricks

WORKDIR /root/

ADD waitonprocess.sh /root/waitonprocess.sh

RUN chmod +x waitonprocess.sh

# wineserver needs to shut down properly!!!
ENV WINEDEBUG -all,err+all
RUN winetricks -q win7 && ./waitonprocess.sh wineserver
RUN xvfb-run winetricks -q vcrun2008 dotnet40 && ./waitonprocess.sh wineserver

# download ProteoWizard and extract it to C:\pwiz
RUN mkdir /root/.wine/drive_c/pwiz && \
    wget https://teamcity.labkey.org/repository/download/bt36/421524:id/pwiz-bin-windows-x86-vc120-release-3_0_10577.tar.bz2?guest=1 -qO- | \
      tar --directory=/root/.wine/drive_c/pwiz -xj

# put C:\pwiz on the Windows search path
ENV WINEPATH "C:\pwiz"
ENV DISPLAY :0

CMD ["wine", "MSConvertGUI" ]
