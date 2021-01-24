# rss_magnet
rss_magnet


apt update
apt install -y wget
# copy from `apt install --fix-missing`
apt install -y adwaita-icon-theme at-spi2-core cpp cpp-6 dbus dconf-gsettings-backend dconf-service fontconfig fontconfig-config fonts-liberation glib-networking \
  glib-networking-common glib-networking-services gsettings-desktop-schemas gtk-update-icon-cache hicolor-icon-theme libapparmor1 libasound2\
  libasound2-data libatk-bridge2.0-0 libatk1.0-0 libatk1.0-data libatspi2.0-0 libauthen-sasl-perl libavahi-client3 libavahi-common-data\
  libavahi-common3 libbsd0 libcairo-gobject2 libcairo2 libcolord2 libcroco3 libcups2 libdatrie1 libdbus-1-3 libdconf1 libdrm-amdgpu1 libdrm-intel1\
  libdrm-nouveau2 libdrm-radeon1 libdrm2 libedit2 libegl1-mesa libelf1 libencode-locale-perl libepoxy0 libexpat1 libfile-basedir-perl\
  libfile-desktopentry-perl libfile-listing-perl libfile-mimeinfo-perl libfont-afm-perl libfontconfig1 libfontenc1 libfreetype6 libgbm1 libgdbm3\
  libgdk-pixbuf2.0-0 libgdk-pixbuf2.0-common libgl1-mesa-dri libgl1-mesa-glx libglapi-mesa libglib2.0-0 libglib2.0-data libgpm2 libgraphite2-3\
  libgtk-3-0 libgtk-3-bin libgtk-3-common libharfbuzz0b libhtml-form-perl libhtml-format-perl libhtml-parser-perl libhtml-tagset-perl\
  libhtml-tree-perl libhttp-cookies-perl libhttp-daemon-perl libhttp-date-perl libhttp-message-perl libhttp-negotiate-perl libice6 libicu57\
  libio-html-perl libio-socket-ssl-perl libipc-system-simple-perl libisl15 libjbig0 libjpeg62-turbo libjson-glib-1.0-0 libjson-glib-1.0-common\
  liblcms2-2 libllvm3.9 liblwp-mediatypes-perl liblwp-protocol-https-perl libmailtools-perl libmpc3 libmpfr4 libncurses5 libnet-dbus-perl\
  libnet-http-perl libnet-smtp-ssl-perl libnet-ssleay-perl libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libpciaccess0\
  libperl5.24 libpixman-1-0 libpng16-16 libproxy1v5 librest-0.7-0 librsvg2-2 librsvg2-common libsensors4 libsm6 libsoup-gnome2.4-1 libsoup2.4-1\
  libsqlite3-0 libtext-iconv-perl libthai-data libthai0 libtie-ixhash-perl libtiff5 libtimedate-perl libtxc-dxtn-s2tc liburi-perl libwayland-client0\
  libwayland-cursor0 libwayland-egl1-mesa libwayland-server0 libwww-perl libwww-robotrules-perl libx11-6 libx11-data libx11-protocol-perl libx11-xcb1\
  libxau6 libxaw7 libxcb-dri2-0 libxcb-dri3-0 libxcb-glx0 libxcb-present0 libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 libxcb-xfixes0 libxcb1\
  libxcomposite1 libxcursor1 libxdamage1 libxdmcp6 libxext6 libxfixes3 libxft2 libxi6 libxinerama1 libxkbcommon0 libxml-parser-perl libxml-twig-perl\
  libxml-xpathengine-perl libxml2 libxmu6 libxmuu1 libxpm4 libxrandr2 libxrender1 libxshmfence1 libxt6 libxtst6 libxv1 libxxf86dga1 libxxf86vm1\
  netbase perl perl-modules-5.24 perl-openssl-defaults rename sgml-base shared-mime-info ucf x11-common x11-utils x11-xserver-utils xdg-user-dirs\
  xdg-utils xkb-data xml-core

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
