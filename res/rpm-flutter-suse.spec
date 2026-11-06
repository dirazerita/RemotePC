Name:       remotepc
Version:    1.5.1
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://rustdesk.com
Vendor:     Pak Dosen
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/remotepc" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/remotepc"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/remotepc.service -t "%{buildroot}/usr/share/remotepc/files"
install -Dm 644 $HBB/res/remotepc.desktop -t "%{buildroot}/usr/share/remotepc/files"
install -Dm 644 $HBB/res/remotepc-link.desktop -t "%{buildroot}/usr/share/remotepc/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/remotepc.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/remotepc.svg"

%files
/usr/share/remotepc/*
/usr/share/remotepc/files/remotepc.service
/usr/share/icons/hicolor/256x256/apps/remotepc.png
/usr/share/icons/hicolor/scalable/apps/remotepc.svg
/usr/share/remotepc/files/remotepc.desktop
/usr/share/remotepc/files/remotepc-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop remotepc || true
  ;;
esac

%post
cp /usr/share/remotepc/files/remotepc.service /etc/systemd/system/remotepc.service
cp /usr/share/remotepc/files/remotepc.desktop /usr/share/applications/
cp /usr/share/remotepc/files/remotepc-link.desktop /usr/share/applications/
ln -sf /usr/share/remotepc/remotepc /usr/bin/remotepc
systemctl daemon-reload
systemctl enable remotepc
systemctl start remotepc
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop remotepc || true
    systemctl disable remotepc || true
    rm /etc/systemd/system/remotepc.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/bin/remotepc || true
    rmdir /usr/lib/remotepc || true
    rmdir /usr/local/remotepc || true
    rmdir /usr/share/remotepc || true
    rm /usr/share/applications/remotepc.desktop || true
    rm /usr/share/applications/remotepc-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/remotepc || true
    rmdir /usr/local/remotepc || true
  ;;
esac
